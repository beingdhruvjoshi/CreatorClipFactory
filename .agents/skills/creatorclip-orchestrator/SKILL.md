---
name: creatorclip-orchestrator
description: Master coordinator for end-to-end pipeline execution from stream to published 4K Short.
---

# Creatorclip Orchestrator

## Overview
Master coordinator for end-to-end pipeline execution from stream to published 4K Short.

## Inputs
- Livestream event or manual trigger.

## Outputs
- Fully completed, styled, 4K upscaled, and QC-verified YouTube Shorts.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --run-all
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
