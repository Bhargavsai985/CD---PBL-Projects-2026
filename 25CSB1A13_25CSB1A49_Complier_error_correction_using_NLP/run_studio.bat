@echo off
cd /d "%~dp0"
echo ========================================================
echo   Starting CompilerAI / INTELLIFIX Optimization Studio
echo ========================================================
echo.

set "PYPATH=%LocalAppData%\Programs\Python\Python315\python.exe"

if exist "%PYPATH%" (
    echo Using Python from: %PYPATH%
    "%PYPATH%" app.py
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        python app.py
    ) else (
        echo Python path not detected. Opening index.html directly in browser...
        start "" index.html
    )
)

pause
