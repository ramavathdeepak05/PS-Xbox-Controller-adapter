@echo off
title Building Gamepad Adapter App
cd /d "%~dp0"

echo ========================================================
echo  Packaging Universal Gamepad Adapter into Standalone EXE
echo ========================================================
echo.

python -m PyInstaller --clean --onefile --noconsole --add-data "ui;ui" --hidden-import "webview" --hidden-import "clr" --name "GamepadAdapter" ps3_adapter.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  Build Successful!
    echo  The standalone application is in: dist\GamepadAdapter.exe
    echo ========================================================
) else (
    echo.
    echo [ERROR] Build failed. Please ensure Python and PyInstaller are installed.
)

pause
