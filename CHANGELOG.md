# Space Engineers Block Exchanger - Changelog

## Version 1.2 - Block Detection Fix (November 28, 2025)

### Critical Bug Fix
- ✅ **FIXED: Block detection now works correctly!**
  - Changed from `<SubtypeId>` to `<SubtypeName>` (Space Engineers uses SubtypeName in blueprints)
  - All armor blocks are now properly detected and counted
  - Conversion functionality now works as intended

### New Features
- ✅ **Heavy Armor Count** - GUI and scanner now show heavy armor block counts
- ✅ Added 36 heavy armor block types to detection system
- ✅ Separate light vs heavy armor statistics

### Bug Fixes
- **Blueprint Scanner**: Fixed to use `SubtypeName` element instead of `SubtypeId`
  - Space Engineers blueprint XML uses `<SubtypeName>` for block identification
  - Original code looked for non-existent `<SubtypeId>` element
  - Now correctly detects: 83/90 blueprints contain armor blocks
  
- **Armor Block Replacer**: Updated to use `SubtypeName` for conversions
  - Conversion now properly identifies light armor blocks
  - Replacement logic now functional

- **GUI Display**: Added heavy armor count field
  - Details panel now shows both light and heavy armor
  - Exchange visualization displays accurate counts
  - Convert button correctly enables when light armor present

### Technical Details
- Added `HEAVY_ARMOR_BLOCKS` set with complete block type list
- Updated `BlueprintInfo` dataclass with `heavy_armor_count` field
- Added `.strip()` to handle whitespace in SubtypeName values
- Fixed XPath queries to use correct element name

### Test Results
**Before:** 0 armor blocks detected (incorrect)
**After:** 83 blueprints with armor blocks, accurate light/heavy counts

Example: "Blueprint Missile" - 70 light, 64 heavy armor blocks ✅

## Version 1.1 - Standalone Edition (November 28, 2025)

### Major Changes
- ✅ **Converted to Standalone Desktop Application** - No web browser required
- ✅ **Removed Legacy Web UI** - Deleted Flask-based web interface and all dependencies
- ✅ **Fixed Blueprint Naming Issue** - Now uses folder names instead of problematic DisplayName XML field

### Bug Fixes
- **Blueprint Scanner**: Fixed issue where DisplayName contained garbled characters (e.g., "xXMSGXx")
  - Now uses folder name as display name (most reliable)
  - Space Engineers users typically name folders, not internal DisplayName field
  - Fallback to folder name ensures readable blueprint names

- **Blueprint Count**: Clarified that 90+ blueprints is correct count
  - Scanner correctly finds all blueprint folders
  - Each folder with bp.sbc file is a valid blueprint

### Removed Files
- ❌ `web_server.py` - Flask web server
- ❌ `launch_web_ui.py` - Web launcher
- ❌ `launch_web_ui.bat` - Windows web launcher
- ❌ `templates/` - HTML templates
- ❌ `static/` - CSS/JavaScript assets

### New Files
- ✅ `gui_standalone.py` - Native tkinter desktop application
- ✅ `launch_gui.bat` - Windows GUI launcher
- ✅ `QUICKSTART_GUI.md` - GUI usage guide
- ✅ `STANDALONE_CONVERSION.md` - Technical conversion notes

### Improvements
- **No Dependencies**: Uses only Python standard library (tkinter)
- **Better Performance**: Native app is faster than web+browser
- **Cleaner Codebase**: Removed 800+ lines of web code
- **Simpler Distribution**: Single .py file vs multi-file web app

### Technical Details
- Blueprint parsing improved to handle XML encoding issues
- GridSizeEnum now searched within CubeGrid element (more reliable)
- Block counting uses proper XPath queries
- Threading prevents UI blocking during scans/conversions

## Version 1.0 - Initial Release

### Features
- Command-line armor block replacement tool
- Web-based tactical hologram UI
- Blueprint scanner with metadata extraction
- Safe conversion with HEAVYARMOR_ prefix
- 60+ armor block type mappings
- Comprehensive unit tests (11 tests)
