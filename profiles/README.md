# Profile Format Guide

Profiles are JSON documents with extension `.sebx-profile`.

## Schema

```json
{
  "name": "WeaponCore Upgrades",
  "author": "Meraby Labs",
  "version": "1.0",
  "description": "Swap vanilla weapons for WeaponCore equivalents",
  "game_version": "1.205+",
  "categories": [
    {
      "name": "WC Turrets",
      "description": "Large-grid turret upgrades",
      "grid_sizes": ["Large"],
      "pairs": [
        ["LargeGatlingTurret", "WC_LargeGatlingTurret"]
      ]
    }
  ]
}
```

## Rules

- Every pair must be `[source, target]`.
- No empty values.
- No circular mappings in a category (`A -> B` and `B -> A`).
- No duplicate targets in a category.

## Loading Behavior

- Profiles in `profiles/` are auto-discovered on startup.
- Categories are namespaced internally as `profile:<profile_name>:<category_name>`.
- Conflicting categories can still coexist; select only compatible categories together.

## Sharing

- Export from Profile Editor or copy Discord payload from the Share button.
- Submit profile additions using the Mapping Request issue template.

