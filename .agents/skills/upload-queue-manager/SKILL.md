---
name: upload-queue-manager
description: Tracks upload queues, daily quota limits (10,000 points), retries, and history.
---

# Upload Queue Manager

## Overview
Tracks upload queues, daily quota limits (10,000 points), retries, and history.

## Inputs
- Queue item ID, status update.

## Outputs
- Updated upload queue table in factory.db.

## Execution Command
```bash
python C:/CreatorClipFactory/core/publisher.py --manage-queue
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
