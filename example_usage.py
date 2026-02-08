"""
SE Block Exchanger v3 usage examples.
"""

from pathlib import Path

from blueprint_analytics import BlueprintAnalyticsEngine
from blueprint_converter import BlueprintConverter
from se_armor_replacer import ArmorBlockReplacer


def example_cli_engine():
    replacer = ArmorBlockReplacer(
        verbose=True,
        enabled_categories=["armor", "thrusters"],
    )
    scanned, changed = replacer.process_blueprint("path/to/blueprint/bp.sbc", dry_run=True)
    print(f"Scanned: {scanned}, changes: {changed}")
    print(replacer.get_dry_run_report())


def example_converter():
    converter = BlueprintConverter(
        reverse=False,
        enabled_categories=["armor", "weapons"],
    )
    destination, scanned, converted = converter.create_converted_blueprint(Path("path/to/MyBlueprint"))
    print(destination, scanned, converted)


def example_analytics():
    engine = BlueprintAnalyticsEngine()
    result = engine.analyze_blueprint(Path("path/to/blueprint/bp.sbc"))
    print(result.pcu_total, result.mass_total)


if __name__ == "__main__":
    print("Run one example function after updating file paths.")

