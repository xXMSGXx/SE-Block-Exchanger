# Installation and Build Guide

## Run From Source

1. Install Python 3.8+.
2. (Optional) Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Launch GUI:

```bash
python gui_standalone.py
```

5. Or run CLI:

```bash
python se_armor_replacer.py --help
```

## Test Suite

```bash
pytest -q
```

Expected: all tests pass.

## Build Windows EXE

```bash
build_exe.bat
```

The build embeds:

- `README.md`
- `LICENSE`
- `RELEASE_NOTES.md`
- `profiles/`
- `data/`

Output executable is written to `dist/`.

## GitHub Actions

- CI: `.github/workflows/ci.yml`
- Tagged release: `.github/workflows/release.yml`

Release flow:

1. Set `version.py` (for example `3.0.0`)
2. Commit and push
3. Create tag `v3.0.0`
4. Push tag to trigger release workflow

