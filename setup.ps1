# GarimpoBot - Quick Setup (Windows)

Write-Host "Starting GarimpoBot setup..." -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Flutter
try {
    $flutterVersion = flutter --version 2>&1 | Select-String "Flutter"
    Write-Host "Flutter found" -ForegroundColor Green
    $FLUTTER_AVAILABLE = $true
} catch {
    Write-Host "Flutter not found. Frontend setup will be skipped." -ForegroundColor Yellow
    $FLUTTER_AVAILABLE = $false
}

Write-Host ""
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
playwright install chromium

Write-Host ""
Write-Host "Backend ready." -ForegroundColor Green
Write-Host ""

if ($FLUTTER_AVAILABLE) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Set-Location frontend
    flutter pub get
    Set-Location ..
    Write-Host ""
    Write-Host "Frontend ready." -ForegroundColor Green
    Write-Host ""
}

Write-Host "Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Start backend:" -ForegroundColor Cyan
Write-Host "  python run.py --mode api"
Write-Host ""

if ($FLUTTER_AVAILABLE) {
    Write-Host "Start frontend:" -ForegroundColor Cyan
    Write-Host "  cd frontend; flutter run -d chrome"
    Write-Host ""
}

Write-Host "Read QUICKSTART.md for more info." -ForegroundColor Yellow
