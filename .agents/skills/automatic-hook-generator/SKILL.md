---
name: automatic-hook-generator
description: Crafts high-retention 2-3s opening hooks using peak action teaser or caption hook.
---

# Automatic Hook Generator

## Overview
Crafts high-retention 2-3s opening hooks using peak action teaser or caption hook.

## Inputs
- Clip highlight segment, audio transients.

## Outputs
- Hook sequence composited at clip start.

## Execution Command
```bash
node C:/CreatorClipFactory/skills/video-editing-skills/skills/hook-overlay/scripts/render-hook.mjs
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
