import zipfile
import io
import requests
from pathlib import Path

url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip"
dest = Path("C:/CreatorClipFactory/tools/realesrgan")
dest.mkdir(parents=True, exist_ok=True)

print(f"Downloading complete Real-ESRGAN release from {url}...")
resp = requests.get(url)
print("Extracting files...")
with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
    z.extractall(str(dest))

print("Verifying models folder...")
models_dir = dest / "models"
if models_dir.exists():
    models = list(models_dir.glob("*.param"))
    print(f"Installed {len(models)} model param files:")
    for m in models:
        print(" -", m.name)

print("Real-ESRGAN package update complete!")
