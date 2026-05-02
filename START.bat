@echo off
REM Quick Start Script for FinAgent-Rec (Windows)
REM This script sets up and guides you through starting both servers

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo.
echo   FinAgent-Rec: Multi-Agent Financial Recommendations
echo.
echo ========================================================
echo.

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node exists
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 14+
    pause
    exit /b 1
)

REM Check if npm exists
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm not found. Please install npm
    pause
    exit /b 1
)

echo [OK] Python found: 
python --version

echo [OK] Node.js found:
node --version

echo [OK] npm found:
npm --version

echo.
echo Setting up Python environment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [OK] Virtual environment activated

echo.
echo Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo [OK] Python dependencies installed

echo.
echo Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing npm packages (this may take a moment)...
    call npm install >nul 2>&1
)

echo [OK] Frontend ready
cd ..

echo.
echo ========================================================
echo.
echo   System Ready!
echo.
echo ========================================================
echo.
echo To start the system, open TWO command prompts:
echo.
echo [Terminal 1] Backend API:
echo   python api.py
echo   Opens on http://localhost:5000
echo.
echo [Terminal 2] Frontend:
echo   cd frontend
echo   npm start
echo   Opens on http://localhost:3000
echo.
echo Then open your browser to: http://localhost:3000
echo.
echo Documentation:
echo   - Quick Start: QUICK_REFERENCE.md
echo   - Full Setup: FRONTEND_SETUP.md
echo   - Deployment: FRONTEND_DEPLOYMENT.md
echo   - All Docs: DOCUMENTATION_INDEX.md
echo.
echo ========================================================
echo.

pause
