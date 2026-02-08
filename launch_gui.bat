@echo off
REM Space Engineers Block Exchanger - Standalone GUI Launcher
REM Double-click this file to launch the tactical command center

echo ========================================
echo SE BLOCK EXCHANGER - TACTICAL COMMAND CENTER
echo ========================================
echo.
echo Launching standalone application...
echo.

REM Try virtual environment first, fall back to system Python
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

python gui_standalone.py

pause
