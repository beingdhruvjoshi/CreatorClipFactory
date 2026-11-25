# CreatorClip Factory - Health Check Script
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " CREATORCLIP FACTORY - SYSTEM HEALTH CHECK" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$status = @{
    AllPassed = $true
    Items = @()
}

function Check-Item ($name, $testBlock) {
    Write-Host -NoNewline "Checking $name... "
    try {
        $result = & $testBlock
        if ($result -eq $true -or $null -eq $result) {
            Write-Host "[OK]" -ForegroundColor Green
            $script:status.Items += [PSCustomObject]@{ Item = $name; Status = "OK" }
        } else {
            Write-Host "[FAIL] - $result" -ForegroundColor Red
            $script:status.AllPassed = $false
            $script:status.Items += [PSCustomObject]@{ Item = $name; Status = "FAIL"; Message = $result }
        }
    } catch {
        Write-Host "[ERROR] - $($_.Exception.Message)" -ForegroundColor Red
        $script:status.AllPassed = $false
        $script:status.Items += [PSCustomObject]@{ Item = $name; Status = "ERROR"; Message = $_.Exception.Message }
    }
}

# 1. Hardware & GPU
Check-Item "NVIDIA GPU (nvidia-smi)" {
    $out = & nvidia-smi --query-gpu=name,memory.free --format=csv,noheader,nounits 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host -NoNewline "($out) "
        return $true
    }
    return "nvidia-smi not available"
}

# 2. Python Environment
Check-Item "Python Virtual Environment" {
    $py = "C:\CreatorClipFactory\venv\Scripts\python.exe"
    if (Test-Path $py) {
        $ver = & $py --version 2>&1
        Write-Host -NoNewline "($ver) "
        return $true
    }
    return "Virtual environment not found at $py"
}

# 3. FFmpeg & FFprobe
Check-Item "FFmpeg & FFprobe" {
    $ff = "C:\Users\acer\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
    if (Test-Path $ff) {
        $v = & $ff -version | Select-Object -First 1
        Write-Host -NoNewline "($v) "
        return $true
    }
    return "FFmpeg not found"
}

# 4. Ollama Local AI & Models
Check-Item "Ollama Local AI API" {
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5
    $models = $res.models | ForEach-Object { $_.name }
    Write-Host -NoNewline "([$($models -join ', ')]) "
    if ($models -contains "qwen2.5:1.5b") {
        return $true
    }
    return "Required model qwen2.5:1.5b not found in Ollama"
}

# 5. Real-ESRGAN NCNN Vulkan
Check-Item "Real-ESRGAN NCNN Vulkan" {
    $exe = "C:\CreatorClipFactory\tools\realesrgan\realesrgan-ncnn-vulkan.exe"
    if (Test-Path $exe) {
        return $true
    }
    return "Real-ESRGAN executable not found"
}

# 6. Database
Check-Item "SQLite Factory Database" {
    $db = "C:\CreatorClipFactory\database\factory.db"
    if (Test-Path $db) {
        $py = "C:\CreatorClipFactory\venv\Scripts\python.exe"
        $res = & $py -c "import sqlite3; c = sqlite3.connect(r'$db'); print(c.execute('SELECT count(*) FROM sqlite_master').fetchone()[0])"
        Write-Host -NoNewline "($res tables) "
        return $true
    }
    return "Database file not found"
}

# 7. Cloned Repositories
Check-Item "PeakCut & Video Skills Repositories" {
    $pc = "C:\CreatorClipFactory\core\peakcut\.git"
    $vs = "C:\CreatorClipFactory\skills\video-editing-skills\.git"
    if ((Test-Path $pc) -and (Test-Path $vs)) {
        return $true
    }
    return "One or more git repositories missing"
}

Write-Host "-----------------------------------------" -ForegroundColor Cyan
if ($status.AllPassed) {
    Write-Host "HEALTH CHECK RESULT: ALL SYSTEMS OPERATIONAL" -ForegroundColor Green
    Exit 0
} else {
    Write-Host "HEALTH CHECK RESULT: DEGRADED / ISSUES FOUND" -ForegroundColor Yellow
    Exit 1
}
