---
name: batch-style-selector
description: Mandatory batch style selection prompt and configuration engine.
---

# Batch Style Selector

## Overview
Mandatory batch style selection prompt and configuration engine.

## Inputs
- Batch ID, chosen style ID (saved style, default, creator-specific, or new URL).

## Outputs
- Batch configured with style and transitioned to pending_approval.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --set-batch-style
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
