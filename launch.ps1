# Quick Shortcut AI - Launch Script
# PowerShell script to start the application

param(
    [switch]$NoConsole,
    [switch]$Debug
)

# Get the script directory
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Quick Shortcut AI - Launching Application" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found! Please install Python 3.10+" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if required packages are installed
Write-Host "`nChecking dependencies..." -ForegroundColor Yellow
python -c "import PySide6; import keyboard; import requests" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ Dependencies OK" -ForegroundColor Green

# Launch the application
Write-Host "`nStarting application..." -ForegroundColor Cyan

if ($Debug) {
    Write-Host "Debug mode: ON (verbose logging)" -ForegroundColor Yellow
    python -m src.main
}
elseif ($NoConsole) {
    Write-Host "Running in background (console will close)" -ForegroundColor Yellow
    Start-Process python -ArgumentList "-m src.main" -WindowStyle Hidden -NoNewWindow
    Write-Host "✓ Application started in background" -ForegroundColor Green
    Write-Host "  Check system tray for the icon" -ForegroundColor Yellow
    exit 0
}
else {
    Write-Host "Running with console (close console to stop app)" -ForegroundColor Yellow
    python -m src.main
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Application closed" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
