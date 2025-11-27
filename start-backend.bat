@echo off
REM FastAPI Backend Startup Script
REM This script ensures uvicorn runs from the correct directory

echo ========================================
echo   Starting FastAPI Backend Server
echo ========================================
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in backend directory!
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if virtual environment exists and activate it (optional)
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\venv\Scripts\activate.bat"
)

echo Starting uvicorn from: %CD%
echo.
echo Server will be available at: http://127.0.0.1:8000
echo API docs will be available at: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Start uvicorn
uvicorn main:app --reload

