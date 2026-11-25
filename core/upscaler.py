"""CreatorClip Factory - AI Upscaling Engine
Wraps Real-ESRGAN NCNN Vulkan and FFmpeg with tiled processing and sequential GPU management.
"""
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Tuple

from core.gpu_manager import GPUResourceManager

class AIUpscalerRouter:
    def __init__(self):
        self.realesrgan_exe = Path("C:/CreatorClipFactory/tools/realesrgan/realesrgan-ncnn-vulkan.exe")
        self.ffmpeg_exe = Path(r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
        self.ffprobe_exe = Path(r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
        self.models_dir = Path("C:/CreatorClipFactory/tools/realesrgan/models")
        self.tmp_dir = Path("C:/CreatorClipFactory/rolling-buffer/tmp_upscale")

    def inspect_source(self, video_path: str) -> Dict[str, Any]:
        cmd = [
            str(self.ffprobe_exe),
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(res.stdout)
        v_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
        width = int(v_stream.get("width", 1080))
        height = int(v_stream.get("height", 1920))
        fps_eval = v_stream.get("r_frame_rate", "30/1")
        try:
            num, den = fps_eval.split("/")
            fps = float(num) / float(den)
        except Exception:
            fps = 30.0

        return {
            "width": width,
            "height": height,
            "fps": fps,
            "duration": float(data.get("format", {}).get("duration", 0))
        }

    def should_upscale(self, source_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Determines if AI upscaling is beneficial without degrading quality."""
        w = source_info["width"]
        h = source_info["height"]
        if w >= 2160 and h >= 3840:
            return False, "Source is already native 4K (2160x3840). Direct pass-through."
        if w < 720 or h < 1280:
            return True, "Low resolution source; AI 4x upscaling recommended."
        return True, "1080x1920 source; 2x AI upscaling to 2160x3840 recommended."

    def upscale_to_4k(self, input_video: str, output_video: str, max_fps: float = 30.0) -> Dict[str, Any]:
        """Runs the complete frame-extraction -> Real-ESRGAN -> reassembly -> audio restore pipeline."""
        in_path = Path(input_video).resolve()
        out_path = Path(output_video).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        source_info = self.inspect_source(str(in_path))
        should_run, reason = self.should_upscale(source_info)
        if not should_run:
            shutil.copy(str(in_path), str(out_path))
            return {"status": "bypassed", "reason": reason, "output_path": str(out_path)}

        # Acquire GPU lock to prevent concurrent heavy tasks
        locked = GPUResourceManager.acquire_execution_lock("Real-ESRGAN 4K Upscale", timeout_sec=120)
        if not locked:
            print("GPU busy, falling back to high-quality FFmpeg lanczos 4K scaling.")
            return self._ffmpeg_bicubic_fallback(str(in_path), str(out_path), source_info)

        tile_size = GPUResourceManager.get_optimal_upscale_tile_size()
        work_dir = self.tmp_dir / f"job_{int(time.time())}"
        frames_in = work_dir / "frames_in"
        frames_out = work_dir / "frames_out"
        frames_in.mkdir(parents=True, exist_ok=True)
        frames_out.mkdir(parents=True, exist_ok=True)

        try:
            fps = min(source_info["fps"], max_fps)
            print(f"Extracting frames at {fps:.1f} fps to {frames_in}...")
            cmd_extract = [
                str(self.ffmpeg_exe),
                "-y",
                "-i", str(in_path),
                "-qscale:v", "2",
                str(frames_in / "frame_%06d.png")
            ]
            subprocess.run(cmd_extract, check=True, capture_output=True)

            print(f"Running Real-ESRGAN with tile size {tile_size}...")
            cmd_upscale = [
                str(self.realesrgan_exe),
                "-i", str(frames_in),
                "-o", str(frames_out),
                "-s", "2", # 1080x1920 * 2 = 2160x3840 (exact 4K vertical!)
                "-t", str(tile_size),
                "-g", "1", # NVIDIA GeForce RTX 4050 dGPU
                "-n", "realesr-animevideov3"
            ]
            # If models directory is in root of tools/realesrgan, pass it
            if self.models_dir.exists():
                cmd_upscale.extend(["-m", str(self.models_dir)])

            res = subprocess.run(cmd_upscale, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"Real-ESRGAN error: {res.stderr}. Using FFmpeg scaling fallback.")
                return self._ffmpeg_bicubic_fallback(str(in_path), str(out_path), source_info)

            print("Reassembling frames and restoring audio...")
            cmd_assemble = [
                str(self.ffmpeg_exe),
                "-y",
                "-framerate", str(fps),
                "-i", str(frames_out / "frame_%06d.png"),
                "-i", str(in_path),
                "-map", "0:v:0",
                "-map", "1:a:0?",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                "-crf", "18",
                "-c:a", "copy",
                "-vf", "scale=2160:3840", # enforce exact 2160x3840
                str(out_path)
            ]
            subprocess.run(cmd_assemble, check=True, capture_output=True)

            return {
                "status": "success",
                "method": "Real-ESRGAN NCNN Vulkan",
                "tile_size": tile_size,
                "output_path": str(out_path),
                "resolution": "2160x3840"
            }

        except Exception as e:
            print(f"AI upscaling pipeline encountered error: {e}. Falling back to FFmpeg.")
            return self._ffmpeg_bicubic_fallback(str(in_path), str(out_path), source_info)
        finally:
            GPUResourceManager.release_execution_lock()
            if work_dir.exists():
                shutil.rmtree(work_dir, ignore_errors=True)

    def _ffmpeg_bicubic_fallback(self, input_video: str, output_video: str, source_info: Dict[str, Any]) -> Dict[str, Any]:
        """High-grade FFmpeg Lanczos 4K scaling fallback."""
        cmd = [
            str(self.ffmpeg_exe),
            "-y",
            "-i", str(input_video),
            "-vf", "scale=2160:3840:flags=lanczos",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "copy",
            str(output_video)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return {
            "status": "success",
            "method": "FFmpeg Lanczos 4K Fallback",
            "output_path": str(output_video),
            "resolution": "2160x3840"
        }

if __name__ == "__main__":
    router = AIUpscalerRouter()
    print("Upscaler router initialized.")
