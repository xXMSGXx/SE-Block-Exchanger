# Space Engineers Block Exchanger v3.0

By Meraby Labs

[![CI](https://github.com/Meraby-Labs/se-block-exchanger/actions/workflows/ci.yml/badge.svg)](https://github.com/Meraby-Labs/se-block-exchanger/actions/workflows/ci.yml)
[![Release](https://github.com/Meraby-Labs/se-block-exchanger/actions/workflows/release.yml/badge.svg)](https://github.com/Meraby-Labs/se-block-exchanger/actions/workflows/release.yml)

SE Block Exchanger is a desktop + CLI toolkit for Space Engineers blueprint engineering:

- Multi-category block conversion (armor, thrusters, weapons, functional)
- Modular mapping registry with profile support
- Blueprint analytics (ores, ingots, components, PCU, mass, category distribution)
- Dry-run diff preview and conversion cost delta reporting
- Profile editor with import/export/share and sample-blueprint testing
- Update checker, changelog viewer, and automated CI/release pipelines

## Requirements

- Python 3.8+
- `customtkinter`
- Optional: `Pillow` for logo/icon workflows

Install:

```bash
pip install -r requirements.txt
```

## Quick Start

GUI:

```bash
python gui_standalone.py
```

CLI (backward compatible):

```bash
python se_armor_replacer.py path/to/blueprint/bp.sbc
```

## CLI Usage

Light -> Heavy armor (default category = `armor`):

```bash
python se_armor_replacer.py <path>
```

Reverse conversion:

```bash
python se_armor_replacer.py <path> --reverse
```

Dry-run:

```bash
python se_armor_replacer.py <path> --dry-run
```

Enable additional categories:

```bash
python se_armor_replacer.py <path> --categories armor,thrusters,weapons,functional
```

List categories and mappings:

```bash
python se_armor_replacer.py --list-categories
python se_armor_replacer.py --list-mappings --categories armor,thrusters
```

## GUI Feature Set

- CustomTkinter modular UI (`ui/` package)
- Category toggles for conversion mapping selection
- Keyboard shortcuts:
  - `Ctrl+O` browse blueprint directory
  - `Ctrl+R` run conversion
  - `Ctrl+Z` undo last conversion
- Recent blueprint directories and recent blueprint quick access
- Native Windows drag-and-drop for blueprint file/folder loading
- Before/after diff preview
- Analytics dashboard with:
  - PCU/mass counters
  - category distribution chart
  - ore -> ingot -> component -> block tree
  - conversion deltas
  - health audit with fix actions
- CSV/TXT analytics export
- Profile editor dialog:
  - create/edit/duplicate profiles
  - add/remove mapping pairs with known subtype suggestions
  - test profile against selected blueprint
  - import/export `.sebx-profile`
  - import profile from URL
  - Discord share payload copy
- In-app changelog and update notifications

## Mapping Registry

Built-in categories:

- `armor` (70 pairs)
- `thrusters`
- `weapons`
- `functional`

Profiles auto-load from `profiles/` at startup.

Built-in mod profile files shipped:

- `profiles/weaponcore.sebx-profile`
- `profiles/assertive_armaments.sebx-profile`
- `profiles/build_vision.sebx-profile`

## UI Gallery

- Header: branding, recent directories, appearance mode, profile/changelog access
- Left panel: blueprint cards with status badges, search, recent picks
- Center panel: INTEL / XML / PREVIEW DIFF / ANALYTICS tabs
- Right panel: conversion mode, category toggles, progress ring, batch + undo controls
- Footer: status telemetry, version/build metadata, update notification

## Testing

Run full suite:

```bash
pytest -q
```

Current suite covers:

- legacy conversion behavior (19 compatibility tests)
- mapping registry validation
- profile management
- analytics and export
- update checker cache behavior

## Packaging and Release

- CI workflow: `.github/workflows/ci.yml`
- Release workflow: `.github/workflows/release.yml` (tag `vX.Y.Z`)
- Version source of truth: `version.py`

## Contributing and Community

- Contributing: `CONTRIBUTING.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- Issue templates:
  - bug report
  - feature request
  - mapping request

## License

See `LICENSE`.

