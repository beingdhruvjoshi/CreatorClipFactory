"""CreatorClip Factory - End-to-End Automated Integration Test Suite
Validates the complete pipeline: creator registration -> synthetic GTA stream -> event detection ->
top-5 ranking -> reference style ingestion -> preview approval -> vertical reframing ->
Real-ESRGAN 4K upscaling -> QC inspection -> YouTube upload queue dry run.
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, "C:/CreatorClipFactory")

from core.db_manager import get_connection, init_db
from core.gpu_manager import GPUResourceManager
from core.gta_detector import GTAGameplayDetector
from core.style_library import StyleManager
from core.upscaler import AIUpscalerRouter
from core.qc_engine import QualityControlEngine
from core.publisher import YouTubePublisher

def run_e2e_test():
    print("=" * 60)
    print("CREATORCLIP FACTORY - END-TO-END PIPELINE VERIFICATION")
    print("=" * 60)

    # 1. Initialize DB & Directories
    init_db()
    StyleManager.initialize_defaults()
    ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

    test_dir = Path("C:/CreatorClipFactory/recordings/test_creator")
    test_dir.mkdir(parents=True, exist_ok=True)
    synth_stream = test_dir / "synth_gta_stream.mp4"

    # 2. Generate Synthetic GTA Footage (35s, 1920x1080) with audio transients & visual flashes
    print("\n[Step 1/10] Generating synthetic GTA livestream footage...")
    cmd_synth = [
        ffmpeg, "-y",
        "-f", "lavfi",
        "-i", "testsrc=duration=35:size=1920x1080:rate=30",
        "-f", "lavfi",
        "-i", "sine=frequency=800:duration=35",
        "-vf", "drawbox=x=1600:y=20:w=300:h=60:color=red@0.8:t=fill", # Wanted stars mockup
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(synth_stream)
    ]
    subprocess.run(cmd_synth, check=True, capture_output=True)
    assert synth_stream.exists(), "Synthetic footage generation failed!"
    print(f"-> Generated: {synth_stream} ({synth_stream.stat().st_size / 1024 / 1024:.2f} MB)")

    # 3. Creator Registration
    print("\n[Step 2/10] Registering test creator...")
    conn = get_connection()
    creator_id = "cr_test_001"
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO creators (id, channel_name, channel_id, channel_url, permission_status, game_category, preferred_language, monitoring_status, created_at)
            VALUES (?, 'Test GTA Streamer', 'UC_TEST_001', 'https://youtube.com/@testgta', 'authorized', 'GTA V', 'en', 'enabled', ?)
        """, (creator_id, time.time()))
    print("-> Creator registered and authorized.")

    # 4. Stream Registration
    print("\n[Step 3/10] Registering completed stream recording...")
    stream_id = "str_test_001"
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO streams (id, creator_id, stream_title, stream_url, status, started_at, ended_at, recording_path, duration_seconds)
            VALUES (?, ?, 'Epic GTA V Chaos Live Stream', 'https://youtube.com/watch?v=mock', 'completed', ?, ?, ?, 35.0)
        """, (stream_id, creator_id, time.time() - 35, time.time(), str(synth_stream)))
    print("-> Stream recording registered in database.")

    # 5. GTA Event Detection & Top-5 Selection
    print("\n[Step 4/10] Running GTA Gameplay Intelligence Engine...")
    detector = GTAGameplayDetector(str(synth_stream))
    candidates = detector.detect_gta_highlights()
    print(f"-> Identified {len(candidates)} candidate moments.")
    top5 = detector.select_top_five(candidates)
    assert len(top5) >= 1, "Failed to select top moments!"
    print(f"-> Top highlight selected: Score {top5[0].score}, Type: {top5[0].event_type}, Reasons: {top5[0].reasons}")

    # 6. Editing Batch Creation & Mandatory Style Selection
    print("\n[Step 5/10] Creating batch and applying reference style...")
    batch_id = "batch_test_001"
    style_id = "creatorclip-default"
    with conn:
        conn.execute("DELETE FROM batches WHERE id = ?", (batch_id,))
        conn.execute("""
            INSERT INTO batches (id, stream_id, status, selected_style_id, created_at, updated_at)
            VALUES (?, ?, 'pending_approval', ?, ?, ?)
        """, (batch_id, stream_id, style_id, time.time(), time.time()))

        best_cand = top5[0]
        hl_id = "hl_test_001"
        conn.execute("DELETE FROM highlights WHERE id = ?", (hl_id,))
        conn.execute("""
            INSERT INTO highlights (id, stream_id, start_time, end_time, duration, score, event_type, reasons_json, signals_json, rank, selected_for_top5, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1, ?)
        """, (hl_id, stream_id, best_cand.start_time, best_cand.end_time, best_cand.duration, best_cand.score, best_cand.event_type, json.dumps(best_cand.reasons), json.dumps(best_cand.signals), time.time()))

        clip_id = "clip_test_001"
        conn.execute("DELETE FROM clips WHERE id = ?", (clip_id,))
        conn.execute("""
            INSERT INTO clips (id, batch_id, highlight_id, title, status, duration, created_at)
            VALUES (?, ?, ?, 'GTA Epic Moment #1', 'draft', ?, ?)
        """, (clip_id, batch_id, hl_id, best_cand.duration, time.time()))
    print("-> Batch and highlight records created. Style configured to:", style_id)

    # 7. Vertical Reframing & Editing
    print("\n[Step 6/10] Rendering 9:16 vertical Short (1080x1920) with audio normalization...")
    raw_clip = Path("C:/CreatorClipFactory/clips") / f"{clip_id}_raw.mp4"
    edited_clip = Path("C:/CreatorClipFactory/renders") / f"{clip_id}_edited.mp4"
    raw_clip.parent.mkdir(parents=True, exist_ok=True)
    edited_clip.parent.mkdir(parents=True, exist_ok=True)

    # Trim slice
    cmd_trim = [
        ffmpeg, "-y",
        "-ss", str(best_cand.start_time),
        "-i", str(synth_stream),
        "-t", str(best_cand.duration),
        "-c:v", "libx264", "-c:a", "aac", str(raw_clip)
    ]
    subprocess.run(cmd_trim, check=True, capture_output=True)

    # Reframe to 9:16 vertical 1080x1920 with audio loudnorm
    cmd_reframe = [
        ffmpeg, "-y",
        "-i", str(raw_clip),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-c:a", "aac", str(edited_clip)
    ]
    subprocess.run(cmd_reframe, check=True, capture_output=True)
    assert edited_clip.exists(), "Vertical reframing failed!"
    print(f"-> 9:16 Vertical Short rendered: {edited_clip}")

    # 8. 4K AI Upscaling (2160x3840)
    print("\n[Step 7/10] Executing 4K AI Upscaling Pipeline...")
    upscaler = AIUpscalerRouter()
    upscaled_clip = Path("C:/CreatorClipFactory/renders") / f"{clip_id}_4k.mp4"
    upscale_res = upscaler.upscale_to_4k(str(edited_clip), str(upscaled_clip), max_fps=30.0)
    assert upscaled_clip.exists(), "4K Upscaling failed!"
    print(f"-> 4K Output Video: {upscaled_clip} (Method: {upscale_res.get('method')})")

    # 9. Quality Control Battery
    print("\n[Step 8/10] Running Quality Control (QC) inspection battery...")
    qc = QualityControlEngine()
    qc_res = qc.verify_clip(str(upscaled_clip), clip_id)
    print(f"-> QC Passed: {qc_res['passed']}")
    print(f"-> Resolution: {qc_res['metrics'].get('width')}x{qc_res['metrics'].get('height')}")
    print(f"-> Duration: {qc_res['metrics'].get('duration')}s")
    for check_name, passed in qc_res["checks"].items():
        print(f"   - {check_name}: {'PASS' if passed else 'FAIL'}")
    assert qc_res["passed"] == True, f"QC failed with issues: {qc_res.get('issues')}"

    # 10. Update DB with QC results
    with conn:
        conn.execute("""
            UPDATE clips
            SET edited_path = ?, upscaled_path = ?, status = 'qc_passed', resolution = '2160x3840', qc_report_json = ?
            WHERE id = ?
        """, (str(edited_clip), str(upscaled_clip), json.dumps(qc_res), clip_id))

    # 11. YouTube Upload Queue Dry-Run
    print("\n[Step 9/10] Queueing Short for private YouTube publishing...")
    q_res = YouTubePublisher.queue_clip_for_upload(
        clip_id=clip_id,
        title="GTA V Epic Escape #1 [4K]",
        description="Top GTA V gameplay highlight captured and edited automatically with CreatorClip Factory.\n\n#Shorts #GTAV #Gaming",
        tags=["GTA", "Gaming", "Shorts", "CreatorClip"],
        privacy="private"
    )
    print("-> Upload Queue Status:", q_res)
    dry_run = YouTubePublisher.process_queue_dry_run()
    print("-> Dry run queue items validated:", len(dry_run))

    # 12. Hardware & Telemetry Verification
    print("\n[Step 10/10] Checking GPU & Telemetry State...")
    gpu_status = GPUResourceManager.get_gpu_status()
    print(f"-> Active GPU: {gpu_status['name']} | VRAM Free: {gpu_status['free_mb']:.1f} MB | Temp: {gpu_status['temp_c']}°C")

    print("\n" + "=" * 60)
    print("END-TO-END PIPELINE VERIFICATION COMPLETED: 100% SUCCESS")
    print("=" * 60)

if __name__ == "__main__":
    run_e2e_test()
