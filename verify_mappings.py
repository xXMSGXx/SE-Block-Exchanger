"""
Mapping verification utility.
"""

from pathlib import Path

from blueprint_scanner import BlueprintScanner
from mapping_profiles import ProfileManager
from mappings import build_registry
from se_armor_replacer import ArmorBlockReplacer


def verify() -> None:
    registry = build_registry(include_builtin=True)
    profile_manager = ProfileManager(Path("profiles"))
    loaded_profiles = profile_manager.load_all()
    loaded_profile_categories = profile_manager.register_profile_categories(registry)

    assert BlueprintScanner.LIGHT_ARMOR_BLOCKS == set(ArmorBlockReplacer.LIGHT_TO_HEAVY.keys()), (
        "LIGHT_ARMOR_BLOCKS mismatch"
    )
    assert BlueprintScanner.HEAVY_ARMOR_BLOCKS == set(ArmorBlockReplacer.LIGHT_TO_HEAVY.values()), (
        "HEAVY_ARMOR_BLOCKS mismatch"
    )

    categories = registry.list_categories()
    all_pairs = {}
    duplicate_sources = []
    for category in categories:
        for source, target in category.pairs.items():
            if source in all_pairs and all_pairs[source] != target:
                duplicate_sources.append((source, all_pairs[source], target, category.name))
            all_pairs[source] = target

    print(f"Built-in categories      : {len([c for c in categories if c.source == 'built-in'])}")
    print(f"Profile files loaded     : {len(loaded_profiles)}")
    print(f"Profile categories loaded: {loaded_profile_categories}")
    print(f"Total categories         : {len(categories)}")
    print(f"Total mapping pairs      : {len(all_pairs)}")
    for category in categories:
        print(f"  - {category.name:40} {len(category.pairs):4} pairs [{category.source}]")
    if duplicate_sources:
        print("\nConflicting sources detected across categories (allowed when categories are toggled separately):")
        for source, old, new, category in duplicate_sources:
            print(f"  - {source}: {old} vs {new} [{category}]")
    print("Mapping verification passed.")


if __name__ == "__main__":
    verify()
