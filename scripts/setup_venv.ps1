$python = "C:\Users\acer\AppData\Local\Programs\Python\Python311\python.exe"
$venvDir = "C:\CreatorClipFactory\venv"

if (-not (Test-Path "$venvDir\Scripts\python.exe")) {
    Write-Host "Creating virtual environment at $venvDir..."
    & $python -m venv $venvDir
} else {
    Write-Host "Virtual environment already exists."
}

$venvPython = "$venvDir\Scripts\python.exe"
$venvPip = "$venvDir\Scripts\pip.exe"

Write-Host "Upgrading pip..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing PeakCut and CreatorClipFactory dependencies..."
$pkgs = @(
    "fastapi>=0.110.0",
    "uvicorn>=0.28.0",
    "httpx>=0.27.0",
    "numpy>=1.26.0",
    "SQLAlchemy>=2.0.0",
    "python-multipart>=0.0.9",
    "yt-dlp>=2024.0.0",
    "pillow>=10.0.0",
    "soundfile>=0.12.0",
    "opencv-python>=4.8.0",
    "requests>=2.31.0",
    "jinja2>=3.1.0",
    "aiofiles>=23.2.0",
    "pydantic>=2.6.0",
    "psutil>=5.9.0",
    "google-api-python-client>=2.100.0",
    "google-auth-oauthlib>=1.2.0",
    "google-auth-httplib2>=0.2.0"
)

& $venvPip install $pkgs

Write-Host "Verifying installed packages..."
& $venvPython -c "import fastapi, uvicorn, cv2, numpy, sqlalchemy, yt_dlp, PIL, psutil; print('All core dependencies imported successfully!')"
