import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Load top 5 segments
segments_file = Path("C:/CreatorClipFactory/analysis/top5_segments.json")
with open(segments_file, "r", encoding="utf-8") as f:
    top5 = json.load(f)

stream_url = "https://www.youtube.com/live/izXcd-bU72k"
rec_dir = Path("C:/CreatorClipFactory/recordings/vice_city_stream")
rec_dir.mkdir(parents=True, exist_ok=True)
clips_dir = Path("C:/CreatorClipFactory/clips")
clips_dir.mkdir(parents=True, exist_ok=True)
renders_dir = Path("C:/CreatorClipFactory/renders")
renders_dir.mkdir(parents=True, exist_ok=True)
previews_dir = Path("C:/CreatorClipFactory/previews")
previews_dir.mkdir(parents=True, exist_ok=True)

ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
python_exe = sys.executable

print("==================================================")
print("DOWNLOADING 5 HIGH-ENERGY 30-SEC VIRAL SEGMENTS")
print("==================================================")

downloaded_segments = []
for s in top5:
    rank = s["rank"]
    start_s = s["start"]
    end_s = s["end"]
    
    # Format HH:MM:SS
    m, sec = divmod(int(start_s), 60)
    h, m = divmod(m, 60)
    start_str = f"{h:02d}:{m:02d}:{sec:02d}"

    m_e, sec_e = divmod(int(end_s), 60)
    h_e, m_e = divmod(m_e, 60)
    end_str = f"{h_e:02d}:{m_e:02d}:{sec_e:02d}"

    out_file = rec_dir / f"segment_{rank}.mp4"
    print(f"\n[Segment #{rank}] Range: {start_str} - {end_str} ({start_s}s - {end_s}s)...")
    
    cmd_dl = [
        python_exe, "-m", "yt_dlp",
        "--no-check-certificates",
        "--download-sections", f"*{start_str}-{end_str}",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]",
        "--merge-output-format", "mp4",
        "--force-overwrites",
        "-o", str(out_file),
        stream_url
    ]
    res = subprocess.run(cmd_dl, capture_output=True, text=True)
    if out_file.exists():
        print(f"-> Successfully downloaded: {out_file} ({out_file.stat().st_size / 1024 / 1024:.2f} MB)")
        downloaded_segments.append({
            "rank": rank,
            "path": str(out_file),
            "start": start_s,
            "end": end_s,
            "score": s["score"],
            "reasons": s["reasons"]
        })
    else:
        print(f"-> Download warning for segment #{rank}: {res.stderr[:200]}")

print(f"\nDownloaded {len(downloaded_segments)} segments successfully.")
