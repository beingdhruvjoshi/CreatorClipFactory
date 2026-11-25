---
name: viral-moment-ranker
description: Ranks candidate clips using virality heuristics (pacing, reaction intensity, action peak).
---

# Viral Moment Ranker

## Overview
Ranks candidate clips using virality heuristics (pacing, reaction intensity, action peak).

## Inputs
- List of highlight candidate moments.

## Outputs
- Ranked highlight candidate list with virality breakdown.

## Execution Command
```bash
python C:/CreatorClipFactory/core/gta_detector.py --rank-moments
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
