$src = "C:\Users\acer\AppData\Local\Microsoft\WinGet\Packages\Ollama.Ollama.Portable_Microsoft.Winget.Source_8wekyb3d8bbwe"
$dest = "C:\CreatorClipFactory\tools\ollama"

if (-not (Test-Path "$dest\ollama.exe")) {
    Write-Host "Copying Ollama portable to $dest..."
    Copy-Item -Path $src -Destination $dest -Recurse -Force
}

$ollamaExe = "$dest\ollama.exe"
Write-Host "Verifying Ollama binary at $ollamaExe..."
& $ollamaExe --version
