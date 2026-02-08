"""Tactical Command Theme System."""

from __future__ import annotations

import customtkinter as ctk


class TacticalTheme:
    """Tactical hologram color scheme and styling constants."""

    APPEARANCE_MODES = ("Light", "Dark", "System")

    BG_DARK = "#0f172a"
    BG_MEDIUM = "#1e293b"
    BG_GLASS = "#1a2332"
    BG_CARD = "#162033"
    CYAN_PRIMARY = "#06b6d4"
    CYAN_DIM = "#0891b2"
    ORANGE_PRIMARY = "#f59e0b"
    ORANGE_DIM = "#d97706"
    TEXT_CYAN = "#67e8f9"
    TEXT_GRAY = "#94a3b8"
    TEXT_WHITE = "#e2e8f0"
    BORDER_CYAN = "#22d3ee"
    BORDER_ORANGE = "#fb923c"
    GREEN_PRIMARY = "#22c55e"
    RED_PRIMARY = "#ef4444"

    FONT_FAMILY = "Courier New"
    FONT_SMALL = ("Courier New", 9)
    FONT_NORMAL = ("Courier New", 10)
    FONT_LARGE = ("Courier New", 12, "bold")
    FONT_TITLE = ("Courier New", 14, "bold")
    FONT_HEADER = ("Courier New", 16, "bold")

    @classmethod
    def normalize_appearance_mode(cls, mode: str) -> str:
        if not mode:
            return "System"
        normalized = mode.strip().capitalize()
        return normalized if normalized in cls.APPEARANCE_MODES else "System"

    @classmethod
    def apply(cls, appearance_mode: str = "System") -> None:
        """Configure CustomTkinter appearance for tactical theme."""
        ctk.set_appearance_mode(cls.normalize_appearance_mode(appearance_mode))
        ctk.set_default_color_theme("dark-blue")
