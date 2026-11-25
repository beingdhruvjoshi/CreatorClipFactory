import re
import json
from pathlib import Path
from typing import List, Dict, Any

vtt_path = Path("C:/CreatorClipFactory/analysis/izXcd.en.vtt")

def parse_vtt_timestamp(ts: str) -> float:
    parts = ts.strip().split(":")
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    return 0.0

def analyze_transcript() -> List[Dict[str, Any]]:
    with open(vtt_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Matches cue blocks: 00:01:23.456 --> 00:01:26.789 align:...
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})[^\n]*\n(.*?)(?=\n\d{2}:\d{2}:\d{2}|\Z)", re.DOTALL)
    
    cues = []
    for m in pattern.finditer(text):
        start_ts, end_ts, content = m.groups()
        start_s = parse_vtt_timestamp(start_ts)
        end_s = parse_vtt_timestamp(end_ts)
        cleaned = re.sub(r"<[^>]+>", "", content).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if cleaned:
            cues.append({"start": start_s, "end": end_s, "text": cleaned})

    print(f"Parsed {len(cues)} speech cues.")

    # High virality keyword weights
    high_energy_keywords = {
        "oh my god": 15, "no way": 15, "what the": 12, "holy": 12,
        "look at this": 14, "look at that": 14, "what is that": 12,
        "easter egg": 16, "secret": 14, "vice city": 12, "gta 6": 12,
        "police": 12, "cops": 12, "chase": 14, "run": 10,
        "crash": 15, "explosion": 16, "explode": 15, "dead": 10, "died": 10,
        "bro": 8, "watch this": 14, "are you serious": 14, "insane": 15,
        "crazy": 12, "fast": 10, "omg": 15, "yo": 6
    }

    # Evaluate 30-second sliding windows (every 10s step)
    max_time = cues[-1]["end"] if cues else 20700.0
    windows = []
    
    # We step every 15 seconds
    t = 120.0 # start at 2 mins (skip intro screen)
    while t + 30.0 < max_time - 60.0:
        win_start = t
        win_end = t + 30.0
        
        # Collect cues in this window
        win_cues = [c for c in cues if (c["start"] >= win_start and c["start"] <= win_end) or (c["end"] >= win_start and c["end"] <= win_end)]
        combined_text = " ".join(c["text"] for c in win_cues).lower()
        word_count = len(combined_text.split())
        
        score = 0.0
        reasons = []
        for kw, wt in high_energy_keywords.items():
            if kw in combined_text:
                score += wt
                reasons.append(kw)

        # Reward high speech rate (fast exciting reaction)
        if word_count > 45: # > 1.5 words per sec
            score += 15
            reasons.append(f"rapid exciting commentary ({word_count} words/30s)")
        elif word_count > 30:
            score += 8

        if score > 20:
            windows.append({
                "start": round(win_start, 1),
                "end": round(win_end, 1),
                "duration": 30.0,
                "score": round(score, 1),
                "reasons": reasons,
                "sample_text": combined_text[:120] + "..."
            })
        t += 15.0

    print(f"Found {len(windows)} candidate windows.")
    
    # Sort by score descending
    windows.sort(key=lambda x: x["score"], reverse=True)

    # Select top 5 non-overlapping (at least 300s / 5 mins apart for variety)
    top5 = []
    for w in windows:
        overlap = False
        for s in top5:
            if abs(w["start"] - s["start"]) < 300.0:
                overlap = True
                break
        if not overlap:
            w["rank"] = len(top5) + 1
            top5.append(w)
            if len(top5) == 5:
                break

    return top5

if __name__ == "__main__":
    top5 = analyze_transcript()
    print("\n--- TOP 5 IDENTIFIED VIRAL 30-SEC HIGH-ENERGY SEGMENTS ---")
    for s in top5:
        m, sec = divmod(int(s["start"]), 60)
        h, m = divmod(m, 60)
        ts_str = f"{h:02d}:{m:02d}:{sec:02d}"
        print(f"#{s['rank']} | Timestamp: {ts_str} ({s['start']}s - {s['end']}s) | Score: {s['score']}")
        print(f"    Reasons: {s['reasons']}")
        print(f"    Dialogue: \"{s['sample_text']}\"\n")

    # Save to JSON
    with open("C:/CreatorClipFactory/analysis/top5_segments.json", "w", encoding="utf-8") as f:
        json.dump(top5, f, indent=2)
