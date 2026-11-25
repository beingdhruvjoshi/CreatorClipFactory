"""CreatorClip Factory - Database Manager
Handles SQLite persistent storage for creators, streams, clips, styles, and queues.
"""
import sqlite3
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path("C:/CreatorClipFactory/database/factory.db")

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn

def init_db():
    conn = get_connection()
    with conn:
        # Creators table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS creators (
                id TEXT PRIMARY KEY,
                channel_name TEXT NOT NULL,
                channel_id TEXT NOT NULL UNIQUE,
                channel_url TEXT NOT NULL,
                permission_status TEXT DEFAULT 'authorized',
                game_category TEXT DEFAULT 'GTA V',
                preferred_language TEXT DEFAULT 'en',
                monitoring_status TEXT DEFAULT 'enabled',
                capture_config TEXT DEFAULT '{}',
                default_style_id TEXT DEFAULT 'creatorclip-default',
                created_at REAL NOT NULL,
                last_stream_at REAL
            )
        """)
        
        # Streams and Recordings table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS streams (
                id TEXT PRIMARY KEY,
                creator_id TEXT NOT NULL,
                stream_title TEXT NOT NULL,
                stream_url TEXT NOT NULL,
                status TEXT NOT NULL, -- 'live', 'recording', 'completed', 'failed', 'interrupted'
                started_at REAL NOT NULL,
                ended_at REAL,
                recording_path TEXT,
                duration_seconds REAL DEFAULT 0,
                metadata_json TEXT DEFAULT '{}',
                FOREIGN KEY (creator_id) REFERENCES creators (id)
            )
        """)

        # Highlight Candidate Moments
        conn.execute("""
            CREATE TABLE IF NOT EXISTS highlights (
                id TEXT PRIMARY KEY,
                stream_id TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL NOT NULL,
                duration REAL NOT NULL,
                score REAL NOT NULL,
                event_type TEXT NOT NULL, -- 'police_chase', 'explosion', 'crash', 'reaction', etc.
                reasons_json TEXT DEFAULT '[]',
                signals_json TEXT DEFAULT '{}',
                rank INTEGER DEFAULT 0,
                selected_for_top5 INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                FOREIGN KEY (stream_id) REFERENCES streams (id)
            )
        """)

        # Editing Batches
        conn.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                id TEXT PRIMARY KEY,
                stream_id TEXT NOT NULL,
                status TEXT NOT NULL, -- 'pending_style', 'pending_approval', 'rendering', 'completed', 'failed'
                selected_style_id TEXT,
                preview_clip_path TEXT,
                preview_approved INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY (stream_id) REFERENCES streams (id)
            )
        """)

        # Final Clips
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clips (
                id TEXT PRIMARY KEY,
                batch_id TEXT NOT NULL,
                highlight_id TEXT NOT NULL,
                title TEXT NOT NULL,
                raw_path TEXT,
                edited_path TEXT,
                upscaled_path TEXT,
                status TEXT NOT NULL, -- 'draft', 'edited', 'upscaling', 'qc_passed', 'qc_failed', 'ready'
                duration REAL DEFAULT 0,
                resolution TEXT DEFAULT '1080x1920',
                fps REAL DEFAULT 30,
                qc_report_json TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                FOREIGN KEY (batch_id) REFERENCES batches (id),
                FOREIGN KEY (highlight_id) REFERENCES highlights (id)
            )
        """)

        # Reference Styles
        conn.execute("""
            CREATE TABLE IF NOT EXISTS styles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source_url TEXT,
                description TEXT DEFAULT '',
                preset_path TEXT NOT NULL,
                metadata_json TEXT DEFAULT '{}',
                version INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)

        # Publishing Queue
        conn.execute("""
            CREATE TABLE IF NOT EXISTS upload_queue (
                id TEXT PRIMARY KEY,
                clip_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                tags_json TEXT DEFAULT '[]',
                privacy_status TEXT DEFAULT 'private', -- 'private', 'unlisted', 'public'
                status TEXT NOT NULL, -- 'queued', 'uploading', 'uploaded', 'failed'
                youtube_video_id TEXT,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                uploaded_at REAL,
                FOREIGN KEY (clip_id) REFERENCES clips (id)
            )
        """)

        # System Metrics & Logs
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                level TEXT NOT NULL,
                component TEXT NOT NULL,
                message TEXT NOT NULL,
                details_json TEXT DEFAULT '{}'
            )
        """)

    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema initialized successfully.")
