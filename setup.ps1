# CreatorClip Factory - Setup & Configuration Script
Write-Host "Configuring CreatorClip Factory runtime..." -ForegroundColor Cyan

# Ensure DB is created
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\core\db_manager.py

# Ensure Styles are initialized
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\core\style_library.py

# Ensure Antigravity skills are in workspace
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\scripts\generate_skills.py

Write-Host "CreatorClip Factory configured successfully." -ForegroundColor Green
