# Quick Start Guide

## Installation

1. Ensure Python 3.7+ is installed:
   ```bash
   python --version
   ```

2. No additional packages required - uses Python standard library only!

## Basic Usage

### Replace armor blocks in a blueprint:
```bash
python se_armor_replacer.py "C:\Users\YourName\AppData\Roaming\SpaceEngineers\Blueprints\local\MyShip\bp.sbc"
```

### Common Commands

**Process with verbose output:**
```bash
python se_armor_replacer.py path/to/bp.sbc -v
```

**Save to new file:**
```bash
python se_armor_replacer.py input.sbc -o output.sbc
```

**List all supported block types:**
```bash
python se_armor_replacer.py --list-mappings
```

**Process without backup:**
```bash
python se_armor_replacer.py path/to/bp.sbc --no-backup
```

## Testing

Run the test suite:
```bash
python test_armor_replacer.py
```

## Examples

See `example_usage.py` for programmatic usage examples including:
- Basic replacement
- Batch processing multiple blueprints
- Custom output locations
- Integration into your own scripts

## Finding Your Blueprints

Space Engineers saves blueprints at:

**Windows:**
```
%APPDATA%\SpaceEngineers\Blueprints\local\
```

**Quick access:**
1. Press Win+R
2. Type: `%APPDATA%\SpaceEngineers\Blueprints\local`
3. Press Enter

## What Gets Replaced?

The tool replaces 60+ light armor block types with heavy armor equivalents:
- ✅ Large Grid: All standard, sloped, corner, and panel variants
- ✅ Small Grid: All standard, sloped, corner, and panel variants
- ✅ Half blocks and quarter panels
- ✅ Round armor variants
- ✅ 2x1 slopes and corners

## Safety Features

- **Automatic Backup**: Creates `.sbc.backup` files by default
- **Non-Destructive**: Original blueprints preserved unless you use `--no-backup`
- **Preview Mode**: Use `-v` to see what will be replaced before committing

## Troubleshooting

**"Could not find bp.sbc"**
→ Make sure you're pointing to the correct blueprint directory

**No replacements made**
→ Your blueprint already uses heavy armor! Use `-v` to verify

**Parse error**
→ Blueprint file may be corrupted or Space Engineers is currently using it

## Need Help?

- Full documentation: See `README.md`
- Code examples: See `example_usage.py`
- Run tests: `python test_armor_replacer.py`
- Help command: `python se_armor_replacer.py --help`

## Tips

1. **Always test in Creative Mode first** after conversion
2. **Keep backups** of important blueprints
3. **Close Space Engineers** before running the tool
4. Use **verbose mode (`-v`)** to see detailed progress

---

**Ready to convert your blueprints? Start with:**
```bash
python se_armor_replacer.py --list-mappings
python se_armor_replacer.py path/to/your/blueprint/bp.sbc -v
```
