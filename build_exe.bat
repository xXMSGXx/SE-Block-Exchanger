@echo off
echo ===================================================
echo  Space Engineers Block Exchanger - Build Script
echo ===================================================

for /f %%i in ('python -c "from version import __version__; print(__version__)"') do set APP_VERSION=%%i

echo.
echo [1/4] Installing Build Dependencies...
pip install pyinstaller

echo.
echo [2/4] Converting Icon (if needed)...
if not exist "app_icon.ico" (
    if exist "logo.png" (
        pip install Pillow
        python convert_icon.py
    ) else (
        echo WARNING: No logo.png found. Building without icon.
    )
)

echo.
echo [3/4] Building Executable...
echo This may take a few minutes...

if exist "app_icon.ico" (
    pyinstaller --noconfirm --onefile --windowed ^
        --name "SE_Tactical_Command_v%APP_VERSION%" ^
        --icon "app_icon.ico" ^
        --add-data "README.md;." ^
        --add-data "LICENSE;." ^
        --add-data "RELEASE_NOTES.md;." ^
        --add-data "profiles;profiles" ^
        --add-data "data;data" ^
        --add-data "app_icon.ico;." ^
        gui_standalone.py
) else (
    pyinstaller --noconfirm --onefile --windowed ^
        --name "SE_Tactical_Command_v%APP_VERSION%" ^
        --icon "NONE" ^
        --add-data "README.md;." ^
        --add-data "LICENSE;." ^
        --add-data "RELEASE_NOTES.md;." ^
        --add-data "profiles;profiles" ^
        --add-data "data;data" ^
        gui_standalone.py
)

echo.
echo [4/4] Build Complete!
echo.
echo The executable is located in the 'dist' folder.
echo.
pause
