import os
import sys
import subprocess
from pathlib import Path

ffmpeg = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
in_segment = Path("C:/CreatorClipFactory/recordings/vice_city_stream/segment_1.mp4")
out_clip = Path("C:/CreatorClipFactory/renders/clip_1_gta_style.mp4")
font_file = "C:/CreatorClipFactory/core/peakcut/studio/fonts/ArchivoBlack-Regular.ttf"

# GTA Reference Style Parameters:
# - 9:16 vertical reframing (1080x1920)
# - 1.18x punch-in zoom for action intensity
# - Color grade: +15% saturation & +12% contrast (vivid GTA street visual)
# - GTA style multi-tier hook & keyword captions:
#   Top Hook: "GTA 6 VICE CITY" (Yellow on black pill)
#   Mid Action: "WAIT FOR IT..." (t=0 to 3) -> "LOOK AT THIS!" (t=3 to 8) -> "SECRET FOUND" (t=8 to 15) -> "TAXI ESCAPE" (t=15 to 30)
# - Audio: EBU R128 loudness normalization (-16 LUFS, TP -1.5)

font_escaped = font_file.replace(":", "\\:").replace("/", "/")

vf_filter = (
    # 1. Color grade: saturation boost & deep contrast
    "eq=saturation=1.20:contrast=1.12:brightness=0.01,"
    # 2. Dynamic 1.18x punch in on center gameplay
    "scale=1274:2265,"
    "crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,"
    # 3. Top Banner Hook Header
    f"drawtext=text='⚡ GTA 6 VICE CITY ⚡':fontcolor=white:fontsize=52:box=1:boxcolor=black@0.75:boxborderw=12:x=(w-text_w)/2:y=220:fontfile='{font_escaped}',"
    # 4. Animated / Timed Dynamic Captions (Middle Third)
    f"drawtext=text='WAIT FOR IT...':fontcolor=yellow:fontsize=68:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.72:enable='between(t,0,3.5)':fontfile='{font_escaped}',"
    f"drawtext=text='SECRET WAREHOUSE!':fontcolor=white:fontsize=72:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.72:enable='between(t,3.5,8.0)':fontfile='{font_escaped}',"
    f"drawtext=text='CALL THE TAXI!':fontcolor=yellow:fontsize=74:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.72:enable='between(t,8.0,16.0)':fontfile='{font_escaped}',"
    f"drawtext=text='NO WAY HE DID THAT':fontcolor=white:fontsize=68:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.72:enable='between(t,16.0,24.0)':fontfile='{font_escaped}',"
    f"drawtext=text='DROP A LIKE 🔥':fontcolor=yellow:fontsize=64:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.72:enable='between(t,24.0,30.0)':fontfile='{font_escaped}'"
)

cmd = [
    ffmpeg, "-y",
    "-i", str(in_segment),
    "-vf", vf_filter,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    str(out_clip)
]

print("Rendering Clip 1 in custom GTA Style...")
res = subprocess.run(cmd, capture_output=True, text=True)
if out_clip.exists():
    print(f"SUCCESS: Rendered Clip 1 in GTA Style: {out_clip} ({out_clip.stat().st_size / 1024 / 1024:.2f} MB)")
else:
    print("Error rendering GTA style clip:", res.stderr)
