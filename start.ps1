# CreatorClip Factory - Launch System Script
Write-Host "=========================================" -ForegroundColor Green
Write-Host " LAUNCHING CREATORCLIP FACTORY SERVICES  " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# 1. Start Ollama if not running
$ollamaProc = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaProc) {
    Write-Host "Starting Ollama Local AI Service..."
    $dest = "C:\CreatorClipFactory\tools\ollama"
    $env:OLLAMA_MODELS = "C:\CreatorClipFactory\models\ollama"
    Start-Process -FilePath "$dest\ollama.exe" -ArgumentList "serve" -WorkingDirectory $dest -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "Ollama service is active." -ForegroundColor Green
}

# 2. Start Dashboard & Orchestrator Supervisor
Write-Host "Starting Dashboard & Background Supervisor..."
$py = "C:\CreatorClipFactory\venv\Scripts\python.exe"
$env:PYTHONPATH = "C:\CreatorClipFactory"

$dashJob = Start-Process -FilePath $py -ArgumentList "-m uvicorn dashboard.app:app --app-dir C:\CreatorClipFactory --host 127.0.0.1 --port 8000" -WorkingDirectory "C:\CreatorClipFactory" -PassThru -WindowStyle Hidden

Write-Host "-----------------------------------------" -ForegroundColor Green
Write-Host " CreatorClip Factory is LIVE!" -ForegroundColor Cyan
Write-Host " Local Dashboard URL: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host " Process ID: $($dashJob.Id)"
Write-Host " To stop services, run .\stop.ps1"
Write-Host "-----------------------------------------" -ForegroundColor Green
