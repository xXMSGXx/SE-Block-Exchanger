# Space Engineers Armor Block Replacer

A Python tool to automatically scan Space Engineers blueprint files and replace all light armor blocks with their heavy armor variants.

## 🎯 Why Use This Tool?

**Save Hours of Tedious Manual Work!**

Converting light armor to heavy armor in Space Engineers is painful:
- ❌ Manually replacing hundreds or thousands of blocks takes **hours**
- ❌ Easy to miss blocks hidden inside your ship
- ❌ Risk of structural mistakes during manual conversion
- ❌ No way to batch convert multiple blueprints

**This tool does it all automatically in seconds:**
- ✅ Converts **entire blueprints instantly** (even 1000+ block ships)
- ✅ **100% accurate** - finds every light armor block automatically
- ✅ **Completely safe** - creates new blueprints, never modifies originals
- ✅ **Zero game downtime** - works on blueprint files while you play
- ✅ **Batch processing** - convert your entire blueprint library at once

**Perfect for:**
- 🚀 Converting survival blueprints to combat-ready heavy armor
- 🏗️ Upgrading old designs without rebuilding from scratch
- ⚔️ Preparing fleet ships for PvP battles
- 🔄 Testing designs with different armor types quickly

## ✨ Two Ways to Use

### 🖥️ Standalone Desktop App (Recommended!)
Native Windows application with tactical hologram interface - **No web browser required!**

### 💻 Command Line Interface
Traditional CLI for advanced users and scripting

## Features

- ✅ **Standalone Desktop GUI** - Native application with tactical hologram styling
- ✅ **No Dependencies** - Uses Python standard library only (tkinter)
- ✅ **Blueprint Scanner** - Automatically finds and lists all your blueprints
- ✅ **Safe Conversion** - Creates new `HEAVYARMOR_` blueprints (preserves originals)
- ✅ Scans Space Engineers blueprint XML files (`bp.sbc`)
- ✅ Replaces all light armor block types with heavy armor equivalents
- ✅ Supports both Large and Small grid blocks
- ✅ Automatic backup creation before modification (CLI)
- ✅ Comprehensive armor block type coverage (60+ block variants)
- ✅ Real-time conversion progress tracking
- ✅ Search and filter blueprints

## Supported Block Types

The tool replaces the following light armor blocks with their heavy variants:

### Large Grid
- Standard blocks (cube, slope, corner, inverted corner)
- Round armor variants
- 2x1 slopes and corners (base and tip)
- Half blocks and slopes
- Armor panels
- Sloped corners

### Small Grid
- All corresponding small grid variants of the above

For a complete list of mappings, run:
```bash
python se_armor_replacer.py --list-mappings
```

## Requirements

- Python 3.7 or higher
- **For Standalone GUI**: No external packages required (uses tkinter - included with Python)
- **For CLI**: No external packages required (uses Python standard library)

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed on your system

```bash
# Verify Python version
python --version
```

## Usage

### 🖥️ Standalone Desktop App (Recommended)

#### Windows Launch

Double-click `launch_gui.bat` or run:

```bash
python gui_standalone.py
```

#### What You'll See

A native desktop application with tactical hologram styling:

- **Blueprint Database Panel** - Left side with search and scrollable list
- **Details Panel** - Right side showing selected blueprint information
- **Exchange Visualization** - Before/after block type display
- **Tactical Styling** - Gunmetal grey, neon cyan/orange, tech-glass effects
- **Status Bar** - System status, scan/conversion counters
- **Corner Brackets** - Military-grade targeting system aesthetic

#### How to Use

1. **Application launches** and automatically scans your SE blueprints
2. **Browse or search** for blueprints in the left panel
3. **Select a blueprint** to view details on the right
4. **Review the conversion** - see light armor block count
5. **Click conversion button** (only enabled if light armor present)
6. **Confirm operation** - new blueprint created with `HEAVYARMOR_` prefix
7. **Original preserved** - your source blueprint remains untouched

#### Features

- ✅ **No browser required** - Native desktop application
- ✅ **Zero dependencies** - Uses Python's built-in tkinter
- ✅ **Fast and lightweight** - Instant startup
- ✅ **Automatic scanning** - Finds all blueprints on launch
- ✅ **Search filter** - Quickly find specific blueprints
- ✅ **Safe operation** - Always preserves originals
- ✅ **Threading** - Non-blocking UI during operations

### 💻 Command Line Interface

### Basic Usage

Replace armor blocks in a blueprint (creates automatic backup):
```bash
python se_armor_replacer.py path/to/blueprint/bp.sbc
```

### Advanced Options

**Save to a different file:**
```bash
python se_armor_replacer.py input.sbc -o output.sbc
```

**Process without creating backup:**
```bash
python se_armor_replacer.py blueprint.sbc --no-backup
```

