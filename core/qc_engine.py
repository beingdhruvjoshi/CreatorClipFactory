"""CreatorClip Factory - Quality Control (QC) Engine
Validates video integrity, resolution (9:16 vertical), duration, audio, black/frozen frames, and produces QC reports.
"""
import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, Tuple

class QualityControlEngine:
    def __init__(self):
        self.ffmpeg_exe = Path(r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
        self.ffprobe_exe = Path(r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
        self.reports_dir = Path("C:/CreatorClipFactory/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def verify_clip(self, video_path: str, clip_id: str = "") -> Dict[str, Any]:
        """Runs the complete QC inspection battery on a rendered clip."""
        v_path = Path(video_path).resolve()
        report = {
            "clip_id": clip_id or v_path.stem,
            "file_path": str(v_path),
            "timestamp": time.time(),
            "passed": True,
            "checks": {},
            "issues": [],
            "metrics": {}
        }

        if not v_path.exists() or v_path.stat().st_size < 10000:
            report["passed"] = False
            report["issues"].append("File does not exist or size is zero/corrupted.")
            return report

        # 1. FFprobe metadata & Stream inspection
        cmd = [
            str(self.ffprobe_exe),
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(v_path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            meta = json.loads(res.stdout)
        except Exception as e:
            report["passed"] = False
            report["issues"].append(f"Failed to read file container: {e}")
            return report

        v_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
        a_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), None)

        if not v_stream:
            report["passed"] = False
            report["issues"].append("No valid video stream found in container.")
            return report

        width = int(v_stream.get("width", 0))
        height = int(v_stream.get("height", 0))
        duration = float(meta.get("format", {}).get("duration", 0))

        report["metrics"]["width"] = width
        report["metrics"]["height"] = height
        report["metrics"]["duration"] = round(duration, 2)
        report["metrics"]["has_audio"] = (a_stream is not None)

        # Check: 9:16 Aspect Ratio
        is_vertical = (height > width)
        ratio = width / max(1, height)
        # 9/16 = 0.5625
        correct_ratio = abs(ratio - 0.5625) < 0.05
        report["checks"]["aspect_ratio_9_16"] = correct_ratio
        if not correct_ratio:
            report["passed"] = False
            report["issues"].append(f"Invalid aspect ratio ({width}x{height}); expected 9:16 vertical.")

        # Check: Resolution (either 1080x1920 or 2160x3840)
        valid_res = (width >= 1080 and height >= 1920)
        report["checks"]["resolution_hd_or_4k"] = valid_res
        if not valid_res:
            report["passed"] = False
            report["issues"].append(f"Resolution below minimum short target: {width}x{height}")

        # Check: Duration (Shorts must be between 10s and 60s)
        valid_duration = (10.0 <= duration <= 60.5)
        report["checks"]["duration_bounds"] = valid_duration
        if not valid_duration:
            report["passed"] = False
            report["issues"].append(f"Duration {duration:.1f}s is out of bounds (10s - 60s).")

        # Check: Audio stream
        report["checks"]["audio_stream_present"] = (a_stream is not None)
        if not a_stream:
            report["passed"] = False
            report["issues"].append("Audio stream missing.")

        # Check: Black frames (detect if video has unintended black screen > 1.5s)
        try:
            cmd_black = [
                str(self.ffmpeg_exe),
                "-i", str(v_path),
                "-vf", "blackdetect=d=1.5:pix_th=0.10",
                "-an", "-f", "null",
                "-"
            ]
            res_black = subprocess.run(cmd_black, capture_output=True, text=True, timeout=30)
            black_detected = "black_start" in res_black.stderr
            report["checks"]["no_black_frames"] = not black_detected
            if black_detected:
                report["passed"] = False
                report["issues"].append("Unintended black screen detected (> 1.5s).")
        except Exception:
            report["checks"]["no_black_frames"] = True

        # Check: Frozen frames (detect if video is frozen > 2.0s)
        try:
            cmd_freeze = [
                str(self.ffmpeg_exe),
                "-i", str(v_path),
                "-vf", "freezedetect=n=-50dB:d=2.0",
                "-an", "-f", "null",
                "-"
            ]
            res_freeze = subprocess.run(cmd_freeze, capture_output=True, text=True, timeout=30)
            freeze_detected = "freeze_start" in res_freeze.stderr
            report["checks"]["no_frozen_frames"] = not freeze_detected
            if freeze_detected:
                report["passed"] = False
                report["issues"].append("Frozen screen detected (> 2.0s).")
        except Exception:
            report["checks"]["no_frozen_frames"] = True

        # Save report files (JSON + Markdown)
        report_file_json = self.reports_dir / f"qc_{report['clip_id']}.json"
        with open(report_file_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        report_file_md = self.reports_dir / f"qc_{report['clip_id']}.md"
        with open(report_file_md, "w", encoding="utf-8") as f:
            f.write(self._format_markdown_report(report))

        return report

    def _format_markdown_report(self, report: Dict[str, Any]) -> str:
        status_badge = "✅ PASSED" if report["passed"] else "❌ FAILED"
        lines = [
            f"# Quality Control Inspection Report: {report['clip_id']}",
            f"**Overall Status**: {status_badge}",
            f"**File**: `{report['file_path']}`",
            "",
            "## Quality Metrics",
            f"- **Resolution**: `{report['metrics'].get('width')}x{report['metrics'].get('height')}`",
            f"- **Duration**: `{report['metrics'].get('duration')}s`",
            f"- **Audio Track**: `{'Present' if report['metrics'].get('has_audio') else 'Missing'}`",
            "",
            "## Automated Check Battery",
        ]
        for check_name, passed in report["checks"].items():
            mark = "✅" if passed else "❌"
            lines.append(f"- {mark} `{check_name}`: {'PASS' if passed else 'FAIL'}")

        if report["issues"]:
            lines.append("")
            lines.append("## Identified Issues")
            for issue in report["issues"]:
                lines.append(f"- ⚠️ {issue}")

        return "\n".join(lines)

if __name__ == "__main__":
    qc = QualityControlEngine()
    print("Quality Control Engine ready.")
