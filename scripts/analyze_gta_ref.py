import cv2
import json
import numpy as np
import subprocess
from pathlib import Path

video_path = Path("C:/CreatorClipFactory/reference-library/incoming/gta_ref.mp4")
ffprobe = r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

# 1. FFprobe metadata
cmd = [
    ffprobe, "-v", "quiet",
    "-print_format", "json",
    "-show_format", "-show_streams",
    str(video_path)
]
res = subprocess.run(cmd, capture_output=True, text=True, check=True)
meta = json.loads(res.stdout)

v_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), {})
width = int(v_stream.get("width", 1080))
height = int(v_stream.get("height", 1920))
duration = float(meta.get("format", {}).get("duration", 0))
fps_eval = v_stream.get("r_frame_rate", "30/1")
num, den = fps_eval.split("/")
fps = float(num) / float(den)

print(f"Video Info: {width}x{height} @ {fps:.2f}fps, Duration: {duration:.2f}s")

# 2. Visual analysis with OpenCV
cap = cv2.VideoCapture(str(video_path))
cuts = []
prev_gray = None
brightness_levels = []
saturations = []
frame_idx = 0

step = max(1, int(fps * 0.1)) # Sample every 100ms
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx % step == 0:
        t = frame_idx / fps
        small = cv2.resize(frame, (320, 180))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        
        brightness = float(np.mean(gray))
        sat = float(np.mean(hsv[:, :, 1]))
        brightness_levels.append(brightness)
        saturations.append(sat)

        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            mean_diff = float(np.mean(diff))
            # Cut threshold
            if mean_diff > 35.0:
                cuts.append(t)
        prev_gray = gray
    frame_idx += 1

cap.release()

avg_cut_interval = duration / max(1, len(cuts))
cuts_per_min = (len(cuts) / max(1.0, duration)) * 60

print(f"Detected Cuts: {len(cuts)} ({cuts_per_min:.1f} cuts/min)")
print(f"Average Cut Interval: {avg_cut_interval:.2f}s")
print(f"Average Brightness: {np.mean(brightness_levels):.1f}")
print(f"Average Saturation: {np.mean(saturations):.1f}")
