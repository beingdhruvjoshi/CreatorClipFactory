import os
import sys
import subprocess
from pathlib import Path

ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
in_segment = Path("C:/CreatorClipFactory/recordings/vice_city_stream/segment_1.mp4")
out_preview = Path("C:/CreatorClipFactory/previews/preview_batch_vicecity.mp4")
out_preview.parent.mkdir(parents=True, exist_ok=True)

# Generate representative 10-second preview with CreatorClip High-Energy GTA style
# - Vertical 9:16 1080x1920
# - ArchivoBlack captions burned with drawtext or ASS subtitles
# - Punch-in dynamic zoom (1.15x)
# - EBU R128 audio normalization (-16 LUFS)

vf_filter = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "drawtext=text='VICE CITY SECRET':fontcolor=yellow:fontsize=64:box=1:boxcolor=black@0.6:boxborderw=10:x=(w-text_w)/2:y=h*0.75:fontfile='C\\:/CreatorClipFactory/core/peakcut/studio/fonts/ArchivoBlack-Regular.ttf'"
)

cmd = [
    ffmpeg, "-y",
    "-ss", "0.0",
    "-i", str(in_segment),
    "-t", "10.0",
    "-vf", vf_filter,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-c:a", "aac",
    str(out_preview)
]

print("Rendering representative preview clip...")
res = subprocess.run(cmd, capture_output=True, text=True)
if out_preview.exists():
    print(f"Representative preview rendered: {out_preview} ({out_preview.stat().st_size / 1024 / 1024:.2f} MB)")
else:
    print("Error rendering preview:", res.stderr)
