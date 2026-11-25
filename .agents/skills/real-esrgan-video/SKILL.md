---
name: real-esrgan-video
description: Executes frame-by-frame AI upscaling using Real-ESRGAN NCNN Vulkan with tiled processing.
---

# Real Esrgan Video

## Overview
Executes frame-by-frame AI upscaling using Real-ESRGAN NCNN Vulkan with tiled processing.

## Inputs
- Frame directory or input video, tile size (256/400).

## Outputs
- 4K upscaled frames and reassembled video.

## Execution Command
```bash
C:/CreatorClipFactory/tools/realesrgan/realesrgan-ncnn-vulkan.exe -i in -o out -s 2 -t 256 -g 0
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
