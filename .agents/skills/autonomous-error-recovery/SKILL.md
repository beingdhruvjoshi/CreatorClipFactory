---
name: autonomous-error-recovery
description: Handles automatic retry, GPU memory flush, checkpoint restore, and service recovery.
---

# Autonomous Error Recovery

## Overview
Handles automatic retry, GPU memory flush, checkpoint restore, and service recovery.

## Inputs
- Error signal or job crash event.

## Outputs
- Recovered state, freed resources, retry dispatched.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --recover
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
