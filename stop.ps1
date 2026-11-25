# CreatorClip Factory - Stop Services Script
Write-Host "Stopping CreatorClip Factory services..." -ForegroundColor Yellow

# Stop uvicorn dashboard processes
Get-Process | Where-Object { $_.CommandLine -like "*dashboard.app:app*" -or $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Stop background ffmpeg or realesrgan if any running
Get-Process -Name "realesrgan-ncnn-vulkan" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "CreatorClip Factory services stopped successfully." -ForegroundColor Green
