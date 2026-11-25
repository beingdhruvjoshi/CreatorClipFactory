---
name: style-consistency-engine
description: Enforces uniform caption typography, color grading, and zoom cadence across all 5 clips.
---

# Style Consistency Engine

## Overview
Enforces uniform caption typography, color grading, and zoom cadence across all 5 clips.

## Inputs
- Batch clips, active style preset.

## Outputs
- Standardized rendering parameter payload for batch.

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --apply-consistency
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
