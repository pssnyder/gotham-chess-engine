@echo off
REM Gotham Chess Engine - Development Setup Script for Windows

echo 🔥 Setting up Gotham Chess Engine Web Platform...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js found!

REM Setup API dependencies
echo 📦 Installing API dependencies...
cd web\api
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install API dependencies
    pause
    exit /b 1
)
echo ✅ API dependencies installed

REM Setup frontend dependencies
echo 📦 Installing frontend dependencies...
cd ..\frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed

cd ..\..

echo ✅ Setup complete!
echo.
echo 🚀 To start development:
echo.
echo 1. Start the API server:
echo    cd web\api ^&^& python main.py
echo.
echo 2. In another terminal, start the frontend:
echo    cd web\frontend ^&^& npm start
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo 🔥 Happy coding!
pause