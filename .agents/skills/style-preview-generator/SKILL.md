---
name: style-preview-generator
description: Generates a representative 10s preview clip for user verification before full batch render.
---

# Style Preview Generator

## Overview
Generates a representative 10s preview clip for user verification before full batch render.

## Inputs
- Clip #1 from batch, style preset.

## Outputs
- preview.mp4 rendered to previews/ directory.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --generate-preview
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
