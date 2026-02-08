"""
Blueprint Converter Module
Handles safe copying and block conversion of Space Engineers blueprints.
"""

import shutil
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from se_armor_replacer import ArmorBlockReplacer


class BlueprintConverter:
    """Converts blueprints by copying and applying selected mapping categories."""

    HEAVYARMOR_PREFIX = "HEAVYARMOR_"
    LIGHTARMOR_PREFIX = "LIGHTARMOR_"
    CONVERTED_PREFIX = "CONVERTED_"
    REVERSED_PREFIX = "REVERSED_"

    def __init__(
        self,
        verbose: bool = False,
        reverse: bool = False,
        enabled_categories: Optional[Sequence[str]] = None,
        include_profiles: bool = True,
        profile_dir: Path = Path("profiles"),
    ):
        self.verbose = verbose
        self.reverse = reverse
        self.enabled_categories = list(enabled_categories) if enabled_categories else ["armor"]
        self.replacer = ArmorBlockReplacer(
            verbose=verbose,
            reverse=reverse,
            enabled_categories=self.enabled_categories,
            include_profiles=include_profiles,
            profile_dir=profile_dir,
        )
        self.prefix = self._select_prefix()
        self._history: List[Path] = []

    def _select_prefix(self) -> str:
        normalized = [name.lower() for name in self.enabled_categories]
        only_armor = normalized == ["armor"]
        if only_armor and not self.reverse:
            return self.HEAVYARMOR_PREFIX
        if only_armor and self.reverse:
            return self.LIGHTARMOR_PREFIX
        return self.REVERSED_PREFIX if self.reverse else self.CONVERTED_PREFIX

    def log(self, message: str) -> None:
        if self.verbose:
            print(f"[CONVERTER] {message}")

    def create_converted_blueprint(self, source_path: Path) -> Tuple[Path, int, int]:
        """
        Create a new blueprint folder with converted blocks.
        """
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source blueprint not found: {source_path}")
        if not source_path.is_dir():
            raise ValueError(f"Source must be a directory: {source_path}")

        bp_file = source_path / "bp.sbc"
        if not bp_file.exists():
            raise ValueError(f"No bp.sbc found in: {source_path}")

        dest_path = self.get_destination_path(source_path)
        if dest_path.exists():
            self.log(f"Destination exists, removing: {dest_path}")
            shutil.rmtree(dest_path)

        self.log(f"Copying blueprint folder: {source_path.name} -> {dest_path.name}")
        shutil.copytree(source_path, dest_path)

        binary_bp_file = dest_path / "bp.sbcB5"
        if binary_bp_file.exists():
            self.log(f"Removing binary blueprint cache: {binary_bp_file}")
            binary_bp_file.unlink()

        new_bp_file = dest_path / "bp.sbc"
        blocks_scanned, replacements = self.replacer.process_blueprint(
            str(new_bp_file),
            create_backup=False,
        )
        self.log(f"Conversion complete ({replacements} replacement(s))")
        self._history.append(dest_path)
        return dest_path, blocks_scanned, replacements

    def create_heavy_armor_blueprint(self, source_path: Path) -> Tuple[Path, int, int]:
        """
        Backward-compatible wrapper for existing callers.
        """
        return self.create_converted_blueprint(source_path)

    def get_destination_path(self, source_path: Path) -> Path:
        source_path = Path(source_path)
        return source_path.parent / f"{self.prefix}{source_path.name}"

    def check_destination_exists(self, source_path: Path) -> bool:
        return self.get_destination_path(source_path).exists()

    def delete_heavy_armor_blueprint(self, source_path: Path) -> bool:
        """
        Backward-compatible delete method.
        """
        return self.delete_converted_blueprint(source_path)

    def delete_converted_blueprint(self, source_path: Path) -> bool:
        dest_path = self.get_destination_path(source_path)
        if dest_path.exists():
            self.log(f"Deleting converted blueprint: {dest_path}")
            shutil.rmtree(dest_path)
            return True
        return False

    def undo_last_conversion(self) -> Optional[Path]:
        """
        Delete the most recently created converted blueprint, if present.
        """
        while self._history:
            path = self._history.pop()
            if path.exists():
                shutil.rmtree(path)
                self.log(f"Undo conversion: removed {path}")
                return path
        return None

