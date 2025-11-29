@echo off
REM Space Engineers Block Exchanger - Standalone GUI Launcher
REM Double-click this file to launch the tactical command center

echo ========================================
echo SE BLOCK EXCHANGER - TACTICAL COMMAND CENTER
echo ========================================
echo.
echo Launching standalone application...
echo.

REM Activate virtual environment and launch GUI
call .venv\Scripts\activate.bat
python gui_standalone.py

pause
