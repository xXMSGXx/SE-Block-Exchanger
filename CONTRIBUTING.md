# Contributing

Thanks for contributing to SE Block Exchanger.

## Development Setup

1. Install Python 3.8+.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
pip install pytest ruff mypy
```

4. Run tests:

```bash
pytest -q
```

## Contribution Flow

1. Create a feature branch from `main`.
2. Make focused commits with clear messages.
3. Run lint/type/tests before pushing:

```bash
ruff check .
mypy . --ignore-missing-imports
pytest -q
```

4. Open a pull request with:
- problem statement
- technical approach
- screenshots for UI changes
- test evidence

## Mapping/Profile Contributions

Use `.sebx-profile` JSON format:

```json
{
  "name": "Example Profile",
  "author": "Your Name",
  "version": "1.0",
  "description": "What this profile does",
  "game_version": "1.205+",
  "categories": [
    {
      "name": "Category Name",
      "pairs": [
        ["SourceSubtype", "TargetSubtype"]
      ]
    }
  ]
}
```

Requirements:
- no circular swaps
- no duplicate targets in a category
- include references for mod subtype IDs when applicable

## Reporting Bugs

Use the Bug Report issue template and include:
- exact steps
- expected vs actual behavior
- stack trace/log output
- app version and SE version

