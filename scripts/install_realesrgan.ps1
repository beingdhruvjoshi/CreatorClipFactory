$releaseUrl = "https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/download/v0.2.0/realesrgan-ncnn-vulkan-20220424-windows.zip"
$dest = "C:\CreatorClipFactory\tools\realesrgan"
$zip = "C:\CreatorClipFactory\tools\realesrgan.zip"

if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
}

Write-Host "Downloading Real-ESRGAN NCNN Vulkan from $releaseUrl..."
Invoke-WebRequest -Uri $releaseUrl -OutFile $zip

Write-Host "Extracting Real-ESRGAN NCNN Vulkan..."
Expand-Archive -Path $zip -DestinationPath $dest -Force
Remove-Item $zip -Force

Write-Host "Verifying executable..."
$exe = Join-Path $dest "realesrgan-ncnn-vulkan.exe"
if (Test-Path $exe) {
    Write-Host "Real-ESRGAN NCNN Vulkan installed successfully at $exe"
    & $exe -h
} else {
    Write-Error "realesrgan-ncnn-vulkan.exe not found!"
}
