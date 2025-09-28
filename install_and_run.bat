@echo off
echo Installing AI Image Metadata Tool for Civitai...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found, installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Try running this script as Administrator
    pause
    exit /b 1
)

echo.
echo Installation complete! Starting the application...
echo.
python simple_ai_metadata_tool.py

pause
