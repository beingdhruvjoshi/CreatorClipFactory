---
name: contextual-highlight-detector
description: Combines audio energy peaks, visual dynamics, and speech context into highlight scores.
---

# Contextual Highlight Detector

## Overview
Combines audio energy peaks, visual dynamics, and speech context into highlight scores.

## Inputs
- Stream recording, transcript segments, audio waveforms.

## Outputs
- Contextual highlight score list (0-100) with event triggers.

## Execution Command
```bash
python C:/CreatorClipFactory/core/gta_detector.py --detect-highlights
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
