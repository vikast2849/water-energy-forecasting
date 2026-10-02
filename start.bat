@echo off
title Population-Driven Water and Energy Demand Forecasting
cd /d "%~dp0"

echo ==================================================================
echo   Starting Water and Energy Demand Forecasting Framework
echo   Dept. of CSE, SJMIT Chitradurga (2026-2027)
echo   Models: SVM, KNN, and Logistic Regression
echo ==================================================================
echo.
echo   [1/2] Launching Web Browser at http://127.0.0.1:5000 in 2 seconds...
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

echo   [2/2] Starting Flask Web Server...
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python run.py
) else (
    if exist "C:\Python314\python.exe" (
        "C:\Python314\python.exe" run.py
    ) else (
        echo [ERROR] Python was not found on your system.
        pause
    )
)

if %errorlevel% neq 0 (
    echo.
    echo Server exited with an error.
    pause
)
