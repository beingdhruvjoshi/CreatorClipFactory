$git = "C:\CreatorClipFactory\tools\git\cmd\git.exe"

Write-Host "Cloning PeakCut..."
$peakcutDir = "C:\CreatorClipFactory\core\peakcut"
if (-not (Test-Path "$peakcutDir\.git")) {
    & $git clone https://github.com/haziqahmedqasmi/peakcut.git $peakcutDir
} else {
    Write-Host "PeakCut already cloned."
}

Write-Host "Cloning video-editing-skills..."
$skillsDir = "C:\CreatorClipFactory\skills\video-editing-skills"
if (-not (Test-Path "$skillsDir\.git")) {
    & $git clone https://github.com/zaddy99999/video-editing-skills.git $skillsDir
} else {
    Write-Host "video-editing-skills already cloned."
}

# Record commit hashes
$hashes = @{}
if (Test-Path "$peakcutDir\.git") {
    Push-Location $peakcutDir
    $hashes["peakcut"] = (& $git rev-parse HEAD).Trim()
    Pop-Location
}
if (Test-Path "$skillsDir\.git") {
    Push-Location $skillsDir
    $hashes["video_editing_skills"] = (& $git rev-parse HEAD).Trim()
    Pop-Location
}

$hashFile = "C:\CreatorClipFactory\config\installed_commits.json"
$hashes | ConvertTo-Json -Depth 4 | Out-File -FilePath $hashFile -Encoding utf8
Write-Host "Installed repository commits:"
Get-Content $hashFile
