---
name: creator-permission-manager
description: Validates channel authorization, licensing permissions, and stream capture agreements.
---

# Creator Permission Manager

## Overview
Validates channel authorization, licensing permissions, and stream capture agreements.

## Inputs
- Channel ID, authorization tokens, terms acceptance.

## Outputs
- Creator permission status record in database.

## Execution Command
```bash
python C:/CreatorClipFactory/core/db_manager.py --verify-creator
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
