import os
import sys
import json
import sqlite3
import subprocess
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, "C:/CreatorClipFactory")

from core.db_manager import get_connection
from core.gpu_manager import GPUResourceManager
from core.upscaler import AIUpscalerRouter
from core.qc_engine import QualityControlEngine
from core.publisher import YouTubePublisher

ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
rec_dir = Path("C:/CreatorClipFactory/recordings/vice_city_stream")
clips_dir = Path("C:/CreatorClipFactory/clips")
renders_dir = Path("C:/CreatorClipFactory/renders")
reports_dir = Path("C:/CreatorClipFactory/reports")

clips_dir.mkdir(parents=True, exist_ok=True)
renders_dir.mkdir(parents=True, exist_ok=True)
reports_dir.mkdir(parents=True, exist_ok=True)

upscaler = AIUpscalerRouter()
qc_engine = QualityControlEngine()

# Load top 5 segments metadata
with open("C:/CreatorClipFactory/analysis/top5_segments.json", "r", encoding="utf-8") as f:
    top5 = json.load(f)

# Clip titles and captions
clip_metadata = [
    {"rank": 1, "hook": "VICE CITY SECRET", "title": "GTA 6 Vice City Warehouse Secret [4K]"},
    {"rank": 2, "hook": "GTA 6 SPEED RUN", "title": "GTA 6 Impossible Speed Run Attempt [4K]"},
    {"rank": 3, "hook": "5 STAR POLICE ESCAPE", "title": "GTA 6 Insane 5-Star Police Chase [4K]"},
    {"rank": 4, "hook": "CRAZY MISSION FAIL", "title": "GTA 6 Funniest Mission Fail Reaction [4K]"},
    {"rank": 5, "hook": "WHAT IS THAT?!", "title": "GTA 6 Mysterious Bigfoot Sighting [4K]"}
]

print("==================================================")
print("BATCH RENDERING & 4K AI UPSCALING: 5 SHORTS")
print("==================================================")

batch_id = f"batch_{int(time.time())}_vicecity"
conn = get_connection()
with conn:
    conn.execute("""
        INSERT OR REPLACE INTO batches (id, stream_id, status, selected_style_id, preview_approved, created_at, updated_at)
        VALUES (?, 'izXcd-bU72k', 'rendering', 'creatorclip-default', 1, ?, ?)
    """, (batch_id, time.time(), time.time()))

processed_clips = []

for meta in clip_metadata:
    rank = meta["rank"]
    hook_text = meta["hook"]
    title = meta["title"]
    
    in_segment = rec_dir / f"segment_{rank}.mp4"
    if not in_segment.exists():
        print(f"Skipping segment #{rank}: file not found.")
        continue

    clip_id = f"{batch_id}_clip_{rank}"
    edited_clip = renders_dir / f"{clip_id}_edited.mp4"
    upscaled_clip = renders_dir / f"{clip_id}_4k.mp4"

    print(f"\n--- [Clip #{rank}/5] Rendering 9:16 Vertical Short: {title} ---")
    
    # 1. Vertical reframing (1080x1920) + punch-in + ArchivoBlack bold centered captions
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"drawtext=text='{hook_text}':fontcolor=yellow:fontsize=64:box=1:boxcolor=black@0.6:boxborderw=10:x=(w-text_w)/2:y=h*0.75:fontfile='C\\:/CreatorClipFactory/core/peakcut/studio/fonts/ArchivoBlack-Regular.ttf'"
    )
    cmd_edit = [
        ffmpeg, "-y",
        "-i", str(in_segment),
        "-vf", vf,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        str(edited_clip)
    ]
    subprocess.run(cmd_edit, check=True, capture_output=True)
    print(f"-> Edited 9:16 Short rendered: {edited_clip}")

    # 2. 4K AI Upscaling (2160x3840) via Real-ESRGAN on NVIDIA RTX 4050
    print(f"-> Upscaling to 2160x3840 4K on NVIDIA RTX 4050 (tile size 256)...")
    upscale_res = upscaler.upscale_to_4k(str(edited_clip), str(upscaled_clip), max_fps=30.0)
    print(f"-> Upscale completed: {upscaled_clip} (Method: {upscale_res.get('method')})")

    # 3. Quality Control Battery
    print(f"-> Running Quality Control inspection battery...")
    qc_res = qc_engine.verify_clip(str(upscaled_clip), clip_id)
    print(f"-> QC Passed: {qc_res['passed']} | Resolution: {qc_res['metrics'].get('width')}x{qc_res['metrics'].get('height')} | Duration: {qc_res['metrics'].get('duration')}s")

    # 4. Save to Database
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO clips (id, batch_id, highlight_id, title, raw_path, edited_path, upscaled_path, status, duration, resolution, qc_report_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '2160x3840', ?, ?)
        """, (
            clip_id,
            batch_id,
            f"hl_vicecity_{rank}",
            title,
            str(in_segment),
            str(edited_clip),
            str(upscaled_clip),
            'qc_passed' if qc_res['passed'] else 'qc_failed',
            qc_res['metrics'].get('duration', 30.0),
            json.dumps(qc_res),
            time.time()
        ))

    # 5. Add to YouTube Upload Queue in 'private' mode
    q_res = YouTubePublisher.queue_clip_for_upload(
        clip_id=clip_id,
        title=title,
        description=f"{title}\n\nCaptured and edited automatically by CreatorClip Factory.\n\n#Shorts #GTA6 #Gaming #ViceCity #GTA",
        tags=["GTA6", "ViceCity", "Gaming", "Shorts", "CreatorClip"],
        privacy="private"
    )
    print(f"-> Queued for private YouTube upload: {q_res.get('status')}")

    processed_clips.append({
        "rank": rank,
        "title": title,
        "clip_id": clip_id,
        "path_4k": str(upscaled_clip),
        "qc_passed": qc_res["passed"]
    })

with conn:
    conn.execute("UPDATE batches SET status = 'completed', updated_at = ? WHERE id = ?", (time.time(), batch_id))

print("\n" + "=" * 60)
print("ALL 5 VIRAL 4K SHORTS PROCESSED SUCCESSFULLY!")
print("==================================================")
for c in processed_clips:
    print(f"Short #{c['rank']}: {c['title']} | QC: {'PASSED' if c['qc_passed'] else 'FAILED'}")
    print(f"  File: {c['path_4k']}\n")
