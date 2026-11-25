---
name: reference-style-analyser
description: Extracts cut frequencies, hook structure, caption styling, and color grading from reference video.
---

# Reference Style Analyser

## Overview
Extracts cut frequencies, hook structure, caption styling, and color grading from reference video.

## Inputs
- Reference video path.

## Outputs
- style.json, analysis.md, and thumbnail.jpg in style folder.

## Execution Command
```bash
python C:/CreatorClipFactory/core/style_library.py --analyze
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
