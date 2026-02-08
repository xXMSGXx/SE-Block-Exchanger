"""
Progress Ring Widget
Animated circular progress indicator for conversion operations.
"""

from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

from ui.theme import TacticalTheme


class ProgressRing(ctk.CTkFrame):
    """Circular progress indicator with status text."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._animating = False
        self._angle = 0
        self._after_id = None

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x")

        self._canvas = tk.Canvas(
            row,
            width=44,
            height=44,
            bg=TacticalTheme.BG_MEDIUM,
            highlightthickness=0,
        )
        self._canvas.pack(side="left", padx=(0, 8))

        self._track = self._canvas.create_oval(
            4,
            4,
            40,
            40,
            outline=TacticalTheme.BG_DARK,
            width=5,
        )
        self._arc = self._canvas.create_arc(
            4,
            4,
            40,
            40,
            start=90,
            extent=0,
            style=tk.ARC,
            outline=TacticalTheme.CYAN_PRIMARY,
            width=5,
        )

        text_column = ctk.CTkFrame(row, fg_color="transparent")
        text_column.pack(side="left", fill="both", expand=True)
        self._label = ctk.CTkLabel(
            text_column,
            text="",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.TEXT_GRAY,
            anchor="w",
            justify="left",
        )
        self._label.pack(fill="x")
        self._value_label = ctk.CTkLabel(
            text_column,
            text="",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.CYAN_PRIMARY,
            anchor="w",
            justify="left",
        )
        self._value_label.pack(fill="x")
        self.pack_forget()

    def _tick(self):
        if not self._animating:
            return
        self._angle = (self._angle + 12) % 360
        self._canvas.itemconfigure(self._arc, start=self._angle, extent=100)
        self._after_id = self.after(35, self._tick)

    def start_indeterminate(self, text: str = "Processing..."):
        self.stop()
        self._label.configure(text=text)
        self._value_label.configure(text="Working...")
        self._canvas.itemconfigure(self._arc, outline=TacticalTheme.CYAN_PRIMARY)
        self._animating = True
        self.pack(fill="x", pady=4)
        self._tick()

    def set_progress(self, value: float, text: str = ""):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        self._animating = False
        value = max(0.0, min(1.0, float(value)))
        if text:
            self._label.configure(text=text)
        self._value_label.configure(text=f"{int(value * 100)}%")
        self._canvas.itemconfigure(self._arc, start=90, extent=-(360 * value))
        self._canvas.itemconfigure(self._arc, outline=TacticalTheme.GREEN_PRIMARY)
        self.pack(fill="x", pady=4)

    def stop(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        self._animating = False
        self._canvas.itemconfigure(self._arc, start=90, extent=0, outline=TacticalTheme.CYAN_PRIMARY)
        self._label.configure(text="")
        self._value_label.configure(text="")
        self.pack_forget()

