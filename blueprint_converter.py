"""
Blueprint Converter Module
Handles safe copying and conversion of Space Engineers blueprints
"""

import shutil
from pathlib import Path
from typing import Tuple
from se_armor_replacer import ArmorBlockReplacer


class BlueprintConverter:
    """Converts blueprints by copying and applying armor replacements (light to heavy or heavy to light)."""
    
    HEAVYARMOR_PREFIX = "HEAVYARMOR_"
    LIGHTARMOR_PREFIX = "LIGHTARMOR_"
    
    def __init__(self, verbose: bool = False, reverse: bool = False):
        """
        Initialize the blueprint converter.
        
        Args:
            verbose: Enable detailed logging
            reverse: If True, converts heavy to light instead of light to heavy
        """
        self.replacer = ArmorBlockReplacer(verbose=verbose, reverse=reverse)
        self.verbose = verbose
        self.reverse = reverse
        self.prefix = self.LIGHTARMOR_PREFIX if reverse else self.HEAVYARMOR_PREFIX
    
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[CONVERTER] {message}")
    
    def create_heavy_armor_blueprint(self, source_path: Path) -> Tuple[Path, int, int]:
        """
        Create a new blueprint with converted armor blocks.
        Creates HEAVYARMOR_ prefix for light->heavy, LIGHTARMOR_ for heavy->light.
        
        Args:
            source_path: Path to the source blueprint directory
        
        Returns:
            Tuple of (new_blueprint_path, blocks_scanned, replacements_made)
        
        Raises:
            FileNotFoundError: If source blueprint doesn't exist
            ValueError: If source is not a valid blueprint directory
        """
        source_path = Path(source_path)
        
        # Validate source
        if not source_path.exists():
            raise FileNotFoundError(f"Source blueprint not found: {source_path}")
        
        if not source_path.is_dir():
            raise ValueError(f"Source must be a directory: {source_path}")
        
        bp_file = source_path / 'bp.sbc'
        if not bp_file.exists():
            raise ValueError(f"No bp.sbc found in: {source_path}")
        
        # Create destination path
        dest_name = self.prefix + source_path.name
        dest_path = source_path.parent / dest_name
        
        # Check if destination already exists
        if dest_path.exists():
            self.log(f"Destination already exists, removing: {dest_path}")
            shutil.rmtree(dest_path)
        
        # Copy entire blueprint directory
        self.log(f"Copying blueprint: {source_path.name} -> {dest_name}")
        shutil.copytree(source_path, dest_path)
        
        # Convert armor blocks in the new copy
        new_bp_file = dest_path / 'bp.sbc'
        self.log(f"Converting armor blocks in: {new_bp_file}")
        
        blocks_scanned, replacements = self.replacer.process_blueprint(
            str(new_bp_file),
            create_backup=False  # No backup needed since it's a copy
        )
        
        self.log(f"Conversion complete: {replacements} blocks converted")
        
        return dest_path, blocks_scanned, replacements
    
    def get_destination_path(self, source_path: Path) -> Path:
        """Get the destination path for a given source blueprint."""
        source_path = Path(source_path)
        dest_name = self.prefix + source_path.name
        return source_path.parent / dest_name
    
    def check_destination_exists(self, source_path: Path) -> bool:
        """Check if a converted version already exists."""
        dest_path = self.get_destination_path(source_path)
        return dest_path.exists()
    
    def delete_heavy_armor_blueprint(self, source_path: Path) -> bool:
        """
        Delete the converted version of a blueprint if it exists.
        
        Args:
            source_path: Path to the source blueprint directory
        
        Returns:
            True if deleted, False if didn't exist
        """
        dest_path = self.get_destination_path(source_path)
        if dest_path.exists():
            self.log(f"Deleting: {dest_path}")
            shutil.rmtree(dest_path)
            return True
        return False
