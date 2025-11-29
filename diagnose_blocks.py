"""
Diagnostic script to analyze Space Engineers blueprints and identify armor blocks
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
import os

# Get first blueprint
bp_dir = Path(os.getenv('APPDATA')) / 'SpaceEngineers' / 'Blueprints' / 'local'
blueprints = list(bp_dir.iterdir())[:5]  # First 5 blueprints

print("=== ANALYZING BLUEPRINTS ===\n")

all_subtypes = Counter()
armor_blocks = {}

for bp_folder in blueprints:
    bp_file = bp_folder / 'bp.sbc'
    if not bp_file.exists():
        continue
    
    print(f"Blueprint: {bp_folder.name}")
    
    try:
        tree = ET.parse(bp_file)
        root = tree.getroot()
        
        # Find all CubeBlock elements
        blocks = root.findall('.//CubeGrid/CubeBlocks/MyObjectBuilder_CubeBlock')
        print(f"  Total blocks found: {len(blocks)}")
        
        # Count subtypes
        local_subtypes = []
        for block in blocks:
            subtype_elem = block.find('SubtypeId')
            type_attr = block.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            
            if subtype_elem is not None:
                subtype = subtype_elem.text
                local_subtypes.append(subtype)
                all_subtypes[subtype] += 1
                
                # Track armor blocks
                if 'Armor' in subtype:
                    if subtype not in armor_blocks:
                        armor_blocks[subtype] = type_attr
        
        # Show unique blocks in this blueprint
        unique = set(local_subtypes)
        print(f"  Unique block types: {len(unique)}")
        
        # Show armor blocks
        armor_in_bp = [s for s in unique if 'Armor' in s or 'armor' in s]
        if armor_in_bp:
            print(f"  Armor blocks: {', '.join(armor_in_bp[:5])}")
        
        print()
        
    except Exception as e:
        print(f"  Error: {e}\n")

print("\n=== MOST COMMON BLOCKS (Top 30) ===")
for subtype, count in all_subtypes.most_common(30):
    print(f"{subtype:50} : {count:4} times")

print("\n=== ALL ARMOR BLOCKS FOUND ===")
for subtype in sorted(armor_blocks.keys()):
    print(f"  {subtype:50} (Type: {armor_blocks[subtype]})")

# Check for light vs heavy
print("\n=== LIGHT vs HEAVY ARMOR ===")
light_armor = [s for s in armor_blocks.keys() if 'Heavy' not in s]
heavy_armor = [s for s in armor_blocks.keys() if 'Heavy' in s]

print(f"Light armor blocks found: {len(light_armor)}")
print(f"Heavy armor blocks found: {len(heavy_armor)}")

if light_armor:
    print("\nLight armor examples:")
    for s in sorted(light_armor)[:10]:
        print(f"  - {s}")

if heavy_armor:
    print("\nHeavy armor examples:")
    for s in sorted(heavy_armor)[:10]:
        print(f"  - {s}")