**Enable verbose output:**
```bash
python se_armor_replacer.py blueprint.sbc -v
```

**List all armor block mappings:**
```bash
python se_armor_replacer.py --list-mappings
```

### Command-Line Arguments

```
usage: se_armor_replacer.py [-h] [-o OUTPUT] [-v] [--no-backup] [--list-mappings] input

positional arguments:
  input                 Path to blueprint file (bp.sbc) or directory containing it

optional arguments:
  -h, --help           show this help message and exit
  -o OUTPUT, --output OUTPUT
                       Output file path (default: modify in place)
  -v, --verbose        Enable verbose output
  --no-backup          Do not create backup file when modifying in place
  --list-mappings      List all armor block mappings and exit
```

## Finding Blueprint Files

Space Engineers blueprints are typically located at:

**Windows:**
```
%APPDATA%\SpaceEngineers\Blueprints\local\<YourBlueprintName>\bp.sbc
```

**Steam Workshop:**
```
C:\Program Files (x86)\Steam\steamapps\workshop\content\244850\<WorkshopID>\bp.sbc
```

## Examples

### Example 1: Process a local blueprint
```bash
python se_armor_replacer.py "C:\Users\YourName\AppData\Roaming\SpaceEngineers\Blueprints\local\MyShip\bp.sbc"
```

### Example 2: Batch process with custom output
```bash
python se_armor_replacer.py input_ship.sbc -o heavy_armor_ship.sbc -v
```

### Example 3: Process directory (automatically finds bp.sbc)
```bash
python se_armor_replacer.py "C:\Users\YourName\AppData\Roaming\SpaceEngineers\Blueprints\local\MyShip"
```

## How It Works

1. **Scan**: The tool parses the Space Engineers blueprint XML file
2. **Identify**: Searches for all `<CubeBlock>` elements with light armor `SubtypeId` values
3. **Replace**: Swaps light armor SubtypeIds with their heavy armor equivalents
4. **Save**: Writes the modified XML back to the file (or new location)
5. **Backup**: Automatically creates a `.sbc.backup` file (unless disabled)

## XML Structure

Space Engineers blueprints use XML format with structure like:
```xml
<Definitions>
  <ShipBlueprints>
    <ShipBlueprint>
      <CubeBlocks>
        <MyObjectBuilder_CubeBlock>
          <SubtypeId>LargeBlockArmorBlock</SubtypeId>
          <!-- This gets replaced with LargeHeavyBlockArmorBlock -->
        </MyObjectBuilder_CubeBlock>
      </CubeBlocks>
    </ShipBlueprint>
  </ShipBlueprints>
</Definitions>
```

## Troubleshooting

**Error: "Could not find bp.sbc"**
- Ensure you're pointing to the correct blueprint directory
- The file must be named exactly `bp.sbc`

**Error: "Failed to parse XML file"**
- The blueprint file may be corrupted
- Ensure Space Engineers isn't currently running or modifying the file

**No replacements made**
- Your blueprint may already use heavy armor blocks
- Use `--list-mappings` to see what blocks can be replaced
- Use `-v` for verbose output to see scanning details

## Safety

- **Automatic Backups**: The tool creates backups by default (`.sbc.backup` files)
- **Read Original First**: Always keep a copy of your original blueprint
- **Test in Creative**: Test converted blueprints in creative mode first
- **Non-Destructive**: Original files are preserved unless `--no-backup` is used

## Limitations

- Only processes blueprint files (`bp.sbc`), not world saves
- Does not modify paint colors or skin settings
- Does not adjust component costs (handled by Space Engineers)
- Requires manual reload in Space Engineers to see changes

## Contributing

Feel free to submit issues or pull requests to add support for:
- Additional armor block variants
- Batch processing multiple blueprints
- GUI interface
- Reverse conversion (heavy to light)

**Note:** By contributing, you agree that your contributions will be licensed under the same terms as this project. All copyright and ownership remain with the original copyright holder.

## License

**Copyright © 2025. All Rights Reserved.**

This software is provided for **personal use only**. You may **NOT**:
- Redistribute, publish, or share this software publicly
- Sell or use this software commercially
- Claim this software as your own work
- Remove copyright notices

**You MAY:**
- Use this software personally for Space Engineers blueprints
- Contribute improvements via pull requests
- Fork for personal modifications (must not redistribute)

See the [LICENSE](LICENSE) file for complete terms.

**TL;DR:** Use it, improve it, but don't steal it or redistribute it.

## Credits

Created for the Space Engineers community to simplify blueprint modifications.

## Version History

- **v1.0.0** (2025) - Initial release
  - Support for 60+ armor block types
  - Automatic backup creation
  - Command-line interface
  - Large and small grid support
