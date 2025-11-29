"""
Blueprint Scanner Module
Scans Space Engineers blueprint directories and extracts metadata
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import os


@dataclass
class BlueprintInfo:
    """Information about a Space Engineers blueprint."""
    name: str
    path: Path
    display_name: str
    grid_size: str  # 'Large' or 'Small'
    block_count: int
    light_armor_count: int
    heavy_armor_count: int
    has_bp_file: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'path': str(self.path),
            'display_name': self.display_name,
            'grid_size': self.grid_size,
            'block_count': self.block_count,
            'light_armor_count': self.light_armor_count,
            'heavy_armor_count': self.heavy_armor_count,
            'has_bp_file': self.has_bp_file
        }


class BlueprintScanner:
    """Scans and manages Space Engineers blueprints."""
    
    # Mapping from ArmorBlockReplacer - Light Armor Blocks
    LIGHT_ARMOR_BLOCKS = {
        'LargeBlockArmorBlock', 'LargeBlockArmorSlope', 'LargeBlockArmorCorner',
        'LargeBlockArmorCornerInv', 'LargeRoundArmor_Slope', 'LargeRoundArmor_Corner',
        'LargeRoundArmor_CornerInv', 'LargeBlockArmorSlope2Base', 'LargeBlockArmorSlope2Tip',
        'LargeBlockArmorCorner2Base', 'LargeBlockArmorCorner2Tip', 'LargeBlockArmorInvCorner2Base',
        'LargeBlockArmorInvCorner2Tip', 'SmallBlockArmorBlock', 'SmallBlockArmorSlope',
        'SmallBlockArmorCorner', 'SmallBlockArmorCornerInv', 'SmallRoundArmor_Slope',
        'SmallRoundArmor_Corner', 'SmallRoundArmor_CornerInv', 'SmallBlockArmorSlope2Base',
        'SmallBlockArmorSlope2Tip', 'SmallBlockArmorCorner2Base', 'SmallBlockArmorCorner2Tip',
        'SmallBlockArmorInvCorner2Base', 'SmallBlockArmorInvCorner2Tip', 'LargeHalfArmorBlock',
        'LargeHalfSlopeArmorBlock', 'SmallHalfArmorBlock', 'SmallHalfSlopeArmorBlock',
        'LargeArmorPanelLight', 'SmallArmorPanelLight', 'LargeArmorSlopedCorner',
        'LargeArmorSlopedCornerTip', 'LargeArmorSlopedCornerBase', 'SmallArmorSlopedCorner',
        'SmallArmorSlopedCornerTip', 'SmallArmorSlopedCornerBase'
    }
    
    # Heavy Armor Blocks
    HEAVY_ARMOR_BLOCKS = {
        'LargeHeavyBlockArmorBlock', 'LargeHeavyBlockArmorSlope', 'LargeHeavyBlockArmorCorner',
        'LargeHeavyBlockArmorCornerInv', 'LargeHeavyRoundArmor_Slope', 'LargeHeavyRoundArmor_Corner',
        'LargeHeavyRoundArmor_CornerInv', 'LargeHeavyBlockArmorSlope2Base', 'LargeHeavyBlockArmorSlope2Tip',
        'LargeHeavyBlockArmorCorner2Base', 'LargeHeavyBlockArmorCorner2Tip', 'LargeHeavyBlockArmorInvCorner2Base',
        'LargeHeavyBlockArmorInvCorner2Tip', 'SmallHeavyBlockArmorBlock', 'SmallHeavyBlockArmorSlope',
        'SmallHeavyBlockArmorCorner', 'SmallHeavyBlockArmorCornerInv', 'SmallHeavyRoundArmor_Slope',
        'SmallHeavyRoundArmor_Corner', 'SmallHeavyRoundArmor_CornerInv', 'SmallHeavyBlockArmorSlope2Base',
        'SmallHeavyBlockArmorSlope2Tip', 'SmallHeavyBlockArmorCorner2Base', 'SmallHeavyBlockArmorCorner2Tip',
        'SmallHeavyBlockArmorInvCorner2Base', 'SmallHeavyBlockArmorInvCorner2Tip', 'LargeHeavyHalfArmorBlock',
        'LargeHeavyHalfSlopeArmorBlock', 'SmallHeavyHalfArmorBlock', 'SmallHeavyHalfSlopeArmorBlock',
        'LargeArmorPanelHeavy', 'SmallArmorPanelHeavy', 'LargeHeavyArmorSlopedCorner',
        'LargeHeavyArmorSlopedCornerTip', 'LargeHeavyArmorSlopedCornerBase', 'SmallHeavyArmorSlopedCorner',
        'SmallHeavyArmorSlopedCornerTip', 'SmallHeavyArmorSlopedCornerBase'
    }
    
    def __init__(self):
        """Initialize the blueprint scanner."""
        self.blueprints_cache: List[BlueprintInfo] = []
    
    def get_default_blueprint_path(self) -> Path:
        """Get the default Space Engineers blueprint path."""
        appdata = os.getenv('APPDATA')
        if not appdata:
            raise RuntimeError("Could not find APPDATA directory")
        
        blueprint_path = Path(appdata) / 'SpaceEngineers' / 'Blueprints' / 'local'
        return blueprint_path
    
    def scan_blueprints(self, blueprint_dir: Optional[Path] = None) -> List[BlueprintInfo]:
        """
        Scan a directory for Space Engineers blueprints.
        
        Args:
            blueprint_dir: Directory to scan. If None, uses default SE directory.
        
        Returns:
            List of BlueprintInfo objects
        """
        if blueprint_dir is None:
            blueprint_dir = self.get_default_blueprint_path()
        
        blueprint_dir = Path(blueprint_dir)
        if not blueprint_dir.exists():
            raise FileNotFoundError(f"Blueprint directory not found: {blueprint_dir}")
        
        blueprints = []
        
        # Scan all subdirectories
        for item in blueprint_dir.iterdir():
            if item.is_dir():
                bp_file = item / 'bp.sbc'
                if bp_file.exists():
                    try:
                        bp_info = self._parse_blueprint(item, bp_file)
                        blueprints.append(bp_info)
                    except Exception as e:
                        # Skip blueprints that can't be parsed
                        print(f"Warning: Could not parse {item.name}: {e}")
                        continue
        
        self.blueprints_cache = blueprints
        return blueprints
    
    def _parse_blueprint(self, folder_path: Path, bp_file: Path) -> BlueprintInfo:
        """Parse a blueprint file and extract metadata."""
        tree = ET.parse(bp_file)
        root = tree.getroot()
        
        # Use folder name as display name (most reliable)
        # Space Engineers users typically name the folder, not the internal DisplayName
        display_name = folder_path.name
        
        # Extract grid size from first CubeGrid
        grid_size = 'Unknown'
        grid_size_elem = root.find('.//CubeGrid/GridSizeEnum')
        if grid_size_elem is not None and grid_size_elem.text:
            grid_size = grid_size_elem.text.strip()
        
        # Count blocks - IMPORTANT: Space Engineers uses SubtypeName not SubtypeId!
        blocks = root.findall('.//CubeGrid/CubeBlocks/MyObjectBuilder_CubeBlock')
        block_count = len(blocks)
        
        # Count light and heavy armor blocks
        light_armor_count = 0
        heavy_armor_count = 0
        
        for block in blocks:
            # Note: Space Engineers blueprints use <SubtypeName> not <SubtypeId>
            subtype_elem = block.find('SubtypeName')
            if subtype_elem is not None and subtype_elem.text:
                subtype = subtype_elem.text.strip()
                if subtype in self.LIGHT_ARMOR_BLOCKS:
                    light_armor_count += 1
                elif subtype in self.HEAVY_ARMOR_BLOCKS:
                    heavy_armor_count += 1
        
        return BlueprintInfo(
            name=folder_path.name,
            path=folder_path,
            display_name=display_name,
            grid_size=grid_size,
            block_count=block_count,
            light_armor_count=light_armor_count,
            heavy_armor_count=heavy_armor_count,
            has_bp_file=True
        )
    
    def get_blueprint_by_name(self, name: str) -> Optional[BlueprintInfo]:
        """Get a blueprint by its folder name."""
        for bp in self.blueprints_cache:
            if bp.name == name:
                return bp
        return None
    
    def filter_blueprints(self, search_term: str = "", 
                         min_light_armor: int = 0) -> List[BlueprintInfo]:
        """
        Filter cached blueprints by search term and minimum light armor count.
        
        Args:
            search_term: Search in blueprint name/display name
            min_light_armor: Minimum number of light armor blocks
        
        Returns:
            Filtered list of BlueprintInfo objects
        """
        filtered = []
        search_lower = search_term.lower()
        
        for bp in self.blueprints_cache:
            # Check light armor count
            if bp.light_armor_count < min_light_armor:
                continue
            
            # Check search term
            if search_term and search_lower not in bp.name.lower() and \
               search_lower not in bp.display_name.lower():
                continue
            
            filtered.append(bp)
        
        return filtered
