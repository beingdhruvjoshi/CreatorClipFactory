---
name: multi-channel-supervisor
description: Coordinates concurrent monitoring of multiple YouTube creators without thread starvation.
---

# Multi Channel Supervisor

## Overview
Coordinates concurrent monitoring of multiple YouTube creators without thread starvation.

## Inputs
- Active creator list, monitoring polling intervals.

## Outputs
- Channel supervision status table, capture worker assignments.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --supervise-channels
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
