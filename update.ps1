# CreatorClip Factory - Update Repositories Script
Write-Host "Updating CreatorClip Factory repositories..." -ForegroundColor Cyan

$git = "C:\CreatorClipFactory\tools\git\cmd\git.exe"

# PeakCut
if (Test-Path "C:\CreatorClipFactory\core\peakcut\.git") {
    Write-Host "Updating PeakCut..."
    Push-Location "C:\CreatorClipFactory\core\peakcut"
    & $git pull
    Pop-Location
}

# Video editing skills
if (Test-Path "C:\CreatorClipFactory\skills\video-editing-skills\.git") {
    Write-Host "Updating video-editing-skills..."
    Push-Location "C:\CreatorClipFactory\skills\video-editing-skills"
    & $git pull
    Pop-Location
}

# Record updated commits
& powershell -ExecutionPolicy Bypass -File "C:\CreatorClipFactory\scripts\clone_repos.ps1"

# Regenerate skills
& C:\CreatorClipFactory\venv\Scripts\python.exe C:\CreatorClipFactory\scripts\generate_skills.py

Write-Host "CreatorClip Factory updated successfully." -ForegroundColor Green
