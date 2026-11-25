"""CreatorClip Factory - Local Management Dashboard
FastAPI Application serving all 14 monitoring, editing, and queue management modules.
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add project root to sys.path
sys.path.insert(0, "C:/CreatorClipFactory")

from core.db_manager import get_connection, init_db
from core.gpu_manager import GPUResourceManager
from core.style_library import StyleManager
from core.publisher import YouTubePublisher
from core.orchestrator import FactoryOrchestrator

app = FastAPI(title="CreatorClip Factory Dashboard")

# Initialize DB and Styles
init_db()
StyleManager.initialize_defaults()

orchestrator = FactoryOrchestrator()

# Templates
templates_dir = Path("C:/CreatorClipFactory/dashboard/templates")
templates_dir.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Static
static_dir = Path("C:/CreatorClipFactory/dashboard/static")
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.on_event("startup")
def startup_event():
    orchestrator.start_supervisor()

@app.on_event("shutdown")
def shutdown_event():
    orchestrator.stop_supervisor()

# ----------------- REST APIs & PAGES ----------------- #

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    conn = get_connection()
    creators = conn.execute("SELECT * FROM creators").fetchall()
    streams = conn.execute("SELECT * FROM streams ORDER BY started_at DESC LIMIT 5").fetchall()
    batches = conn.execute("SELECT * FROM batches ORDER BY created_at DESC LIMIT 5").fetchall()
    clips = conn.execute("SELECT * FROM clips ORDER BY created_at DESC LIMIT 10").fetchall()
    styles = StyleManager.list_styles()
    gpu = GPUResourceManager.get_gpu_status()
    quota = YouTubePublisher.get_quota_status()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "creators": creators,
            "streams": streams,
            "batches": batches,
            "clips": clips,
            "styles": styles,
            "gpu": gpu,
            "quota": quota
        }
    )

@app.get("/api/status")
def api_status():
    gpu = GPUResourceManager.get_gpu_status()
    quota = YouTubePublisher.get_quota_status()
    conn = get_connection()
    active_streams = conn.execute("SELECT COUNT(*) as count FROM streams WHERE status IN ('live', 'recording')").fetchone()["count"]
    pending_batches = conn.execute("SELECT COUNT(*) as count FROM batches WHERE status IN ('pending_style', 'pending_approval', 'rendering')").fetchone()["count"]
    total_clips = conn.execute("SELECT COUNT(*) as count FROM clips").fetchone()["count"]
    return {
        "gpu": gpu,
        "quota": quota,
        "active_streams": active_streams,
        "pending_batches": pending_batches,
        "total_clips": total_clips
    }

# Creators
@app.get("/api/creators")
def api_get_creators():
    conn = get_connection()
    creators = conn.execute("SELECT * FROM creators").fetchall()
    return [dict(c) for c in creators]

@app.post("/api/creators/add")
def api_add_creator(
    channel_name: str = Form(...),
    channel_id: str = Form(...),
    channel_url: str = Form(...),
    game_category: str = Form("GTA V"),
    preferred_language: str = Form("en"),
    default_style_id: str = Form("creatorclip-default")
):
    conn = get_connection()
    cid = f"cr_{int(time.time())}_{channel_id[:6]}"
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO creators (id, channel_name, channel_id, channel_url, permission_status, game_category, preferred_language, monitoring_status, default_style_id, created_at)
            VALUES (?, ?, ?, ?, 'authorized', ?, ?, 'enabled', ?, ?)
        """, (cid, channel_name, channel_id, channel_url, game_category, preferred_language, default_style_id, time.time()))
    return RedirectResponse(url="/", status_code=303)

# Style Library
@app.get("/api/styles")
def api_get_styles():
    return StyleManager.list_styles()

@app.post("/api/styles/add")
def api_add_style(name: str = Form(...), source_url: str = Form("")):
    # If a sample or URL is provided, analyze it
    sample_video = "C:/CreatorClipFactory/reference-library/incoming/sample_ref.mp4"
    if not Path(sample_video).exists():
        # create mock sample reference video for analysis
        subprocess.run([
            r"C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe",
            "-y", "-f", "lavfi", "-i", "testsrc=duration=15:size=1080x1920:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=1000:duration=15",
            "-c:v", "libx264", "-c:a", "aac", sample_video
        ], capture_output=True)

    style = StyleManager.analyze_reference_video(sample_video, name, source_url)
    return RedirectResponse(url="/", status_code=303)

# Batches & Mandatory Style Selection
@app.post("/api/batches/{batch_id}/select_style")
def api_batch_select_style(batch_id: str, style_id: str = Form(...)):
    conn = get_connection()
    with conn:
        conn.execute("""
            UPDATE batches
            SET selected_style_id = ?, status = 'pending_approval', updated_at = ?
            WHERE id = ?
        """, (style_id, time.time(), batch_id))
    return RedirectResponse(url="/", status_code=303)

@app.post("/api/batches/{batch_id}/approve")
def api_batch_approve(batch_id: str):
    conn = get_connection()
    with conn:
        conn.execute("""
            UPDATE batches
            SET preview_approved = 1, status = 'rendering', updated_at = ?
            WHERE id = ?
        """, (time.time(), batch_id))
    return RedirectResponse(url="/", status_code=303)

# YouTube Upload Queue
@app.post("/api/clips/{clip_id}/queue_upload")
def api_queue_upload(clip_id: str, title: str = Form(...), description: str = Form(""), tags: str = Form("GTA,Gaming,Shorts")):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    res = YouTubePublisher.queue_clip_for_upload(clip_id, title, description, tag_list, privacy="private")
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard.app:app", host="127.0.0.1", port=8000, reload=False)
