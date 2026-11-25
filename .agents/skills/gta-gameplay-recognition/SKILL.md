---
name: gta-gameplay-recognition
description: Detects police chases, wanted stars, explosions, crashes, and stunts via OpenCV.
---

# Gta Gameplay Recognition

## Overview
Detects police chases, wanted stars, explosions, crashes, and stunts via OpenCV.

## Inputs
- Gameplay video path, frame sampling interval.

## Outputs
- Classified visual event candidates with confidence scores.

## Execution Command
```bash
python C:/CreatorClipFactory/core/gta_detector.py --scan-visuals
```

## Dependencies
- Python 3.11 (`C:/CreatorClipFactory/venv/Scripts/python.exe`)
- FFmpeg 9.1 (`ffmpeg.exe`, `ffprobe.exe`)
- Real-ESRGAN NCNN Vulkan (`realesrgan-ncnn-vulkan.exe`)
- Local Ollama (`qwen2.5:1.5b`, `moondream:latest`)
- SQLite database (`C:/CreatorClipFactory/database/factory.db`)

## Error Handling & Safe Fallback
- If GPU VRAM is below threshold (< 1500MB free), defer heavy model tasks or use CPU fallback.
- If network connection interrupts during upload, queue state is set to retry with exponential backoff.
- Any failed render triggers automatic checkpoint restoration.
