@echo off
echo ===================================================
echo  Space Engineers Block Exchanger - Build Script
echo ===================================================

echo.
echo [1/3] Installing Build Dependencies...
pip install pyinstaller

echo.
echo [2/3] Building Executable...
echo This may take a few minutes...

pyinstaller --noconfirm --onefile --windowed ^
    --name "SE_Tactical_Command" ^
    --icon "NONE" ^
    --add-data "README.md;." ^
    --add-data "LICENSE;." ^
    gui_standalone.py

echo.
echo [3/3] Build Complete!
echo.
echo The executable is located in the 'dist' folder.
echo.
pause
