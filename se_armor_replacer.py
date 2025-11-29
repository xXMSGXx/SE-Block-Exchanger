#!/usr/bin/env python3
"""
Space Engineers Armor Block Replacer
Scans Space Engineers blueprint XML files and replaces light armor blocks with heavy armor variants.
"""

import xml.etree.ElementTree as ET
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class ArmorBlockReplacer:
    """Replaces light armor blocks with heavy armor variants in Space Engineers blueprints."""
    
    # Mapping of light armor SubtypeIds to their heavy armor equivalents
    ARMOR_REPLACEMENTS = {
        # Large Grid Blocks
        'LargeBlockArmorBlock': 'LargeHeavyBlockArmorBlock',
        'LargeBlockArmorSlope': 'LargeHeavyBlockArmorSlope',
        'LargeBlockArmorCorner': 'LargeHeavyBlockArmorCorner',
        'LargeBlockArmorCornerInv': 'LargeHeavyBlockArmorCornerInv',
        'LargeRoundArmor_Slope': 'LargeHeavyRoundArmor_Slope',
        'LargeRoundArmor_Corner': 'LargeHeavyRoundArmor_Corner',
        'LargeRoundArmor_CornerInv': 'LargeHeavyRoundArmor_CornerInv',
        'LargeBlockArmorSlope2Base': 'LargeHeavyBlockArmorSlope2Base',
        'LargeBlockArmorSlope2Tip': 'LargeHeavyBlockArmorSlope2Tip',
        'LargeBlockArmorCorner2Base': 'LargeHeavyBlockArmorCorner2Base',
        'LargeBlockArmorCorner2Tip': 'LargeHeavyBlockArmorCorner2Tip',
        'LargeBlockArmorInvCorner2Base': 'LargeHeavyBlockArmorInvCorner2Base',
        'LargeBlockArmorInvCorner2Tip': 'LargeHeavyBlockArmorInvCorner2Tip',
        
        # Small Grid Blocks
        'SmallBlockArmorBlock': 'SmallHeavyBlockArmorBlock',
        'SmallBlockArmorSlope': 'SmallHeavyBlockArmorSlope',
        'SmallBlockArmorCorner': 'SmallHeavyBlockArmorCorner',
        'SmallBlockArmorCornerInv': 'SmallHeavyBlockArmorCornerInv',
        'SmallRoundArmor_Slope': 'SmallHeavyRoundArmor_Slope',
        'SmallRoundArmor_Corner': 'SmallHeavyRoundArmor_Corner',
        'SmallRoundArmor_CornerInv': 'SmallHeavyRoundArmor_CornerInv',
        'SmallBlockArmorSlope2Base': 'SmallHeavyBlockArmorSlope2Base',
        'SmallBlockArmorSlope2Tip': 'SmallHeavyBlockArmorSlope2Tip',
        'SmallBlockArmorCorner2Base': 'SmallHeavyBlockArmorCorner2Base',
        'SmallBlockArmorCorner2Tip': 'SmallHeavyBlockArmorCorner2Tip',
        'SmallBlockArmorInvCorner2Base': 'SmallHeavyBlockArmorInvCorner2Base',
        'SmallBlockArmorInvCorner2Tip': 'SmallHeavyBlockArmorInvCorner2Tip',
        
        # Half Blocks
        'LargeHalfArmorBlock': 'LargeHeavyHalfArmorBlock',
        'LargeHalfSlopeArmorBlock': 'LargeHeavyHalfSlopeArmorBlock',
        'SmallHalfArmorBlock': 'SmallHeavyHalfArmorBlock',
        'SmallHalfSlopeArmorBlock': 'SmallHeavyHalfSlopeArmorBlock',
        
        # Quarter Blocks
        'LargeArmorPanelLight': 'LargeArmorPanelHeavy',
        'SmallArmorPanelLight': 'SmallArmorPanelHeavy',
        
        # Additional variants
        'LargeArmorSlopedCorner': 'LargeHeavyArmorSlopedCorner',
        'LargeArmorSlopedCornerTip': 'LargeHeavyArmorSlopedCornerTip',
        'LargeArmorSlopedCornerBase': 'LargeHeavyArmorSlopedCornerBase',
        'SmallArmorSlopedCorner': 'SmallHeavyArmorSlopedCorner',
        'SmallArmorSlopedCornerTip': 'SmallHeavyArmorSlopedCornerTip',
        'SmallArmorSlopedCornerBase': 'SmallHeavyArmorSlopedCornerBase',
    }
    
    def __init__(self, verbose: bool = False):
        """Initialize the replacer with optional verbose output."""
        self.verbose = verbose
        self.replacements_made = 0
        self.blocks_scanned = 0
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def find_blueprint_file(self, path: Path) -> Path:
        """Find the bp.sbc file in the given path."""
        if path.is_file() and path.name == 'bp.sbc':
            return path
        elif path.is_dir():
            bp_file = path / 'bp.sbc'
            if bp_file.exists():
                return bp_file
            # Search subdirectories
            for item in path.rglob('bp.sbc'):
                return item
        raise FileNotFoundError(f"Could not find bp.sbc in {path}")
    
    def backup_file(self, file_path: Path) -> Path:
        """Create a backup of the original file."""
        backup_path = file_path.with_suffix('.sbc.backup')
        counter = 1
        while backup_path.exists():
            backup_path = file_path.with_suffix(f'.sbc.backup{counter}')
            counter += 1
        
        import shutil
        shutil.copy2(file_path, backup_path)
        self.log(f"Backup created: {backup_path}")
        return backup_path
    
    def replace_armor_blocks(self, tree: ET.ElementTree) -> int:
        """
        Replace light armor blocks with heavy armor variants in the XML tree.
        Returns the number of replacements made.
        """
        root = tree.getroot()
        replacements = 0
        
        # Find all CubeBlocks sections
        for cube_blocks in root.findall('.//CubeBlocks'):
            for block in cube_blocks.findall('MyObjectBuilder_CubeBlock'):
                self.blocks_scanned += 1
                
                # IMPORTANT: Space Engineers uses <SubtypeName> not <SubtypeId>
                subtype_elem = block.find('SubtypeName')
                if subtype_elem is not None and subtype_elem.text:
                    current_subtype = subtype_elem.text.strip()
                    
                    # Check if this is a light armor block that needs replacement
                    if current_subtype in self.ARMOR_REPLACEMENTS:
                        new_subtype = self.ARMOR_REPLACEMENTS[current_subtype]
                        self.log(f"Replacing {current_subtype} -> {new_subtype}")
                        subtype_elem.text = new_subtype
                        replacements += 1
        
        return replacements
    
    def process_blueprint(self, input_path: str, output_path: str = None, 
                         create_backup: bool = True) -> Tuple[int, int]:
        """
        Process a Space Engineers blueprint file.
        
        Args:
            input_path: Path to the blueprint file or directory
            output_path: Optional output path (if None, modifies in place)
            create_backup: Whether to create a backup before modifying
        
        Returns:
            Tuple of (blocks_scanned, replacements_made)
        """
        input_file = self.find_blueprint_file(Path(input_path))
        self.log(f"Processing blueprint: {input_file}")
        
        # Parse the XML file
        try:
            tree = ET.parse(input_file)
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML file: {e}")
        
        # Create backup if requested and modifying in place
        if create_backup and output_path is None:
            self.backup_file(input_file)
        
        # Replace armor blocks
        self.replacements_made = self.replace_armor_blocks(tree)
        
        # Determine output file
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_file = input_file
        
        # Write the modified XML
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        self.log(f"Output written to: {output_file}")
        
        return self.blocks_scanned, self.replacements_made
    
    def get_replacement_summary(self) -> str:
        """Get a summary of the replacement operation."""
        return (f"Scanned {self.blocks_scanned} blocks, "
                f"replaced {self.replacements_made} light armor blocks with heavy armor variants.")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Replace light armor blocks with heavy armor in Space Engineers blueprints',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Replace armor in a blueprint (creates backup)
  python se_armor_replacer.py path/to/blueprint/bp.sbc
  
  # Replace and save to a different file
  python se_armor_replacer.py input.sbc -o output.sbc
  
  # Process without creating backup
  python se_armor_replacer.py blueprint.sbc --no-backup
  
  # Verbose output
  python se_armor_replacer.py blueprint.sbc -v
        """
    )
    
    parser.add_argument('input', help='Path to blueprint file (bp.sbc) or directory containing it')
    parser.add_argument('-o', '--output', help='Output file path (default: modify in place)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--no-backup', action='store_true', 
                       help='Do not create backup file when modifying in place')
    parser.add_argument('--list-mappings', action='store_true',
                       help='List all armor block mappings and exit')
    
    args = parser.parse_args()
    
    # Handle --list-mappings
    if args.list_mappings:
        print("Light Armor -> Heavy Armor Mappings:")
        print("=" * 60)
        for light, heavy in sorted(ArmorBlockReplacer.ARMOR_REPLACEMENTS.items()):
            print(f"{light:40} -> {heavy}")
        return 0
    
    # Create replacer instance
    replacer = ArmorBlockReplacer(verbose=args.verbose)
    
    try:
        # Process the blueprint
        blocks_scanned, replacements = replacer.process_blueprint(
            args.input,
            args.output,
            create_backup=not args.no_backup
        )
        
        # Print summary
        print(f"\n✓ Success!")
        print(f"  Blocks scanned: {blocks_scanned}")
        print(f"  Replacements made: {replacements}")
        
        if replacements == 0:
            print("\n  No light armor blocks found to replace.")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
