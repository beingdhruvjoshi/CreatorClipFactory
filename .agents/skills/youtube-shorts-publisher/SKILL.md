---
name: youtube-shorts-publisher
description: Publishes approved Shorts to YouTube via OAuth Data API with private/unlisted safeguards.
---

# Youtube Shorts Publisher

## Overview
Publishes approved Shorts to YouTube via OAuth Data API with private/unlisted safeguards.

## Inputs
- Final 4K clip path, title, description, tags, privacy.

## Outputs
- YouTube video ID and upload confirmation.

## Execution Command
```bash
python C:/CreatorClipFactory/core/publisher.py --upload
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
