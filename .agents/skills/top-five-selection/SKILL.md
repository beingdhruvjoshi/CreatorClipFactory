---
name: top-five-selection
description: Deduplicates candidate moments and selects up to the 5 highest-scoring non-overlapping clips.
---

# Top Five Selection

## Overview
Deduplicates candidate moments and selects up to the 5 highest-scoring non-overlapping clips.

## Inputs
- Ranked highlight moments from completed stream.

## Outputs
- Top 5 selected clips saved to SQLite editing batch.

## Execution Command
```bash
python C:/CreatorClipFactory/core/gta_detector.py --select-top-5
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
