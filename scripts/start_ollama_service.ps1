$dest = "C:\CreatorClipFactory\tools\ollama"
$ollamaExe = "$dest\ollama.exe"

$running = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $running) {
    Write-Host "Starting Ollama service..."
    $env:OLLAMA_MODELS = "C:\CreatorClipFactory\models\ollama"
    if (-not (Test-Path $env:OLLAMA_MODELS)) {
        New-Item -ItemType Directory -Path $env:OLLAMA_MODELS -Force | Out-Null
    }
    Start-Process -FilePath $ollamaExe -ArgumentList "serve" -WorkingDirectory $dest -WindowStyle Hidden
    Start-Sleep -Seconds 4
} else {
    Write-Host "Ollama service is already running."
}

# Test connection
try {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
    Write-Host "Ollama is responding at http://127.0.0.1:11434"
    Write-Host "Models installed:" ($res.models | ForEach-Object { $_.name })
} catch {
    Write-Host "Waiting for Ollama to initialize..."
    Start-Sleep -Seconds 3
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
    Write-Host "Ollama is responding at http://127.0.0.1:11434"
}
