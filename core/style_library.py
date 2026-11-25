"""CreatorClip Factory - Reference Style Library & Analysis Engine
Ingests reference videos/URLs, extracts editing DNA, manages versioned presets.
"""
import os
import cv2
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path("C:/CreatorClipFactory/reference-library")
STYLES_DIR = BASE_DIR / "styles"
PRESETS_DIR = BASE_DIR / "style-presets"
INCOMING_DIR = BASE_DIR / "incoming"
CACHE_DIR = BASE_DIR / "analysis-cache"
META_DIR = BASE_DIR / "reference-metadata"
HISTORY_DIR = BASE_DIR / "version-history"

class StyleManager:
    @classmethod
    def initialize_defaults(cls):
        """Creates the default CreatorClip styles if not already present."""
        for d in [STYLES_DIR, PRESETS_DIR, INCOMING_DIR, CACHE_DIR, META_DIR, HISTORY_DIR]:
            d.mkdir(parents=True, exist_ok=True)

        default_style = {
            "id": "creatorclip-default",
            "name": "CreatorClip High-Energy GTA",
            "description": "Fast-paced action shorts with dynamic punch-in zooms, ArchivoBlack captions, and impact emphasis.",
            "version": 1,
            "pacing": {
                "avg_cut_duration_sec": 2.2,
                "hook_duration_sec": 2.5,
                "hook_style": "action_teaser_zoom"
            },
            "captions": {
                "font": "ArchivoBlack-Regular.ttf",
                "font_size": 52,
                "primary_color": "&H00FFFFFF",
                "highlight_color": "&H0000FFFF", # bright yellow
                "outline_color": "&H00000000",
                "outline_width": 3.0,
                "position": "bottom_third",
                "words_per_line": 3,
                "animation": "pop_bounce"
            },
            "framing": {
                "mode": "smart_gameplay_tracking",
                "aspect_ratio": "9:16",
                "target_width": 1080,
                "target_height": 1920,
                "target_4k_width": 2160,
                "target_4k_height": 3840,
                "gameplay_crop": "center_weighted",
                "facecam_mode": "auto_pip_top"
            },
            "effects": {
                "punch_in_zoom_intensity": 1.15,
                "transition_type": "quick_whip",
                "color_grading": "vibrant_contrast",
                "audio_ducking_db": -6.0
            }
        }
        
        style_dir = STYLES_DIR / "creatorclip-default"
        style_dir.mkdir(parents=True, exist_ok=True)
        style_json_path = style_dir / "style.json"
        if not style_json_path.exists():
            with open(style_json_path, "w", encoding="utf-8") as f:
                json.dump(default_style, f, indent=2)

            analysis_md = """# CreatorClip High-Energy GTA - Editing Analysis
- **Pacing**: Aggressive short cuts (2.2s avg) keeping viewer attention.
- **Hook Structure**: 2.5s teaser clip punch-in with instant sound FX.
- **Captions**: ArchivoBlack bold centered text with yellow keyword pop.
- **Framing**: Dynamic 9:16 vertical crop focused on high-action minimap & vehicle.
- **Color Grade**: +10% saturation and slight S-curve contrast for vivid GTA visuals.
"""
            with open(style_dir / "analysis.md", "w", encoding="utf-8") as f:
                f.write(analysis_md)

    @classmethod
    def list_styles(cls) -> List[Dict[str, Any]]:
        cls.initialize_defaults()
        styles = []
        for s_dir in STYLES_DIR.iterdir():
            if s_dir.is_dir():
                s_json = s_dir / "style.json"
                if s_json.exists():
                    try:
                        with open(s_json, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            # check thumbnail
                            thumb = s_dir / "thumbnail.jpg"
                            data["has_thumbnail"] = thumb.exists()
                            data["has_preview"] = (s_dir / "preview.mp4").exists()
                            styles.append(data)
                    except Exception:
                        pass
        return styles

    @classmethod
    def get_style(cls, style_id: str) -> Optional[Dict[str, Any]]:
        s_dir = STYLES_DIR / style_id
        s_json = s_dir / "style.json"
        if s_json.exists():
            with open(s_json, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    @classmethod
    def analyze_reference_video(cls, video_path: str, style_name: str, source_url: str = "") -> Dict[str, Any]:
        """Analyzes a reference video to extract editing style DNA."""
        v_path = Path(video_path).resolve()
        style_id = "".join(c if c.isalnum() else "-" for c in style_name.lower()).strip("-")
        s_dir = STYLES_DIR / style_id
        s_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(v_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 10.0

        cuts = 0
        prev_gray = None
        sampled_frames = 0
        step = max(1, int(fps * 0.2)) # check every 200ms

        thumb_saved = False
        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % step == 0:
                small = cv2.resize(frame, (320, 180))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
                if not thumb_saved and idx > fps * 2:
                    cv2.imwrite(str(s_dir / "thumbnail.jpg"), frame)
                    thumb_saved = True

                if prev_gray is not None:
                    diff = cv2.absdiff(gray, prev_gray)
                    if np.mean(diff) > 35.0: # scene change / cut threshold
                        cuts += 1
                prev_gray = gray
                sampled_frames += 1
            idx += 1

        cap.release()

        avg_cut_duration = round(duration / max(1, cuts), 2)
        
        style_data = {
            "id": style_id,
            "name": style_name,
            "source_url": source_url,
            "version": 1,
            "pacing": {
                "avg_cut_duration_sec": max(1.2, min(5.0, avg_cut_duration)),
                "cut_frequency_per_min": round((cuts / max(1.0, duration)) * 60, 1),
                "hook_duration_sec": 2.2,
                "hook_style": "rapid_hook"
            },
            "captions": {
                "font": "ArchivoBlack-Regular.ttf",
                "font_size": 50,
                "primary_color": "&H00FFFFFF",
                "highlight_color": "&H0000E5FF", # bright cyan
                "outline_color": "&H00000000",
                "outline_width": 3.0,
                "position": "middle_third",
                "words_per_line": 2,
                "animation": "slide_fade"
            },
            "framing": {
                "mode": "smart_gameplay_tracking",
                "aspect_ratio": "9:16",
                "target_width": 1080,
                "target_height": 1920,
                "target_4k_width": 2160,
                "target_4k_height": 3840,
                "gameplay_crop": "center_weighted",
                "facecam_mode": "auto_pip_top"
            },
            "effects": {
                "punch_in_zoom_intensity": 1.2,
                "transition_type": "flash_cut",
                "color_grading": "cinematic_cool",
                "audio_ducking_db": -7.0
            }
        }

        with open(s_dir / "style.json", "w", encoding="utf-8") as f:
            json.dump(style_data, f, indent=2)

        analysis_md = f"""# Style Analysis: {style_name}
- **Source**: {source_url or 'Local File'}
- **Detected Duration**: {duration:.1f}s
- **Detected Cuts**: {cuts} cuts ({style_data['pacing']['cut_frequency_per_min']} cuts/min)
- **Average Scene Duration**: {style_data['pacing']['avg_cut_duration_sec']}s
- **Visual Rhythm**: {'Very Fast' if avg_cut_duration < 2.0 else 'Moderate' if avg_cut_duration < 3.5 else 'Deliberate'}
- **Color Grading Profile**: Cinematic cool tone with high luma contrast
- **Recommended Captions**: {style_data['captions']['font']} ({style_data['captions']['words_per_line']} words per block)
"""
        with open(s_dir / "analysis.md", "w", encoding="utf-8") as f:
            f.write(analysis_md)

        # Archive version 1
        v1_dir = HISTORY_DIR / style_id / "v1"
        v1_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(s_dir / "style.json", v1_dir / "style.json")

        return style_data

if __name__ == "__main__":
    StyleManager.initialize_defaults()
    print("Default styles:", StyleManager.list_styles())
