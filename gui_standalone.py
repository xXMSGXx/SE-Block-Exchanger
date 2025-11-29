"""
Space Engineers Block Exchanger - Standalone Desktop Application
Tactical Command Center GUI using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from pathlib import Path
from typing import Optional
import sys

from blueprint_scanner import BlueprintScanner, BlueprintInfo
from blueprint_converter import BlueprintConverter


class TacticalTheme:
    """Tactical hologram color scheme and styling constants."""
    
    # Colors
    BG_DARK = "#0f172a"           # Deep gunmetal
    BG_MEDIUM = "#1e293b"         # Medium slate
    BG_GLASS = "#1a2332"          # Tech-glass
    CYAN_PRIMARY = "#06b6d4"      # Neon cyan
    CYAN_DIM = "#0891b2"          # Dimmed cyan
    ORANGE_PRIMARY = "#f59e0b"    # Industrial orange
    ORANGE_DIM = "#d97706"        # Dimmed orange
    TEXT_CYAN = "#67e8f9"         # Light cyan text
    TEXT_GRAY = "#94a3b8"         # Gray text
    BORDER_CYAN = "#22d3ee"       # Cyan border
    BORDER_ORANGE = "#fb923c"     # Orange border
    
    # Font
    FONT_FAMILY = "Courier New"   # Monospace
    FONT_SMALL = ("Courier New", 9)
    FONT_NORMAL = ("Courier New", 10)
    FONT_LARGE = ("Courier New", 12, "bold")
    FONT_TITLE = ("Courier New", 14, "bold")


class TacticalCommandCenter(tk.Tk):
    """Main application window with tactical hologram interface."""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("SE BLOCK EXCHANGER // TACTICAL COMMAND CENTER")
        self.geometry("1200x800")
        self.configure(bg=TacticalTheme.BG_DARK)
        
        # Initialize services
        self.scanner = BlueprintScanner()
        self.converter = BlueprintConverter(verbose=True)
        self.selected_blueprint: Optional[BlueprintInfo] = None
        self.blueprints = []
        
        # Build UI
        self.create_widgets()
        
        # Load blueprints
        self.after(100, self.load_blueprints_async)
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all UI widgets."""
        
        # Header Frame
        self.create_header()
        
        # Main content area
        main_frame = tk.Frame(self, bg=TacticalTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel - Blueprint Selector
        self.create_blueprint_panel(main_frame)
        
        # Right Panel - Details and Conversion
        self.create_conversion_panel(main_frame)
        
        # Footer - Status Bar
        self.create_footer()
    
    def create_header(self):
        """Create the header with system status."""
        header = tk.Frame(self, bg=TacticalTheme.BG_MEDIUM, 
                         highlightbackground=TacticalTheme.CYAN_PRIMARY,
                         highlightthickness=2)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        # Status indicator
        status_frame = tk.Frame(header, bg=TacticalTheme.BG_MEDIUM)
        status_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # LED indicator (canvas for colored circle)
        led = tk.Canvas(status_frame, width=12, height=12, 
                       bg=TacticalTheme.BG_MEDIUM, highlightthickness=0)
        led.pack(side=tk.LEFT, padx=(0, 5))
        led.create_oval(2, 2, 10, 10, fill=TacticalTheme.CYAN_PRIMARY, outline="")
        
        tk.Label(status_frame, text="SYSTEM ACTIVE",
                font=TacticalTheme.FONT_SMALL,
                fg=TacticalTheme.CYAN_PRIMARY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.LEFT)
        
        # Title
        tk.Label(header, text="SE BLOCK EXCHANGER // TACTICAL COMMAND CENTER",
                font=TacticalTheme.FONT_TITLE,
                fg=TacticalTheme.CYAN_PRIMARY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.LEFT, padx=20)
        
        # Rescan button
        rescan_btn = tk.Button(header, text="[ RESCAN ]",
                              font=TacticalTheme.FONT_NORMAL,
                              fg=TacticalTheme.CYAN_PRIMARY,
                              bg=TacticalTheme.BG_DARK,
                              activeforeground=TacticalTheme.ORANGE_PRIMARY,
                              activebackground=TacticalTheme.BG_MEDIUM,
                              relief=tk.FLAT,
                              cursor="hand2",
                              command=self.load_blueprints_async)
        rescan_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Blueprint count
        self.bp_count_label = tk.Label(header, text="BLUEPRINTS: --",
                                      font=TacticalTheme.FONT_NORMAL,
                                      fg=TacticalTheme.CYAN_PRIMARY,
                                      bg=TacticalTheme.BG_MEDIUM)
        self.bp_count_label.pack(side=tk.RIGHT, padx=10)
    
    def create_blueprint_panel(self, parent):
        """Create the left panel with blueprint list."""
        panel = tk.Frame(parent, bg=TacticalTheme.BG_MEDIUM,
                        highlightbackground=TacticalTheme.CYAN_PRIMARY,
                        highlightthickness=2)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, 
                  padx=(0, 5), ipadx=10, ipady=10)
        panel.config(width=350)
        
        # Header
        tk.Label(panel, text=">> BLUEPRINT DATABASE",
                font=TacticalTheme.FONT_LARGE,
                fg=TacticalTheme.ORANGE_PRIMARY,
                bg=TacticalTheme.BG_MEDIUM).pack(pady=10)
        
        # Search box
        search_frame = tk.Frame(panel, bg=TacticalTheme.BG_MEDIUM)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_blueprints())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=TacticalTheme.FONT_NORMAL,
                               fg=TacticalTheme.TEXT_CYAN,
                               bg=TacticalTheme.BG_DARK,
                               insertbackground=TacticalTheme.CYAN_PRIMARY,
                               relief=tk.FLAT,
                               highlightbackground=TacticalTheme.CYAN_PRIMARY,
                               highlightthickness=1)
        search_entry.pack(fill=tk.X, ipady=5)
        search_entry.insert(0, "SEARCH BLUEPRINTS...")
        search_entry.config(fg=TacticalTheme.TEXT_GRAY)
        
        # Bind focus events for placeholder
        def on_focus_in(event):
            if search_entry.get() == "SEARCH BLUEPRINTS...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=TacticalTheme.TEXT_CYAN)
        
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "SEARCH BLUEPRINTS...")
                search_entry.config(fg=TacticalTheme.TEXT_GRAY)
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Blueprint listbox
        list_frame = tk.Frame(panel, bg=TacticalTheme.BG_DARK)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.bp_listbox = tk.Listbox(list_frame,
                                     font=TacticalTheme.FONT_SMALL,
                                     fg=TacticalTheme.TEXT_CYAN,
                                     bg=TacticalTheme.BG_DARK,
                                     selectbackground=TacticalTheme.ORANGE_PRIMARY,
                                     selectforeground=TacticalTheme.BG_DARK,
                                     activestyle='none',
                                     relief=tk.FLAT,
                                     yscrollcommand=scrollbar.set)
        self.bp_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.bp_listbox.yview)
        
        self.bp_listbox.bind('<<ListboxSelect>>', self.on_blueprint_select)
    
    def create_conversion_panel(self, parent):
        """Create the right panel with details and conversion."""
        panel = tk.Frame(parent, bg=TacticalTheme.BG_MEDIUM,
                        highlightbackground=TacticalTheme.CYAN_PRIMARY,
                        highlightthickness=2)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                  ipadx=10, ipady=10)
        
        # Details section
        self.create_details_section(panel)
        
        # Exchange visualization
        self.create_exchange_section(panel)
        
        # Conversion button
        self.create_conversion_button(panel)
    
    def create_details_section(self, parent):
        """Create blueprint details section."""
        details_frame = tk.Frame(parent, bg=TacticalTheme.BG_GLASS,
                                highlightbackground=TacticalTheme.CYAN_DIM,
                                highlightthickness=1)
        details_frame.pack(fill=tk.X, padx=10, pady=10, ipady=10)
        
        tk.Label(details_frame, text=">> SELECTED BLUEPRINT",
                font=TacticalTheme.FONT_LARGE,
                fg=TacticalTheme.ORANGE_PRIMARY,
                bg=TacticalTheme.BG_GLASS).pack(pady=5)
        
        # Details grid
        info_frame = tk.Frame(details_frame, bg=TacticalTheme.BG_GLASS)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create labels for details
        self.detail_labels = {}
        fields = [
            ("NAME:", "name"),
            ("GRID SIZE:", "grid"),
            ("TOTAL BLOCKS:", "blocks"),
            ("LIGHT ARMOR:", "light_armor"),
            ("HEAVY ARMOR:", "heavy_armor")
        ]
        
        for i, (label_text, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(info_frame, text=label_text,
                    font=TacticalTheme.FONT_SMALL,
                    fg=TacticalTheme.TEXT_GRAY,
                    bg=TacticalTheme.BG_GLASS).grid(row=row, column=col, 
                                                    sticky=tk.W, padx=10, pady=5)
            
            value_label = tk.Label(info_frame, text="--",
                                  font=TacticalTheme.FONT_NORMAL,
                                  fg=TacticalTheme.CYAN_PRIMARY if key not in ["light_armor", "heavy_armor"] else (
                                      TacticalTheme.ORANGE_PRIMARY if key == "light_armor" else TacticalTheme.CYAN_PRIMARY
                                  ),
                                  bg=TacticalTheme.BG_GLASS)
            value_label.grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=5)
            self.detail_labels[key] = value_label
    
    def create_exchange_section(self, parent):
        """Create the exchange visualization section."""
        exchange_frame = tk.Frame(parent, bg=TacticalTheme.BG_GLASS,
                                 highlightbackground=TacticalTheme.CYAN_DIM,
                                 highlightthickness=1)
        exchange_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(exchange_frame, text=">> ARMOR EXCHANGE PROCESS",
                font=TacticalTheme.FONT_LARGE,
                fg=TacticalTheme.ORANGE_PRIMARY,
                bg=TacticalTheme.BG_GLASS).pack(pady=10)
        
        # Three columns: Standard, Arrow, Heavy
        cols_frame = tk.Frame(exchange_frame, bg=TacticalTheme.BG_GLASS)
        cols_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Standard blocks column
        std_frame = tk.Frame(cols_frame, bg=TacticalTheme.BG_DARK,
                            highlightbackground=TacticalTheme.CYAN_DIM,
                            highlightthickness=1)
        std_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(std_frame, text="STANDARD BLOCKS",
                font=TacticalTheme.FONT_NORMAL,
                fg=TacticalTheme.CYAN_PRIMARY,
                bg=TacticalTheme.BG_DARK).pack(pady=5)
        
        for block in ["> LightArmorBlock", "> LightArmorSlope", 
                     "> LightArmorCorner", "> LightArmorPanel"]:
            tk.Label(std_frame, text=block,
                    font=TacticalTheme.FONT_SMALL,
                    fg=TacticalTheme.TEXT_GRAY,
                    bg=TacticalTheme.BG_DARK).pack(pady=2)
        
        self.light_count_label = tk.Label(std_frame, text="0 BLOCKS",
                                         font=TacticalTheme.FONT_NORMAL,
                                         fg=TacticalTheme.ORANGE_PRIMARY,
                                         bg=TacticalTheme.BG_DARK)
        self.light_count_label.pack(pady=10)
        
        # Arrow column
        arrow_frame = tk.Frame(cols_frame, bg=TacticalTheme.BG_GLASS)
        arrow_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(arrow_frame, text=">>>",
                font=("Courier New", 24, "bold"),
                fg=TacticalTheme.ORANGE_PRIMARY,
                bg=TacticalTheme.BG_GLASS).pack(expand=True)
        
        # Heavy armor column
        heavy_frame = tk.Frame(cols_frame, bg=TacticalTheme.BG_DARK,
                              highlightbackground=TacticalTheme.ORANGE_PRIMARY,
                              highlightthickness=2)
        heavy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(heavy_frame, text="HEAVY ARMOR",
                font=TacticalTheme.FONT_NORMAL,
                fg=TacticalTheme.ORANGE_PRIMARY,
                bg=TacticalTheme.BG_DARK).pack(pady=5)
        
        for block in ["> HeavyArmorBlock", "> HeavyArmorSlope",
                     "> HeavyArmorCorner", "> HeavyArmorPanel"]:
            tk.Label(heavy_frame, text=block,
                    font=TacticalTheme.FONT_SMALL,
                    fg=TacticalTheme.ORANGE_DIM,
                    bg=TacticalTheme.BG_DARK).pack(pady=2)
        
        self.heavy_count_label = tk.Label(heavy_frame, text="0 BLOCKS",
                                         font=TacticalTheme.FONT_NORMAL,
                                         fg=TacticalTheme.ORANGE_PRIMARY,
                                         bg=TacticalTheme.BG_DARK)
        self.heavy_count_label.pack(pady=10)
    
    def create_conversion_button(self, parent):
        """Create the main conversion button."""
        self.convert_btn = tk.Button(parent,
                                    text="[ INITIATE HEAVY ARMOR CONVERSION ]",
                                    font=TacticalTheme.FONT_LARGE,
                                    fg=TacticalTheme.ORANGE_PRIMARY,
                                    bg=TacticalTheme.BG_DARK,
                                    activeforeground=TacticalTheme.BG_DARK,
                                    activebackground=TacticalTheme.ORANGE_PRIMARY,
                                    highlightbackground=TacticalTheme.ORANGE_PRIMARY,
                                    highlightthickness=3,
                                    relief=tk.FLAT,
                                    cursor="hand2",
                                    state=tk.DISABLED,
                                    command=self.convert_blueprint)
        self.convert_btn.pack(fill=tk.X, padx=10, pady=10, ipady=15)
    
    def create_footer(self):
        """Create the status bar footer."""
        footer = tk.Frame(self, bg=TacticalTheme.BG_MEDIUM,
                         highlightbackground=TacticalTheme.CYAN_PRIMARY,
                         highlightthickness=2)
        footer.pack(fill=tk.X, padx=10, pady=10)
        
        status_frame = tk.Frame(footer, bg=TacticalTheme.BG_MEDIUM)
        status_frame.pack(side=tk.LEFT, padx=10, pady=8)
        
        tk.Label(status_frame, text="STATUS:",
                font=TacticalTheme.FONT_SMALL,
                fg=TacticalTheme.TEXT_GRAY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_label = tk.Label(status_frame, text="SYSTEM READY",
                                    font=TacticalTheme.FONT_NORMAL,
                                    fg=TacticalTheme.CYAN_PRIMARY,
                                    bg=TacticalTheme.BG_MEDIUM)
        self.status_label.pack(side=tk.LEFT)
        
        # Stats
        stats_frame = tk.Frame(footer, bg=TacticalTheme.BG_MEDIUM)
        stats_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(stats_frame, text="SCANNED:",
                font=TacticalTheme.FONT_SMALL,
                fg=TacticalTheme.TEXT_GRAY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.LEFT, padx=(0, 5))
        
        self.scanned_label = tk.Label(stats_frame, text="0",
                                     font=TacticalTheme.FONT_NORMAL,
                                     fg=TacticalTheme.CYAN_PRIMARY,
                                     bg=TacticalTheme.BG_MEDIUM)
        self.scanned_label.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(stats_frame, text="CONVERTED:",
                font=TacticalTheme.FONT_SMALL,
                fg=TacticalTheme.TEXT_GRAY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.LEFT, padx=(0, 5))
        
        self.converted_label = tk.Label(stats_frame, text="0",
                                       font=TacticalTheme.FONT_NORMAL,
                                       fg=TacticalTheme.ORANGE_PRIMARY,
                                       bg=TacticalTheme.BG_MEDIUM)
        self.converted_label.pack(side=tk.LEFT)
        
        # Version info
        tk.Label(footer, text="SE-BCX-v1.0 // TACTICAL SYSTEMS ONLINE",
                font=TacticalTheme.FONT_SMALL,
                fg=TacticalTheme.TEXT_GRAY,
                bg=TacticalTheme.BG_MEDIUM).pack(side=tk.RIGHT, padx=10)
    
    def load_blueprints_async(self):
        """Load blueprints in a background thread."""
        self.status_label.config(text="SCANNING BLUEPRINTS...")
        
        def load_task():
            try:
                self.blueprints = self.scanner.scan_blueprints()
                self.after(0, self.on_blueprints_loaded)
            except Exception as e:
                self.after(0, lambda: self.show_error(f"Scan failed: {e}"))
        
        thread = threading.Thread(target=load_task, daemon=True)
        thread.start()
    
    def on_blueprints_loaded(self):
        """Handle blueprints loaded successfully."""
        if hasattr(self, 'bp_count_label'):
            self.bp_count_label.config(text=f"BLUEPRINTS: {len(self.blueprints)}")
        if hasattr(self, 'status_label'):
            self.status_label.config(text="BLUEPRINTS LOADED")
        if hasattr(self, 'scanned_label'):
            self.scanned_label.config(text=str(len(self.blueprints)))
        self.update_blueprint_list()
    
    def update_blueprint_list(self, filtered=None):
        """Update the blueprint listbox."""
        if not hasattr(self, 'bp_listbox'):
            return
        
        blueprints = filtered if filtered is not None else self.blueprints
        
        self.bp_listbox.delete(0, tk.END)
        
        if not blueprints:
            self.bp_listbox.insert(tk.END, "NO BLUEPRINTS FOUND")
            return
        
        for bp in blueprints:
            display = f"{bp.display_name[:30]:30} | {bp.grid_size:5} | {bp.light_armor_count:3} LA"
            self.bp_listbox.insert(tk.END, display)
    
    def filter_blueprints(self):
        """Filter blueprints based on search."""
        if not hasattr(self, 'bp_listbox'):
            return
        
        search = self.search_var.get()
        if not search or search == "SEARCH BLUEPRINTS...":
            self.update_blueprint_list()
            return
        
        filtered = [bp for bp in self.blueprints 
                   if search.lower() in bp.name.lower() or 
                      search.lower() in bp.display_name.lower()]
        self.update_blueprint_list(filtered)
    
    def on_blueprint_select(self, event):
        """Handle blueprint selection."""
        selection = self.bp_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        
        # Get filtered or full list
        search = self.search_var.get()
        if search and search != "SEARCH BLUEPRINTS...":
            filtered = [bp for bp in self.blueprints 
                       if search.lower() in bp.name.lower() or 
                          search.lower() in bp.display_name.lower()]
            blueprints = filtered
        else:
            blueprints = self.blueprints
        
        if idx >= len(blueprints):
            return
        
        self.selected_blueprint = blueprints[idx]
        self.update_details()
        self.status_label.config(text=f"SELECTED: {self.selected_blueprint.display_name}")
    
    def update_details(self):
        """Update details panel with selected blueprint."""
        if not self.selected_blueprint:
            return
        
        bp = self.selected_blueprint
        
        self.detail_labels['name'].config(text=bp.display_name[:30])
        self.detail_labels['grid'].config(text=bp.grid_size)
        self.detail_labels['blocks'].config(text=str(bp.block_count))
        self.detail_labels['light_armor'].config(text=str(bp.light_armor_count))
        self.detail_labels['heavy_armor'].config(text=str(bp.heavy_armor_count))
        
        self.light_count_label.config(text=f"{bp.light_armor_count} BLOCKS")
        self.heavy_count_label.config(text=f"{bp.heavy_armor_count} BLOCKS")
        
        # Enable/disable convert button
        if bp.light_armor_count > 0:
            self.convert_btn.config(state=tk.NORMAL)
        else:
            self.convert_btn.config(state=tk.DISABLED)
    
    def convert_blueprint(self):
        """Convert the selected blueprint."""
        if not self.selected_blueprint:
            return
        
        bp = self.selected_blueprint
        
        # Confirm
        response = messagebox.askyesno(
            "Confirm Conversion",
            f"Convert {bp.display_name} to heavy armor?\n\n"
            f"This will create: HEAVYARMOR_{bp.name}\n\n"
            f"Light armor blocks: {bp.light_armor_count}",
            icon='warning'
        )
        
        if not response:
            return
        
        # Disable button and update status
        self.convert_btn.config(state=tk.DISABLED)
        self.status_label.config(text="CONVERTING...")
        
        def convert_task():
            try:
                dest, scanned, converted = self.converter.create_heavy_armor_blueprint(bp.path)
                self.after(0, lambda: self.on_conversion_complete(scanned, converted))
            except Exception as e:
                self.after(0, lambda: self.show_error(f"Conversion failed: {e}"))
        
        thread = threading.Thread(target=convert_task, daemon=True)
        thread.start()
    
    def on_conversion_complete(self, scanned, converted):
        """Handle conversion completion."""
        self.scanned_label.config(text=str(scanned))
        self.converted_label.config(text=str(converted))
        self.status_label.config(text="CONVERSION COMPLETE")
        self.convert_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo(
            "Conversion Complete",
            f"Successfully converted {converted} blocks!\n\n"
            f"Blocks scanned: {scanned}\n"
            f"New blueprint created with HEAVYARMOR_ prefix"
        )
        
        # Reload blueprints
        self.load_blueprints_async()
    
    def show_error(self, message):
        """Show error message."""
        self.status_label.config(text="ERROR")
        self.convert_btn.config(state=tk.NORMAL)
        messagebox.showerror("Error", message)


def main():
    """Main entry point."""
    try:
        app = TacticalCommandCenter()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
