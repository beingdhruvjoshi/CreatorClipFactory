---
name: gpu-resource-scheduler
description: Enforces sequential heavy-model execution and monitors 6GB RTX 4050 VRAM.
---

# Gpu Resource Scheduler

## Overview
Enforces sequential heavy-model execution and monitors 6GB RTX 4050 VRAM.

## Inputs
- Requested task memory, current VRAM free.

## Outputs
- Execution lock grant or CPU fallback trigger.

## Execution Command
```bash
python C:/CreatorClipFactory/core/gpu_manager.py --check-lock
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
