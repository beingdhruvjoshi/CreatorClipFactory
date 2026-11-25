$json = curl.exe -s https://api.github.com/repos/xinntao/Real-ESRGAN-ncnn-vulkan/releases
$releases = $json | ConvertFrom-Json
$asset = $releases[0].assets | Where-Object { $_.name -like "*windows*.zip" } | Select-Object -First 1
Write-Host "Name: " $asset.name
Write-Host "URL: " $asset.browser_download_url

$dest = "C:\CreatorClipFactory\tools\realesrgan"
$zip = "C:\CreatorClipFactory\tools\realesrgan.zip"

curl.exe -L -o $zip $asset.browser_download_url
Expand-Archive -Path $zip -DestinationPath $dest -Force
Remove-Item $zip -Force

$exe = Join-Path $dest "realesrgan-ncnn-vulkan.exe"
if (Test-Path $exe) {
    Write-Host "SUCCESS: Real-ESRGAN installed at $exe"
    & $exe -h
} else {
    # Check if subfolder was created inside $dest
    $sub = Get-ChildItem -Path $dest -Filter "realesrgan-ncnn-vulkan.exe" -Recurse | Select-Object -First 1
    if ($sub) {
        Write-Host "Found in subfolder: $($sub.FullName)"
        # move contents up
        Get-ChildItem -Path $sub.DirectoryName | Move-Item -Destination $dest -Force
        & (Join-Path $dest "realesrgan-ncnn-vulkan.exe") -h
    }
}
