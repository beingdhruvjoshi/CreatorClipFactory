---
name: 4k-render-manager
description: Orchestrates full 2160x3840 4K export with frame-rate verification and audio restoration.
---

# 4K Render Manager

## Overview
Orchestrates full 2160x3840 4K export with frame-rate verification and audio restoration.

## Inputs
- Upscaled video stream, original high-quality audio.

## Outputs
- 2160x3840 4K final Short at C:/CreatorClipFactory/renders.

## Execution Command
```bash
python C:/CreatorClipFactory/core/upscaler.py --export-4k
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
