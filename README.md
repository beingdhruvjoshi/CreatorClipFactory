# CreatorClip Factory

A local-first automated YouTube livestream clipping, highlight detection, style cloning, 4K upscaling, quality-control, and Shorts upload-queuing system with a FastAPI dashboard.

## Architecture & Key Modules

- **Core Pipeline (`core/`)**
  - `db_manager.py` — SQLite WAL persistence for creators, streams, highlights, batches, clips, and upload queues.
  - `orchestrator.py` — Background supervisor coordinating pending stream analysis, batch rendering, and upscaling queues.
  - `gta_detector.py` — OpenCV frame intelligence, audio transient spike analysis, and top-5 highlight selection.
  - `style_library.py` — Reference video ingestion, editing DNA extraction, and versioned style presets.
  - `upscaler.py` — GPU-aware routing between Real-ESRGAN NCNN Vulkan 4K upscaling and FFmpeg scaling.
  - `qc_engine.py` — Automated verification of aspect ratio (9:16), resolution (`1080x1920` / `2160x3840`), duration, and audio streams.
  - `publisher.py` — YouTube Data API v3 upload queue manager with daily quota tracking (`10,000` points/day) and `private`/`unlisted` defaults.
  - `gpu_manager.py` — Sequential GPU task locking and VRAM monitoring via `nvidia-smi`.
- **Dashboard (`dashboard/`)** — FastAPI + Jinja2 web UI (`app.py`, `templates/index.html`) served on `http://127.0.0.1:8000`.
- **Automation & Setup (`scripts/` & root `.ps1`)** — Environment bootstrap (`install.ps1`, `setup.ps1`), service lifecycle (`start.ps1`, `stop.ps1`), diagnostics (`health-check.ps1`), upstream repo updater (`update.ps1`), and helper pipeline scripts.
- **Agent Skills (`.agents/skills/`)** — 26 generated Antigravity workflow skills covering stream capture, detection, styling, upscaling, QC, and publishing.
- **Tests (`tests/`)** — End-to-end synthetic pipeline verification (`tests/test_pipeline_e2e.py`).

## Upstream Repositories (Not Committed)

To keep this repository focused on the CreatorClip Factory integration layer and avoid nested Git repositories or large binaries, upstream clones, virtual environments, models, tools, recordings, renders, and secrets are excluded via `.gitignore`.

Clone or restore the pinned upstream dependencies using `scripts/clone_repos.ps1` (pinned versions recorded in `config/installed_commits.json`):

- **PeakCut** (`core/peakcut`) — https://github.com/haziqahmedqasmi/peakcut
- **Video Editing Skills** (`skills/video-editing-skills`) — https://github.com/zaddy99999/video-editing-skills

## Quick Start (Windows)

1. Restore directories, upstream repositories, Python venv, local Ollama models, and Real-ESRGAN binaries:
   ```powershell
   .\install.ps1
   ```
2. Verify system dependencies (`nvidia-smi`, Python venv, FFmpeg, Ollama, Real-ESRGAN, SQLite DB, cloned repos):
   ```powershell
   .\health-check.ps1
   ```
3. Launch local services and the dashboard (`http://127.0.0.1:8000`):
   ```powershell
   .\start.ps1
   ```
4. Stop background services:
   ```powershell
   .\stop.ps1
   ```

## Credentials & Local Data

- Place YouTube OAuth client secrets at `config/client_secrets.json` (and generated token at `config/youtube_token.json`). Both are excluded from Git tracking via `.gitignore`.
- Runtime recordings, rolling buffers, reference media, rendered clips, SQLite databases, and logs are ignored by `.gitignore`.
