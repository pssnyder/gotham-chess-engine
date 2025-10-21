@echo off
REM Simple UCI Test for Arena Chess GUI
REM This file starts a basic UCI engine that should work with Arena

echo Starting Simple Gotham Chess Engine UCI Interface...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ to use this engine
    pause
    exit /b 1
)

REM Set the working directory to the engine location
cd /d "%~dp0"

REM Run the simple UCI engine
python simple_uci.py

pause