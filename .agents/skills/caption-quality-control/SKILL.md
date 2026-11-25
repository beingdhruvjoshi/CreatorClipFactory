---
name: caption-quality-control
description: Validates subtitle readability, word wrapping, contrast, and font rendering.
---

# Caption Quality Control

## Overview
Validates subtitle readability, word wrapping, contrast, and font rendering.

## Inputs
- Subtitles file (.ass/.srt), rendered video.

## Outputs
- Caption verification report.

## Execution Command
```bash
node C:/CreatorClipFactory/skills/video-editing-skills/skills/captions/scripts/burn.mjs --check
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
