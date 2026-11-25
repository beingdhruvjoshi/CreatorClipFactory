"""CreatorClip Factory - Antigravity Custom Skills Generator
Generates the 26 required workspace skills under .agents/skills/ with complete specifications.
"""
from pathlib import Path

SKILLS = {
    "youtube-live-monitor": {
        "description": "Continuously tracks YouTube livestream statuses across configured authorized creators.",
        "inputs": "Creator channel IDs, YouTube API credentials/yt-dlp stream probes.",
        "outputs": "Stream state events (stream_start, stream_end, stream_interrupted).",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --check-streams"
    },
    "creator-permission-manager": {
        "description": "Validates channel authorization, licensing permissions, and stream capture agreements.",
        "inputs": "Channel ID, authorization tokens, terms acceptance.",
        "outputs": "Creator permission status record in database.",
        "command": "python C:/CreatorClipFactory/core/db_manager.py --verify-creator"
    },
    "multi-channel-supervisor": {
        "description": "Coordinates concurrent monitoring of multiple YouTube creators without thread starvation.",
        "inputs": "Active creator list, monitoring polling intervals.",
        "outputs": "Channel supervision status table, capture worker assignments.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --supervise-channels"
    },
    "stream-capture-manager": {
        "description": "Handles live stream recording into rolling buffers with segment indexing.",
        "inputs": "Stream URL, creator ID, rolling buffer path.",
        "outputs": "Continuous TS/MP4 stream recordings at C:/CreatorClipFactory/recordings.",
        "command": "yt-dlp -o C:/CreatorClipFactory/recordings/%(id)s.%(ext)s <stream_url>"
    },
    "gta-gameplay-recognition": {
        "description": "Detects police chases, wanted stars, explosions, crashes, and stunts via OpenCV.",
        "inputs": "Gameplay video path, frame sampling interval.",
        "outputs": "Classified visual event candidates with confidence scores.",
        "command": "python C:/CreatorClipFactory/core/gta_detector.py --scan-visuals"
    },
    "contextual-highlight-detector": {
        "description": "Combines audio energy peaks, visual dynamics, and speech context into highlight scores.",
        "inputs": "Stream recording, transcript segments, audio waveforms.",
        "outputs": "Contextual highlight score list (0-100) with event triggers.",
        "command": "python C:/CreatorClipFactory/core/gta_detector.py --detect-highlights"
    },
    "viral-moment-ranker": {
        "description": "Ranks candidate clips using virality heuristics (pacing, reaction intensity, action peak).",
        "inputs": "List of highlight candidate moments.",
        "outputs": "Ranked highlight candidate list with virality breakdown.",
        "command": "python C:/CreatorClipFactory/core/gta_detector.py --rank-moments"
    },
    "top-five-selection": {
        "description": "Deduplicates candidate moments and selects up to the 5 highest-scoring non-overlapping clips.",
        "inputs": "Ranked highlight moments from completed stream.",
        "outputs": "Top 5 selected clips saved to SQLite editing batch.",
        "command": "python C:/CreatorClipFactory/core/gta_detector.py --select-top-5"
    },
    "reference-style-ingestion": {
        "description": "Ingests reference YouTube Shorts or MP4 videos into reference-library/incoming.",
        "inputs": "Reference URL or local file path.",
        "outputs": "Ingested reference media and metadata in reference-library.",
        "command": "python C:/CreatorClipFactory/core/style_library.py --ingest"
    },
    "reference-style-analyser": {
        "description": "Extracts cut frequencies, hook structure, caption styling, and color grading from reference video.",
        "inputs": "Reference video path.",
        "outputs": "style.json, analysis.md, and thumbnail.jpg in style folder.",
        "command": "python C:/CreatorClipFactory/core/style_library.py --analyze"
    },
    "style-preset-generator": {
        "description": "Compiles analyzed reference styles into usable JSON rendering presets.",
        "inputs": "Style analysis metrics.",
        "outputs": "Reusable preset file in reference-library/style-presets.",
        "command": "python C:/CreatorClipFactory/core/style_library.py --generate-preset"
    },
    "style-library-manager": {
        "description": "Provides CRUD, duplicate, re-analyze, and version control for reference editing styles.",
        "inputs": "Style ID, action (add, edit, duplicate, delete, restore).",
        "outputs": "Updated style registry and version history.",
        "command": "python C:/CreatorClipFactory/core/style_library.py --manage"
    },
    "batch-style-selector": {
        "description": "Mandatory batch style selection prompt and configuration engine.",
        "inputs": "Batch ID, chosen style ID (saved style, default, creator-specific, or new URL).",
        "outputs": "Batch configured with style and transitioned to pending_approval.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --set-batch-style"
    },
    "style-consistency-engine": {
        "description": "Enforces uniform caption typography, color grading, and zoom cadence across all 5 clips.",
        "inputs": "Batch clips, active style preset.",
        "outputs": "Standardized rendering parameter payload for batch.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --apply-consistency"
    },
    "style-preview-generator": {
        "description": "Generates a representative 10s preview clip for user verification before full batch render.",
        "inputs": "Clip #1 from batch, style preset.",
        "outputs": "preview.mp4 rendered to previews/ directory.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --generate-preview"
    },
    "automatic-hook-generator": {
        "description": "Crafts high-retention 2-3s opening hooks using peak action teaser or caption hook.",
        "inputs": "Clip highlight segment, audio transients.",
        "outputs": "Hook sequence composited at clip start.",
        "command": "node C:/CreatorClipFactory/skills/video-editing-skills/skills/hook-overlay/scripts/render-hook.mjs"
    },
    "vertical-smart-reframing": {
        "description": "Reframes 16:9 gameplay footage to 9:16 vertical (1080x1920) with action tracking.",
        "inputs": "16:9 video segment.",
        "outputs": "Reframed 9:16 vertical MP4 video.",
        "command": "ffmpeg -i input.mp4 -vf 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920' output.mp4"
    },
    "caption-quality-control": {
        "description": "Validates subtitle readability, word wrapping, contrast, and font rendering.",
        "inputs": "Subtitles file (.ass/.srt), rendered video.",
        "outputs": "Caption verification report.",
        "command": "node C:/CreatorClipFactory/skills/video-editing-skills/skills/captions/scripts/burn.mjs --check"
    },
    "ai-upscaler-router": {
        "description": "Inspects clip resolution and GPU load to route between Real-ESRGAN and Lanczos scaling.",
        "inputs": "Edited 1080x1920 clip, VRAM telemetry.",
        "outputs": "Routing decision (AI upscale vs direct scale).",
        "command": "python C:/CreatorClipFactory/core/upscaler.py --route"
    },
    "real-esrgan-video": {
        "description": "Executes frame-by-frame AI upscaling using Real-ESRGAN NCNN Vulkan with tiled processing.",
        "inputs": "Frame directory or input video, tile size (256/400).",
        "outputs": "4K upscaled frames and reassembled video.",
        "command": "C:/CreatorClipFactory/tools/realesrgan/realesrgan-ncnn-vulkan.exe -i in -o out -s 2 -t 256 -g 0"
    },
    "4k-render-manager": {
        "description": "Orchestrates full 2160x3840 4K export with frame-rate verification and audio restoration.",
        "inputs": "Upscaled video stream, original high-quality audio.",
        "outputs": "2160x3840 4K final Short at C:/CreatorClipFactory/renders.",
        "command": "python C:/CreatorClipFactory/core/upscaler.py --export-4k"
    },
    "youtube-shorts-publisher": {
        "description": "Publishes approved Shorts to YouTube via OAuth Data API with private/unlisted safeguards.",
        "inputs": "Final 4K clip path, title, description, tags, privacy.",
        "outputs": "YouTube video ID and upload confirmation.",
        "command": "python C:/CreatorClipFactory/core/publisher.py --upload"
    },
    "upload-queue-manager": {
        "description": "Tracks upload queues, daily quota limits (10,000 points), retries, and history.",
        "inputs": "Queue item ID, status update.",
        "outputs": "Updated upload queue table in factory.db.",
        "command": "python C:/CreatorClipFactory/core/publisher.py --manage-queue"
    },
    "gpu-resource-scheduler": {
        "description": "Enforces sequential heavy-model execution and monitors 6GB RTX 4050 VRAM.",
        "inputs": "Requested task memory, current VRAM free.",
        "outputs": "Execution lock grant or CPU fallback trigger.",
        "command": "python C:/CreatorClipFactory/core/gpu_manager.py --check-lock"
    },
    "autonomous-error-recovery": {
        "description": "Handles automatic retry, GPU memory flush, checkpoint restore, and service recovery.",
        "inputs": "Error signal or job crash event.",
        "outputs": "Recovered state, freed resources, retry dispatched.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --recover"
    },
    "creatorclip-orchestrator": {
        "description": "Master coordinator for end-to-end pipeline execution from stream to published 4K Short.",
        "inputs": "Livestream event or manual trigger.",
        "outputs": "Fully completed, styled, 4K upscaled, and QC-verified YouTube Shorts.",
        "command": "python C:/CreatorClipFactory/core/orchestrator.py --run-all"
    }
}

target_dirs = [
    Path("C:/CreatorClipFactory/.agents/skills"),
    Path("d:/factory/.agents/skills")
]

for base_dir in target_dirs:
    base_dir.mkdir(parents=True, exist_ok=True)
    for skill_name, info in SKILLS.items():
        s_dir = base_dir / skill_name
        s_dir.mkdir(parents=True, exist_ok=True)
        content = f"""---
name: {skill_name}
description: {info['description']}
---

# {skill_name.replace('-', ' ').title()}

## Overview
{info['description']}

## Inputs
- {info['inputs']}

## Outputs
- {info['outputs']}

## Execution Command
```bash
{info['command']}
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
"""
        with open(s_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(content)

print(f"Generated {len(SKILLS)} functional Antigravity skills in both target locations.")
