---
name: reference-style-ingestion
description: Ingests reference YouTube Shorts or MP4 videos into reference-library/incoming.
---

# Reference Style Ingestion

## Overview
Ingests reference YouTube Shorts or MP4 videos into reference-library/incoming.

## Inputs
- Reference URL or local file path.

## Outputs
- Ingested reference media and metadata in reference-library.

## Execution Command
```bash
python C:/CreatorClipFactory/core/style_library.py --ingest
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
