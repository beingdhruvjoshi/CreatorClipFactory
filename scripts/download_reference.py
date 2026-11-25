import subprocess
import sys
from pathlib import Path

url = "https://youtube.com/shorts/nrf8gDfCNiY"
dest_dir = Path("C:/CreatorClipFactory/reference-library/incoming")
dest_dir.mkdir(parents=True, exist_ok=True)
out_template = str(dest_dir / "gta_ref.%(ext)s")

python_exe = sys.executable

cmd = [
    python_exe, "-m", "yt_dlp",
    "--no-check-certificates",
    "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "--merge-output-format", "mp4",
    "-o", out_template,
    url
]

print("Executing yt-dlp download...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

# Check files
files = list(dest_dir.glob("gta_ref*"))
print(f"Downloaded files: {[str(f) for f in files]}")
