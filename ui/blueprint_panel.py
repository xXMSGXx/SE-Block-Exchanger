"""
Blueprint Panel Component
Left panel with searchable blueprint card list
"""

import customtkinter as ctk
from typing import List, Optional, Callable
from ui.theme import TacticalTheme
from ui.widgets.blueprint_card import BlueprintCard


class BlueprintPanel(ctk.CTkFrame):
    """Left panel containing search bar and scrollable blueprint card list."""

    def __init__(
        self,
        master,
        on_select: Optional[Callable] = None,
        on_recent_select: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            border_color=TacticalTheme.CYAN_PRIMARY,
            corner_radius=8,
            **kwargs,
        )
        self._on_select = on_select
        self._on_recent_select = on_recent_select
        self._cards: List[BlueprintCard] = []
        self._blueprints = []
        self._selected_indices: set = set()
        self._recent_lookup = {}

        # Header
        ctk.CTkLabel(
            self, text=">> BLUEPRINT DATABASE",
            font=TacticalTheme.FONT_LARGE,
            text_color=TacticalTheme.ORANGE_PRIMARY,
        ).pack(pady=(12, 8))

        recent_row = ctk.CTkFrame(self, fg_color="transparent")
        recent_row.pack(fill="x", padx=10, pady=(0, 6))

        ctk.CTkLabel(
            recent_row,
            text="RECENT:",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.TEXT_GRAY,
        ).pack(side="left", padx=(0, 6))

        self.recent_var = ctk.StringVar(value="(none)")
        self.recent_menu = ctk.CTkOptionMenu(
            recent_row,
            values=["(none)"],
            variable=self.recent_var,
            width=230,
            fg_color=TacticalTheme.BG_DARK,
            button_color=TacticalTheme.BG_GLASS,
            button_hover_color=TacticalTheme.CYAN_DIM,
            dropdown_fg_color=TacticalTheme.BG_MEDIUM,
            dropdown_hover_color=TacticalTheme.BG_GLASS,
            text_color=TacticalTheme.TEXT_CYAN,
            font=TacticalTheme.FONT_SMALL,
            command=self._on_recent_picked,
        )
        self.recent_menu.pack(side="left", fill="x", expand=True)

        # Search box
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._on_search())

        self._search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="SEARCH BLUEPRINTS...",
            font=TacticalTheme.FONT_NORMAL,
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color=TacticalTheme.BG_DARK,
            border_color=TacticalTheme.CYAN_DIM,
            placeholder_text_color=TacticalTheme.TEXT_GRAY,
            height=32,
        )
        self._search_entry.pack(fill="x")

        # Scrollable card container
        self._scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=TacticalTheme.BG_DARK,
            border_width=1,
            border_color=TacticalTheme.BG_MEDIUM,
            corner_radius=4,
        )
        self._scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def set_blueprints(self, blueprints):
        """Populate the card list with blueprint data."""
        self._blueprints = blueprints
        self._selected_indices.clear()
        self._rebuild_cards(blueprints)

    def _rebuild_cards(self, blueprints):
        """Rebuild all card widgets."""
        # Clear existing cards
        for card in self._cards:
            card.destroy()
        self._cards.clear()

        if not blueprints:
            ctk.CTkLabel(
                self._scroll_frame,
                text="NO BLUEPRINTS FOUND",
                font=TacticalTheme.FONT_NORMAL,
                text_color=TacticalTheme.TEXT_GRAY,
            ).pack(pady=20)
            return

        for i, bp in enumerate(blueprints):
            card = BlueprintCard(
                self._scroll_frame, bp, i,
                on_select=self._handle_card_select,
            )
            card.pack(fill="x", padx=4, pady=2)
            self._cards.append(card)

    def _handle_card_select(self, index: int, multi: bool = False):
        """Handle card selection, supporting multi-select with Ctrl."""
        if multi:
            if index in self._selected_indices:
                self._selected_indices.discard(index)
            else:
                self._selected_indices.add(index)
        else:
            self._selected_indices = {index}

        # Update card visuals
        for i, card in enumerate(self._cards):
            card.set_selected(i in self._selected_indices)

        # Notify parent of primary selection (last clicked)
        visible = self._get_visible_blueprints()
        if index < len(visible) and self._on_select:
            self._on_select(visible[index])

    def _on_search(self):
        """Filter cards based on search text."""
        search = self.search_var.get().lower()
        if not search:
            self._rebuild_cards(self._blueprints)
            return

        filtered = [
            bp for bp in self._blueprints
            if search in bp.name.lower() or search in bp.display_name.lower()
        ]
        self._selected_indices.clear()
        self._rebuild_cards(filtered)

    def _get_visible_blueprints(self):
        """Return the currently visible (possibly filtered) blueprints."""
        search = self.search_var.get().lower()
        if not search:
            return self._blueprints
        return [
            bp for bp in self._blueprints
            if search in bp.name.lower() or search in bp.display_name.lower()
        ]

    def get_selected_blueprints(self):
        """Return list of currently selected blueprint infos."""
        visible = self._get_visible_blueprints()
        return [visible[i] for i in sorted(self._selected_indices) if i < len(visible)]

    def get_selected_count(self) -> int:
        return len(self._selected_indices)

    def set_recent_blueprints(self, blueprint_names: List[str]):
        values = ["(none)"]
        self._recent_lookup = {}
        for idx, name in enumerate(blueprint_names):
            key = f"{idx + 1}. {name}"
            self._recent_lookup[key] = name
            values.append(key)
        self.recent_menu.configure(values=values)
        self.recent_var.set(values[0])

    def _on_recent_picked(self, value: str):
        if value == "(none)":
            return
        name = self._recent_lookup.get(value)
        if not name:
            return
        self.select_blueprint_by_name(name)
        if self._on_recent_select:
            self._on_recent_select(name)

    def select_blueprint_by_name(self, name: str) -> bool:
        visible = self._get_visible_blueprints()
        for idx, bp in enumerate(visible):
            if bp.display_name == name or bp.name == name:
                self._handle_card_select(idx, multi=False)
                return True
        return False
