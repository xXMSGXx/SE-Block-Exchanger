# Installation and Build Guide

## Running from Source
1. Install Python 3.10+ (tkinter is bundled with the official installer)
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Run the application:
   ```bash
   python gui_standalone.py
   ```

## Building Standalone Executable
To create a single `.exe` file that can be shared with other users (no Python installation required):

1. Double-click `build_exe.bat`
   OR
2. Run the following command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "SE_Tactical_Command" gui_standalone.py
   ```

The resulting `SE_Tactical_Command.exe` will be found in the `dist` folder.
