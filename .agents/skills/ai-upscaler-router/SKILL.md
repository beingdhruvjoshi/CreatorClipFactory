---
name: ai-upscaler-router
description: Inspects clip resolution and GPU load to route between Real-ESRGAN and Lanczos scaling.
---

# Ai Upscaler Router

## Overview
Inspects clip resolution and GPU load to route between Real-ESRGAN and Lanczos scaling.

## Inputs
- Edited 1080x1920 clip, VRAM telemetry.

## Outputs
- Routing decision (AI upscale vs direct scale).

## Execution Command
```bash
python C:/CreatorClipFactory/core/upscaler.py --route
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
