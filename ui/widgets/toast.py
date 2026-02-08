"""
Toast Notification Widget
Non-blocking slide-in notifications that auto-dismiss
"""

import customtkinter as ctk
from ui.theme import TacticalTheme


class Toast(ctk.CTkFrame):
    """A single toast notification that slides in and auto-dismisses."""

    def __init__(self, master, message: str, level: str = "info", duration: int = 3000):
        super().__init__(
            master,
            fg_color=TacticalTheme.BG_GLASS,
            border_width=1,
            border_color=self._get_border_color(level),
            corner_radius=6,
        )
        self._duration = duration
        self._after_id = None

        # Color bar on the left
        bar = ctk.CTkFrame(
            self, width=4, corner_radius=0,
            fg_color=self._get_border_color(level),
        )
        bar.pack(side="left", fill="y", padx=(0, 8), pady=2)

        # Message
        ctk.CTkLabel(
            self, text=message,
            font=TacticalTheme.FONT_NORMAL,
            text_color=TacticalTheme.TEXT_CYAN,
            wraplength=350,
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=(0, 8), pady=8)

        # Close button
        close_btn = ctk.CTkButton(
            self, text="X", width=24, height=24,
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            hover_color=TacticalTheme.BG_MEDIUM,
            text_color=TacticalTheme.TEXT_GRAY,
            command=self.dismiss,
        )
        close_btn.pack(side="right", padx=4, pady=4)

    @staticmethod
    def _get_border_color(level: str) -> str:
        colors = {
            "info": TacticalTheme.CYAN_PRIMARY,
            "success": TacticalTheme.GREEN_PRIMARY,
            "warning": TacticalTheme.ORANGE_PRIMARY,
            "error": TacticalTheme.RED_PRIMARY,
        }
        return colors.get(level, TacticalTheme.CYAN_PRIMARY)

    def show(self):
        """Display the toast and schedule auto-dismiss."""
        self.pack(fill="x", padx=10, pady=(0, 4))
        self.lift()
        self._after_id = self.after(self._duration, self.dismiss)

    def dismiss(self):
        """Remove the toast."""
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.pack_forget()
        self.destroy()


class ToastManager:
    """Manages a stack of toast notifications anchored to a parent widget."""

    def __init__(self, parent):
        self._parent = parent
        self._container = ctk.CTkFrame(parent, fg_color="transparent")
        # Position at top-right as an overlay
        self._container.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        self._container.configure(width=400)
        self._container.lift()

    def toast(self, message: str, level: str = "info", duration: int = 3000):
        """Show a new toast notification."""
        t = Toast(self._container, message, level, duration)
        t.show()
