@echo off
echo ========================================
echo   CyberSuite - Penetration Testing Suite
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Starting CyberSuite...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
)
