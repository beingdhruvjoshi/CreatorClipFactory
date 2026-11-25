# CreatorClip Factory - Full Installation Script
Write-Host "Starting CreatorClip Factory Automated Installation..." -ForegroundColor Green

# 1. Directory Structure
Write-Host "[1/6] Initializing Directory Hierarchy..."
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\init_dirs.ps1

# 2. Repositories
Write-Host "[2/6] Cloning Locked Repositories (PeakCut, video-editing-skills)..."
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\clone_repos.ps1

# 3. Virtual Environment & Dependencies
Write-Host "[3/6] Setting up Python Virtual Environment & Packages..."
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\setup_venv.ps1

# 4. Ollama & Models
Write-Host "[4/6] Setting up Local Ollama Runtime & Models..."
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\setup_ollama.ps1
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\start_ollama_service.ps1

# 5. Real-ESRGAN NCNN Vulkan
Write-Host "[5/6] Verifying Real-ESRGAN NCNN Vulkan..."
& powershell -ExecutionPolicy Bypass -File C:\CreatorClipFactory\scripts\get_realesrgan.ps1

# 6. Antigravity Skills & Database
Write-Host "[6/6] Generating Antigravity Skills & Database Schemas..."
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\core\db_manager.py
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\core\style_library.py
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\scripts\generate_skills.py

Write-Host "Installation completed! Run .\health-check.ps1 to verify or .\start.ps1 to launch." -ForegroundColor Green
