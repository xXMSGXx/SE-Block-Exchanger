"""
Space Engineers Armor Block Replacer - Example Usage

This file demonstrates how to use the ArmorBlockReplacer class programmatically.
"""

from se_armor_replacer import ArmorBlockReplacer

# Example 1: Basic usage with default settings
def example_basic():
    """Replace armor blocks with default settings."""
    replacer = ArmorBlockReplacer(verbose=True)
    
    blueprint_path = "path/to/your/blueprint/bp.sbc"
    blocks_scanned, replacements = replacer.process_blueprint(blueprint_path)
    
    print(f"\nProcessed blueprint:")
    print(f"  Blocks scanned: {blocks_scanned}")
    print(f"  Replacements made: {replacements}")


# Example 2: Save to a different file
def example_save_to_new_file():
    """Replace armor and save to a new file."""
    replacer = ArmorBlockReplacer(verbose=False)
    
    input_path = "original_blueprint.sbc"
    output_path = "heavy_armor_blueprint.sbc"
    
    replacer.process_blueprint(input_path, output_path)
    print(replacer.get_replacement_summary())


# Example 3: Process without backup
def example_no_backup():
    """Replace armor without creating backup."""
    replacer = ArmorBlockReplacer(verbose=True)
    
    blueprint_path = "temporary_blueprint.sbc"
    replacer.process_blueprint(blueprint_path, create_backup=False)


# Example 4: Batch process multiple blueprints
def example_batch_process():
    """Process multiple blueprint files."""
    from pathlib import Path
    
    blueprint_dir = Path("blueprints")
    replacer = ArmorBlockReplacer(verbose=False)
    
    total_replacements = 0
    
    for bp_file in blueprint_dir.rglob("bp.sbc"):
        print(f"\nProcessing: {bp_file}")
        blocks, replacements = replacer.process_blueprint(str(bp_file))
        total_replacements += replacements
        print(f"  Replaced {replacements} blocks")
    
    print(f"\nTotal replacements across all blueprints: {total_replacements}")


# Example 5: Check what mappings are available
def example_list_mappings():
    """Display all available armor block mappings."""
    print("Available armor block mappings:")
    print("=" * 80)
    
    for light, heavy in sorted(ArmorBlockReplacer.ARMOR_REPLACEMENTS.items()):
        print(f"{light:45} -> {heavy}")


if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # example_basic()
    # example_save_to_new_file()
    # example_no_backup()
    # example_batch_process()
    example_list_mappings()
