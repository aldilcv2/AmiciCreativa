@echo off
:: Launcher for Portfolio GUI Manager (Windows)

echo Starting Portfolio Manager...

:: Check if Python is accessible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in PATH.
    echo Please install Python from https://python.org and make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

:: Run the application
venv\Scripts\python.exe gui_app.py

if %errorlevel% neq 0 (
    echo.
    echo An error occurred. If the error is "ModuleNotFoundError: No module named 'tkinter'",
    echo please make sure you installed Python with "tcl/tk and IDLE" option checked.
    pause
)
