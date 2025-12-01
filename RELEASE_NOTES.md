# Release Notes

## v1.0.0 - Initial Release (November 2025)

### 🎉 Welcome to SE Block Exchanger!

The **Space Engineers Block Exchanger** is a powerful Python tool designed to automate armor block conversions in Space Engineers blueprints. Save hours of tedious manual work by converting entire blueprints in seconds!

---

### ✨ New Features

#### 🔄 Bidirectional Armor Conversion
- **Light → Heavy**: Convert light armor blocks to heavy armor variants for increased durability
- **Heavy → Light**: Convert heavy armor blocks to light armor variants to save resources
- Toggle conversion direction with a single click in the GUI or `--reverse` flag in CLI

#### 🖥️ Standalone Desktop Application
- Native Windows desktop application using tkinter
- **Tactical Hologram Interface** with military-grade styling:
  - Gunmetal grey and neon cyan/orange color scheme
  - Tech-glass panel effects
  - Corner bracket targeting system aesthetic
- **Blueprint Database Panel** with search and scrollable list
- **Real-time Block Analysis** showing light/heavy armor counts
- **Exchange Visualization** with before/after block display
- Threaded operations for responsive UI during scanning/conversion

#### 💻 Command Line Interface
- Full-featured CLI for automation and scripting
- Process single blueprints or entire directories
- Verbose output mode for detailed logging
- List all supported block mappings with `--list-mappings`

#### 🛡️ Safe & Non-Destructive
- **Automatic Backup Creation** - Creates `.sbc.backup` files before modification (CLI)
- **Prefix-Based Copies** - GUI creates new blueprints with `HEAVYARMOR_` or `LIGHTARMOR_` prefixes
- **Original Preservation** - Source blueprints are never modified

#### 📦 Comprehensive Block Support
- **60+ armor block types** supported
- **Large Grid Blocks**:
  - Standard blocks (cube, slope, corner, inverted corner)
  - Round armor variants
  - 2x1 slopes and corners (base and tip)
  - Half blocks and slopes
  - Armor panels
  - Sloped corners
- **Small Grid Blocks**:
  - All corresponding small grid variants

---

### 🔧 Technical Details

#### Dependencies
- **Python 3.7+** required
- **No external packages** - Uses Python standard library only
- GUI uses built-in `tkinter` module

#### File Structure
| File | Description |
|------|-------------|
| `se_armor_replacer.py` | Core armor replacement logic and CLI |
| `gui_standalone.py` | Standalone desktop GUI application |
| `blueprint_scanner.py` | Blueprint directory scanner and metadata extractor |
| `blueprint_converter.py` | Safe blueprint copying and conversion |
| `launch_gui.bat` | Windows launcher for GUI |
| `test_armor_replacer.py` | Comprehensive unit test suite |

#### Supported Platforms
- **Windows** - Full support (native paths, GUI, CLI)
- **Linux/Mac** - CLI support (GUI may require tkinter installation)

---

### 📋 Usage Quick Start

#### GUI (Recommended)
```bash
# Windows - Double-click launch_gui.bat or run:
python gui_standalone.py
```

#### Command Line
```bash
# Light to Heavy conversion
python se_armor_replacer.py path/to/blueprint/bp.sbc

# Heavy to Light conversion
python se_armor_replacer.py path/to/blueprint/bp.sbc --reverse

# List all supported block mappings
python se_armor_replacer.py --list-mappings
```

---

### 🧪 Testing

The project includes a comprehensive test suite with 11 unit tests covering:
- Light to heavy block replacement
- Heavy to light block replacement (reverse mode)
- Mixed block processing
- Backup file creation
- Output file generation
- All armor type mappings validation

Run tests with:
```bash
python -m unittest test_armor_replacer -v
```

---

### 📍 Blueprint Locations

**Windows Local Blueprints:**
```
%APPDATA%\SpaceEngineers\Blueprints\local\<BlueprintName>\bp.sbc
```

**Steam Workshop:**
```
C:\Program Files (x86)\Steam\steamapps\workshop\content\244850\<WorkshopID>\bp.sbc
```

---

### ⚠️ Known Limitations

- Only processes blueprint files (`bp.sbc`), not world saves
- Does not modify paint colors or skin settings
- Does not adjust component costs (handled by Space Engineers)
- Requires manual reload in Space Engineers to see changes

---

### 🚀 Perfect For

- 🛡️ Converting survival blueprints to combat-ready heavy armor
- 🏗️ Upgrading old designs without rebuilding from scratch
- ⚔️ Preparing fleet ships for PvP battles
- 💰 Downgrading expensive heavy armor ships to save resources
- 🔄 Testing designs with different armor types quickly
- 📦 Batch processing entire blueprint libraries

---

### 📜 License

**Copyright © 2025. All Rights Reserved.**

This software is provided for **personal use only**. See the LICENSE file for complete terms.

---

### 🙏 Credits

Created for the Space Engineers community to simplify blueprint modifications.

---

*For feature requests, bug reports, or contributions, please open an issue or pull request on the project repository.*
