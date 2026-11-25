---
name: youtube-live-monitor
description: Continuously tracks YouTube livestream statuses across configured authorized creators.
---

# Youtube Live Monitor

## Overview
Continuously tracks YouTube livestream statuses across configured authorized creators.

## Inputs
- Creator channel IDs, YouTube API credentials/yt-dlp stream probes.

## Outputs
- Stream state events (stream_start, stream_end, stream_interrupted).

## Execution Command
```bash
python C:/CreatorClipFactory/core/orchestrator.py --check-streams
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
