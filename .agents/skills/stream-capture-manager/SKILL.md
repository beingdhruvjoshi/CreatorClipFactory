---
name: stream-capture-manager
description: Handles live stream recording into rolling buffers with segment indexing.
---

# Stream Capture Manager

## Overview
Handles live stream recording into rolling buffers with segment indexing.

## Inputs
- Stream URL, creator ID, rolling buffer path.

## Outputs
- Continuous TS/MP4 stream recordings at C:/CreatorClipFactory/recordings.

## Execution Command
```bash
yt-dlp -o C:/CreatorClipFactory/recordings/%(id)s.%(ext)s <stream_url>
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
