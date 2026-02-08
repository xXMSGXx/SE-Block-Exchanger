"""Header component."""

import os
import customtkinter as ctk
from ui.theme import TacticalTheme


def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller."""
    import sys
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, relative_path)


class Header(ctk.CTkFrame):
    """Header bar with branding, status indicator, and action buttons."""

    def __init__(
        self,
        master,
        on_rescan=None,
        on_browse=None,
        on_appearance_change=None,
        on_recent_dir_select=None,
        on_open_profiles=None,
        on_show_changelog=None,
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
        self._on_rescan = on_rescan
        self._on_browse = on_browse
        self._on_appearance_change = on_appearance_change
        self._on_recent_dir_select = on_recent_dir_select
        self._on_open_profiles = on_open_profiles
        self._on_show_changelog = on_show_changelog
        self._recent_lookup = {}

        # --- Left side: brand block ---
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.pack(side="left", padx=(10, 0), pady=8)

        # Logo image
        self._logo_image = None
        try:
            from PIL import Image
            logo_path = get_resource_path('logo.png')
            if not os.path.exists(logo_path):
                logo_path = get_resource_path('app_icon.png')
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                target_h = 60
                aspect = img.width / img.height
                target_w = int(target_h * aspect)
                self._logo_image = ctk.CTkImage(
                    light_image=img, dark_image=img,
                    size=(target_w, target_h),
                )
                logo_label = ctk.CTkLabel(
                    brand_frame, image=self._logo_image, text="",
                )
                logo_label.pack(side="left", padx=(0, 10))
        except Exception:
            pass  # Pillow not installed or image missing

        # Title block
        title_block = ctk.CTkFrame(brand_frame, fg_color="transparent")
        title_block.pack(side="left", fill="y")

        # Status indicator row
        status_row = ctk.CTkFrame(title_block, fg_color="transparent")
        status_row.pack(anchor="w")

        self._led = ctk.CTkLabel(
            status_row, text="\u2022", width=16,
            font=("Courier New", 14),
            text_color=TacticalTheme.GREEN_PRIMARY,
        )
        self._led.pack(side="left")

        ctk.CTkLabel(
            status_row, text="SYSTEM ACTIVE",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).pack(side="left", padx=(2, 0))

        # Title
        ctk.CTkLabel(
            title_block,
            text="SE BLOCK EXCHANGER // TACTICAL COMMAND CENTER",
            font=TacticalTheme.FONT_TITLE,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).pack(anchor="w", pady=(2, 0))

        # Subtitle
        ctk.CTkLabel(
            title_block, text="DEVELOPED BY MERABY LABS",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.TEXT_GRAY,
        ).pack(anchor="w")

        # --- Right side: action buttons ---
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(side="right", padx=10, pady=8)

        # Blueprint count
        self.bp_count_label = ctk.CTkLabel(
            actions, text="BLUEPRINTS: --",
            font=TacticalTheme.FONT_NORMAL,
            text_color=TacticalTheme.CYAN_PRIMARY,
        )
        self.bp_count_label.pack(side="left", padx=(0, 12))

        self.recent_var = ctk.StringVar(value="RECENT DIRS")
        self.recent_menu = ctk.CTkOptionMenu(
            actions,
            values=["RECENT DIRS"],
            variable=self.recent_var,
            font=TacticalTheme.FONT_SMALL,
            fg_color=TacticalTheme.BG_DARK,
            button_color=TacticalTheme.BG_GLASS,
            button_hover_color=TacticalTheme.CYAN_DIM,
            dropdown_fg_color=TacticalTheme.BG_MEDIUM,
            dropdown_hover_color=TacticalTheme.BG_GLASS,
            text_color=TacticalTheme.TEXT_CYAN,
            width=160,
            command=self._on_recent_selected,
        )
        self.recent_menu.pack(side="left", padx=4)

        self.appearance_var = ctk.StringVar(value="System")
        self.appearance_menu = ctk.CTkOptionMenu(
            actions,
            values=list(TacticalTheme.APPEARANCE_MODES),
            variable=self.appearance_var,
            font=TacticalTheme.FONT_SMALL,
            fg_color=TacticalTheme.BG_DARK,
            button_color=TacticalTheme.BG_GLASS,
            button_hover_color=TacticalTheme.CYAN_DIM,
            dropdown_fg_color=TacticalTheme.BG_MEDIUM,
            dropdown_hover_color=TacticalTheme.BG_GLASS,
            text_color=TacticalTheme.TEXT_CYAN,
            width=110,
            command=self._on_appearance_changed,
        )
        self.appearance_menu.pack(side="left", padx=4)

        # Browse button
        ctk.CTkButton(
            actions, text="BROWSE",
            font=TacticalTheme.FONT_NORMAL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.CYAN_PRIMARY,
            text_color=TacticalTheme.CYAN_PRIMARY,
            hover_color=TacticalTheme.BG_DARK,
            width=90, height=32,
            command=self._on_browse,
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            actions, text="PROFILES",
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.GREEN_PRIMARY,
            text_color=TacticalTheme.GREEN_PRIMARY,
            hover_color=TacticalTheme.BG_DARK,
            width=96, height=32,
            command=self._on_open_profiles,
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            actions, text="CHANGELOG",
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.ORANGE_PRIMARY,
            text_color=TacticalTheme.ORANGE_PRIMARY,
            hover_color=TacticalTheme.BG_DARK,
            width=98, height=32,
            command=self._on_show_changelog,
        ).pack(side="left", padx=4)

        # Rescan button
        ctk.CTkButton(
            actions, text="RESCAN",
            font=TacticalTheme.FONT_NORMAL,
            fg_color=TacticalTheme.CYAN_PRIMARY,
            text_color=TacticalTheme.BG_DARK,
            hover_color=TacticalTheme.CYAN_DIM,
            width=90, height=32,
            command=self._on_rescan,
        ).pack(side="left", padx=4)

    def set_blueprint_count(self, count: int):
        self.bp_count_label.configure(text=f"BLUEPRINTS: {count}")

    def set_recent_dirs(self, directories):
        values = ["RECENT DIRS"]
        self._recent_lookup = {}
        for idx, directory in enumerate(directories):
            short_name = directory
            if len(short_name) > 48:
                short_name = "..." + short_name[-45:]
            key = f"{idx + 1}. {short_name}"
            self._recent_lookup[key] = directory
            values.append(key)
        self.recent_menu.configure(values=values)
        self.recent_var.set(values[0])

    def set_appearance_mode(self, mode: str):
        self.appearance_var.set(TacticalTheme.normalize_appearance_mode(mode))

    def _on_recent_selected(self, value: str):
        if value == "RECENT DIRS":
            return
        directory = self._recent_lookup.get(value)
        if directory and self._on_recent_dir_select:
            self._on_recent_dir_select(directory)

    def _on_appearance_changed(self, mode: str):
        if self._on_appearance_change:
            self._on_appearance_change(mode)
