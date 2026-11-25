---
name: vertical-smart-reframing
description: Reframes 16:9 gameplay footage to 9:16 vertical (1080x1920) with action tracking.
---

# Vertical Smart Reframing

## Overview
Reframes 16:9 gameplay footage to 9:16 vertical (1080x1920) with action tracking.

## Inputs
- 16:9 video segment.

## Outputs
- Reframed 9:16 vertical MP4 video.

## Execution Command
```bash
ffmpeg -i input.mp4 -vf 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920' output.mp4
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
