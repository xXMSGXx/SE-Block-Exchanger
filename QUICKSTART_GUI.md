# Space Engineers Block Exchanger - Quick Start Guide

## Standalone Desktop Application (Recommended)

The fastest way to convert your blueprints!

### Launch

**Option 1: Double-click**
- Double-click `launch_gui.bat`

**Option 2: Command line**
```bash
python gui_standalone.py
```

### Using the Tactical Command Center

1. **Wait for scan to complete**
   - Application automatically scans your Space Engineers blueprints
   - Status shown in header and footer

2. **Select a blueprint**
   - Browse the list on the left panel
   - Use the search box to filter by name
   - Click to select

3. **Review details**
   - Right panel shows selected blueprint info
   - Grid size, block counts, light armor blocks
   - Exchange visualization shows before/after

4. **Convert**
   - Click `[ INITIATE HEAVY ARMOR CONVERSION ]`
   - Confirm the operation
   - Wait for completion message

5. **Result**
   - New blueprint created: `HEAVYARMOR_OriginalName`
   - Original blueprint untouched
   - Stats updated in footer

### Interface Guide

**Left Panel - Blueprint Database**
- Search box at top
- Scrollable blueprint list
- Shows name, grid size, light armor count

**Right Panel - Control Center**
- Top: Selected blueprint details
- Middle: Exchange visualization (Standard → Heavy)
- Bottom: Conversion button (only enabled if light armor present)

**Header Bar**
- System status indicator (green dot)
- Blueprint count
- Rescan button

**Footer Bar**
- Current operation status
- Blueprints scanned counter
- Blueprints converted counter
- Version info

### Keyboard Shortcuts

- **Up/Down arrows**: Navigate blueprint list
- **Enter**: Select highlighted blueprint
- **F5 or Ctrl+R**: Rescan blueprints

### Troubleshooting

**No blueprints found?**
- Check that Space Engineers is installed
- Default path: `%APPDATA%\SpaceEngineers\Blueprints\local`
- Application scans this automatically

**Application won't start?**
- Requires Python 3.7+
- Tkinter is included with Python
- Try: `python --version` to verify Python installation

**Conversion failed?**
- Ensure original blueprint file is not open/locked
- Check that you have write permissions
- Check status bar for error details

### Features

✅ No web browser required
✅ Native Windows application
✅ No additional dependencies (uses Python standard library)
✅ Automatic blueprint scanning
✅ Safe conversion (original preserved)
✅ Real-time status updates
✅ Tactical hologram aesthetic
✅ Fast and lightweight

### Support

For issues or questions, check:
- README.md for detailed documentation
- PROJECT_SUMMARY.md for technical overview
- test_armor_replacer.py for example usage
