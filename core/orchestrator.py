"""CreatorClip Factory - Autonomous Pipeline Orchestrator & Background Supervisor
Coordinates stream capture, highlight detection, style selection, editing, 4K upscaling, and QC.
"""
import os
import sys
import time
import json
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional

from core.db_manager import get_connection, init_db
from core.gpu_manager import GPUResourceManager
from core.gta_detector import GTAGameplayDetector
from core.style_library import StyleManager
from core.upscaler import AIUpscalerRouter
from core.qc_engine import QualityControlEngine
from core.publisher import YouTubePublisher

class FactoryOrchestrator:
    def __init__(self):
        init_db()
        StyleManager.initialize_defaults()
        self.upscaler = AIUpscalerRouter()
        self.qc = QualityControlEngine()
        self.is_running = False
        self.worker_thread = None

    def start_supervisor(self):
        """Starts the persistent background supervisor loop."""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.worker_thread.start()
        print("CreatorClip Factory supervisor started.")

    def stop_supervisor(self):
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("CreatorClip Factory supervisor stopped.")

    def _run_loop(self):
        while self.is_running:
            try:
                self.process_pending_streams()
                self.process_rendering_batches()
                self.process_upscaling_queue()
            except Exception as e:
                print(f"Supervisor loop encountered error: {e}")
            time.sleep(5)

    def process_pending_streams(self):
        """Finds completed recordings that have not been analyzed yet."""
        conn = get_connection()
        streams = conn.execute("SELECT * FROM streams WHERE status = 'completed' AND id NOT IN (SELECT stream_id FROM batches)").fetchall()
        for stream in streams:
            rec_path = stream["recording_path"]
            if rec_path and Path(rec_path).exists():
                print(f"Analyzing stream {stream['id']} ({stream['stream_title']})...")
                detector = GTAGameplayDetector(rec_path)
                candidates = detector.detect_gta_highlights()
                top5 = detector.select_top_five(candidates)
                
                batch_id = f"batch_{int(time.time())}_{stream['id'][:8]}"
                with conn:
                    conn.execute("""
                        INSERT INTO batches (id, stream_id, status, selected_style_id, created_at, updated_at)
                        VALUES (?, ?, 'pending_style', 'creatorclip-default', ?, ?)
                    """, (batch_id, stream["id"], time.time(), time.time()))

                    for cand in top5:
                        hl_id = f"hl_{int(time.time())}_{cand.start_time}_{cand.end_time}"
                        conn.execute("""
                            INSERT INTO highlights (id, stream_id, start_time, end_time, duration, score, event_type, reasons_json, signals_json, rank, selected_for_top5, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
                        """, (hl_id, stream["id"], cand.start_time, cand.end_time, cand.duration, cand.score, cand.event_type, json.dumps(cand.reasons), json.dumps(cand.signals), cand.rank, time.time()))

                        clip_id = f"clip_{batch_id}_{cand.rank}"
                        conn.execute("""
                            INSERT INTO clips (id, batch_id, highlight_id, title, status, duration, created_at)
                            VALUES (?, ?, ?, ?, 'draft', ?, ?)
                        """, (clip_id, batch_id, hl_id, f"GTA Highlight #{cand.rank} - {cand.event_type}", cand.duration, time.time()))

                print(f"Stream {stream['id']} processed: {len(top5)} top highlights selected into batch {batch_id}.")

    def process_rendering_batches(self):
        """Renders approved batches into vertical shorts with captions and punch-ins."""
        conn = get_connection()
        # Find batches ready for rendering
        batches = conn.execute("SELECT * FROM batches WHERE status = 'rendering'").fetchall()
        for b in batches:
            style_id = b["selected_style_id"] or "creatorclip-default"
            style = StyleManager.get_style(style_id)
            clips = conn.execute("SELECT c.*, h.start_time, h.end_time, s.recording_path FROM clips c JOIN highlights h ON c.highlight_id = h.id JOIN batches b ON c.batch_id = b.id JOIN streams s ON b.stream_id = s.id WHERE c.batch_id = ? AND c.status = 'draft'", (b["id"],)).fetchall()
            
            for c in clips:
                self.render_single_short(c, style)

            with conn:
                conn.execute("UPDATE batches SET status = 'completed', updated_at = ? WHERE id = ?", (time.time(), b["id"]))

    def render_single_short(self, clip_row: Any, style: Dict[str, Any]):
        """Trims, reframes to 9:16 vertical, adds dynamic captions and audio normalization."""
        clip_id = clip_row["id"]
        rec_path = clip_row["recording_path"]
        start_t = clip_row["start_time"]
        duration = clip_row["end_time"] - clip_row["start_time"]
        
        out_dir = Path("C:/CreatorClipFactory/renders")
        out_dir.mkdir(parents=True, exist_ok=True)
        raw_clip = Path("C:/CreatorClipFactory/clips") / f"{clip_id}_raw.mp4"
        raw_clip.parent.mkdir(parents=True, exist_ok=True)
        final_edited = out_dir / f"{clip_id}_edited.mp4"

        ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

        # 1. Trim slice from stream recording
        cmd_trim = [
            ffmpeg, "-y",
            "-ss", str(start_t),
            "-i", str(rec_path),
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            str(raw_clip)
        ]
        subprocess.run(cmd_trim, check=True, capture_output=True)

        # 2. Vertical Reframing (9:16 1080x1920) + punch-in center crop
        # Filter: crop center 1080x1920 from 1920x1080 or scale & crop with subtle zoom
        vf_filter = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "loudnorm=I=-16:TP=-1.5:LRA=11"
        )
        cmd_render = [
            ffmpeg, "-y",
            "-i", str(raw_clip),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            str(final_edited)
        ]
        subprocess.run(cmd_render, check=True, capture_output=True)

        conn = get_connection()
        with conn:
            conn.execute("""
                UPDATE clips
                SET raw_path = ?, edited_path = ?, status = 'edited'
                WHERE id = ?
            """, (str(raw_clip), str(final_edited), clip_id))

        print(f"Clip {clip_id} rendered to {final_edited}.")

    def process_upscaling_queue(self):
        """Takes edited clips and upscales to 4K (2160x3840) with Real-ESRGAN."""
        conn = get_connection()
        clips = conn.execute("SELECT * FROM clips WHERE status = 'edited' AND (upscaled_path IS NULL OR upscaled_path = '')").fetchall()
        for c in clips:
            edited_path = c["edited_path"]
            if not edited_path or not Path(edited_path).exists():
                continue

            upscaled_path = Path("C:/CreatorClipFactory/renders") / f"{c['id']}_4k.mp4"
            print(f"Running 4K upscaling for clip {c['id']}...")
            res = self.upscaler.upscale_to_4k(edited_path, str(upscaled_path))
            
            # Run QC
            final_path = res["output_path"]
            qc_result = self.qc.verify_clip(final_path, c["id"])

            with conn:
                conn.execute("""
                    UPDATE clips
                    SET upscaled_path = ?, status = ?, resolution = ?, qc_report_json = ?
                    WHERE id = ?
                """, (final_path, 'qc_passed' if qc_result['passed'] else 'qc_failed', qc_result['metrics'].get('width', 1080), json.dumps(qc_result), c["id"]))

            print(f"Clip {c['id']} QC result: {'PASSED' if qc_result['passed'] else 'FAILED'}.")

if __name__ == "__main__":
    orch = FactoryOrchestrator()
    print("Orchestrator initialized.")
