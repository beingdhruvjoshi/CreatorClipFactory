$ollamaDir = "C:\CreatorClipFactory\tools\ollama"
$env:PATH = "$ollamaDir;" + $env:PATH
Set-Location $ollamaDir

Write-Host "Pulling qwen2.5:1.5b..."
& "$ollamaDir\ollama.exe" pull qwen2.5:1.5b

Write-Host "Checking installed models..."
& "$ollamaDir\ollama.exe" list

