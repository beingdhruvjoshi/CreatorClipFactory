---
name: style-library-manager
description: Provides CRUD, duplicate, re-analyze, and version control for reference editing styles.
---

# Style Library Manager

## Overview
Provides CRUD, duplicate, re-analyze, and version control for reference editing styles.

## Inputs
- Style ID, action (add, edit, duplicate, delete, restore).

## Outputs
- Updated style registry and version history.

## Execution Command
```bash
python C:/CreatorClipFactory/core/style_library.py --manage
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
