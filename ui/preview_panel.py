"""
Preview Panel Component
Center tabview with Intel, XML Source, Preview Diff, and Analytics tabs.
"""

from __future__ import annotations

import tkinter as tk
from typing import Dict, Iterable, List, Optional

import customtkinter as ctk

from blueprint_analytics import (
    ConversionComparison,
    HealthIssue,
    SEVERITY_ERROR,
    SEVERITY_INFO,
    SEVERITY_WARNING,
)
from ui.theme import TacticalTheme


class PreviewPanel(ctk.CTkFrame):
    """Center panel with tabbed views for blueprint information."""

    def __init__(
        self,
        master,
        on_run_preview=None,
        on_export_csv=None,
        on_export_txt=None,
        on_apply_fix=None,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=TacticalTheme.BG_DARK,
            border_width=1,
            border_color=TacticalTheme.CYAN_PRIMARY,
            corner_radius=8,
            **kwargs,
        )
        self._on_run_preview = on_run_preview
        self._on_export_csv = on_export_csv
        self._on_export_txt = on_export_txt
        self._on_apply_fix = on_apply_fix
        self._latest_health_issues: List[HealthIssue] = []

        self.tabview = ctk.CTkTabview(
            self,
            fg_color=TacticalTheme.BG_DARK,
            segmented_button_fg_color=TacticalTheme.BG_MEDIUM,
            segmented_button_selected_color=TacticalTheme.ORANGE_PRIMARY,
            segmented_button_selected_hover_color=TacticalTheme.ORANGE_DIM,
            segmented_button_unselected_color=TacticalTheme.BG_MEDIUM,
            segmented_button_unselected_hover_color=TacticalTheme.BG_GLASS,
            text_color=TacticalTheme.TEXT_GRAY,
            text_color_disabled=TacticalTheme.TEXT_GRAY,
            corner_radius=6,
        )
        self.tabview.pack(fill="both", expand=True, padx=4, pady=4)

        self._build_intel_tab()
        self._build_xml_tab()
        self._build_preview_tab()
        self._build_analytics_tab()

    def _build_intel_tab(self):
        self.tab_intel = self.tabview.add("INTEL")
        self.tab_intel.configure(fg_color=TacticalTheme.BG_DARK)
        ctk.CTkLabel(
            self.tab_intel,
            text=">> BLUEPRINT INTEL",
            font=TacticalTheme.FONT_LARGE,
            text_color=TacticalTheme.ORANGE_PRIMARY,
        ).pack(pady=(8, 4))
        self.intel_text = ctk.CTkLabel(
            self.tab_intel,
            text="Select a blueprint to review block totals, conversion readiness, and file location.",
            font=TacticalTheme.FONT_NORMAL,
            text_color=TacticalTheme.TEXT_CYAN,
            wraplength=600,
            anchor="nw",
            justify="left",
        )
        self.intel_text.pack(fill="both", expand=True, padx=20, pady=10)

    def _build_xml_tab(self):
        self.tab_xml = self.tabview.add("XML SOURCE")
        self.tab_xml.configure(fg_color=TacticalTheme.BG_DARK)

        xml_header = ctk.CTkFrame(self.tab_xml, fg_color="transparent")
        xml_header.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(
            xml_header,
            text=">> XML SOURCE VIEWER",
            font=TacticalTheme.FONT_LARGE,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).pack(side="left")
        self.xml_status = ctk.CTkLabel(
            xml_header,
            text="(No file loaded)",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.TEXT_GRAY,
        )
        self.xml_status.pack(side="right")
        self.xml_textbox = ctk.CTkTextbox(
            self.tab_xml,
            font=("Consolas", 9),
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color="#0c1220",
            border_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            corner_radius=4,
            state="disabled",
        )
        self.xml_textbox.pack(fill="both", expand=True, padx=8, pady=8)

    def _build_preview_tab(self):
        self.tab_preview = self.tabview.add("PREVIEW")
        self.tab_preview.configure(fg_color=TacticalTheme.BG_DARK)

        preview_header = ctk.CTkFrame(self.tab_preview, fg_color="transparent")
        preview_header.pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(
            preview_header,
            text=">> BEFORE / AFTER DIFF",
            font=TacticalTheme.FONT_LARGE,
            text_color=TacticalTheme.GREEN_PRIMARY,
        ).pack(side="left")
        ctk.CTkButton(
            preview_header,
            text="RUN PREVIEW",
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.GREEN_PRIMARY,
            text_color=TacticalTheme.GREEN_PRIMARY,
            hover_color=TacticalTheme.BG_MEDIUM,
            width=120,
            height=28,
            command=self._run_preview,
        ).pack(side="right")

        preview_split = ctk.CTkFrame(self.tab_preview, fg_color="transparent")
        preview_split.pack(fill="both", expand=True, padx=8, pady=8)
        preview_split.columnconfigure(0, weight=1)
        preview_split.columnconfigure(1, weight=1)
        preview_split.rowconfigure(1, weight=1)

        ctk.CTkLabel(
            preview_split,
            text="CURRENT (MATCHING SOURCE BLOCKS)",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.ORANGE_PRIMARY,
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        ctk.CTkLabel(
            preview_split,
            text="AFTER CONVERSION (TARGET BLOCKS)",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.preview_before_text = ctk.CTkTextbox(
            preview_split,
            font=("Consolas", 9),
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color="#0c1220",
            border_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            corner_radius=4,
            state="disabled",
        )
        self.preview_before_text.grid(row=1, column=0, sticky="nsew", padx=(0, 4))
        self.preview_after_text = ctk.CTkTextbox(
            preview_split,
            font=("Consolas", 9),
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color="#0c1220",
            border_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            corner_radius=4,
            state="disabled",
        )
        self.preview_after_text.grid(row=1, column=1, sticky="nsew", padx=(4, 0))

        self.preview_summary_text = ctk.CTkTextbox(
            self.tab_preview,
            height=120,
            font=("Consolas", 9),
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color="#0c1220",
            border_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            corner_radius=4,
            state="disabled",
        )
        self.preview_summary_text.pack(fill="x", padx=8, pady=(0, 8))

    def _build_analytics_tab(self):
        self.tab_analytics = self.tabview.add("ANALYTICS")
        self.tab_analytics.configure(fg_color=TacticalTheme.BG_DARK)

        header = ctk.CTkFrame(self.tab_analytics, fg_color="transparent")
        header.pack(fill="x", padx=8, pady=(6, 4))
        ctk.CTkLabel(
            header,
            text=">> BLUEPRINT ANALYTICS",
            font=TacticalTheme.FONT_LARGE,
            text_color=TacticalTheme.ORANGE_PRIMARY,
        ).pack(side="left")

        button_row = ctk.CTkFrame(header, fg_color="transparent")
        button_row.pack(side="right")
        ctk.CTkButton(
            button_row,
            text="EXPORT CSV",
            width=100,
            height=28,
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.CYAN_PRIMARY,
            text_color=TacticalTheme.CYAN_PRIMARY,
            hover_color=TacticalTheme.BG_MEDIUM,
            command=self._export_csv,
        ).pack(side="left", padx=3)
        ctk.CTkButton(
            button_row,
            text="EXPORT TXT",
            width=100,
            height=28,
            font=TacticalTheme.FONT_SMALL,
            fg_color="transparent",
            border_width=1,
            border_color=TacticalTheme.GREEN_PRIMARY,
            text_color=TacticalTheme.GREEN_PRIMARY,
            hover_color=TacticalTheme.BG_MEDIUM,
            command=self._export_txt,
        ).pack(side="left", padx=3)

        metrics = ctk.CTkFrame(
            self.tab_analytics,
            fg_color=TacticalTheme.BG_GLASS,
            border_width=1,
            border_color=TacticalTheme.CYAN_DIM,
            corner_radius=6,
        )
        metrics.pack(fill="x", padx=8, pady=(0, 6))
        metrics.columnconfigure((0, 1, 2, 3), weight=1)
        self.metric_labels = {}
        metric_defs = [
            ("Blocks", "0"),
            ("PCU", "0"),
            ("Mass", "0"),
            ("Convertible", "0"),
        ]
        for idx, (name, value) in enumerate(metric_defs):
            cell = ctk.CTkFrame(metrics, fg_color="transparent")
            cell.grid(row=0, column=idx, sticky="ew", padx=8, pady=8)
            ctk.CTkLabel(
                cell,
                text=name.upper(),
                font=TacticalTheme.FONT_SMALL,
                text_color=TacticalTheme.TEXT_GRAY,
            ).pack(anchor="w")
            label = ctk.CTkLabel(
                cell,
                text=value,
                font=TacticalTheme.FONT_LARGE,
                text_color=TacticalTheme.TEXT_CYAN,
            )
            label.pack(anchor="w")
            self.metric_labels[name] = label

        body = ctk.CTkFrame(self.tab_analytics, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        body.columnconfigure(0, weight=1, uniform="analytics")
        body.columnconfigure(1, weight=1, uniform="analytics")
        body.rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="CATEGORY DISTRIBUTION",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        ctk.CTkLabel(
            body,
            text="ORES -> INGOTS -> COMPONENTS -> BLOCKS",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.CYAN_PRIMARY,
        ).grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.chart_canvas = tk.Canvas(
            body,
            bg="#0c1220",
            highlightthickness=1,
            highlightbackground=TacticalTheme.BG_MEDIUM,
        )
        self.chart_canvas.grid(row=1, column=0, sticky="nsew", padx=(0, 4), pady=(0, 4))

        self.resource_tree = ctk.CTkTextbox(
            body,
            font=("Consolas", 9),
            text_color=TacticalTheme.TEXT_CYAN,
            fg_color="#0c1220",
            border_color=TacticalTheme.BG_MEDIUM,
            border_width=1,
            corner_radius=4,
            state="disabled",
        )
        self.resource_tree.grid(row=1, column=1, sticky="nsew", padx=(4, 0), pady=(0, 4))

        self.issues_frame = ctk.CTkFrame(
            self.tab_analytics,
            fg_color=TacticalTheme.BG_GLASS,
            border_width=1,
            border_color=TacticalTheme.CYAN_DIM,
            corner_radius=6,
        )
        self.issues_frame.pack(fill="x", padx=8, pady=(0, 8))
        ctk.CTkLabel(
            self.issues_frame,
            text="HEALTH AUDIT",
            font=TacticalTheme.FONT_SMALL,
            text_color=TacticalTheme.ORANGE_PRIMARY,
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.issues_container = ctk.CTkFrame(self.issues_frame, fg_color="transparent")
        self.issues_container.pack(fill="x", padx=8, pady=(0, 8))

    def _run_preview(self):
        if self._on_run_preview:
            self._on_run_preview()

    def _export_csv(self):
        if self._on_export_csv:
            self._on_export_csv()

    def _export_txt(self):
        if self._on_export_txt:
            self._on_export_txt()

    def update_intel(self, bp_info, conversion_mode: str):
        convertible = (
            bp_info.light_armor_count
            if conversion_mode == "light_to_heavy"
            else bp_info.heavy_armor_count
        )
        source = "LIGHT" if conversion_mode == "light_to_heavy" else "HEAVY"
        target = "HEAVY" if conversion_mode == "light_to_heavy" else "LIGHT"
        lines = [
            f"BLUEPRINT: {bp_info.display_name}",
            f"GRID SIZE: {bp_info.grid_size}",
            f"TOTAL BLOCKS: {bp_info.block_count:,}",
            f"LIGHT ARMOR: {bp_info.light_armor_count:,}",
            f"HEAVY ARMOR: {bp_info.heavy_armor_count:,}",
            "",
            f"Current mode: {source} -> {target}",
            f"Convertible armor blocks available: {convertible:,}",
            "",
            f"Blueprint path: {bp_info.path}",
        ]
        if bp_info.category_counts:
            lines.extend(["", "Category matches:"])
            for name, count in sorted(bp_info.category_counts.items()):
                lines.append(f"  {name}: {count}")
        self.intel_text.configure(text="\n".join(lines))

    def clear_intel(self):
        self.intel_text.configure(
            text="Select a blueprint to review block totals, conversion readiness, and file location."
        )
        self.clear_analytics()
        self.show_preview_diff({}, {}, "Select a blueprint and run preview.")

    def load_xml(self, file_path, status_text: str):
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                content = handle.read()
            self.xml_textbox.configure(state="normal")
            self.xml_textbox.delete("1.0", "end")
            self.xml_textbox.insert("end", content)
            self.xml_textbox.configure(state="disabled")
            self.xml_status.configure(text=status_text)
        except Exception as exc:
            self.xml_textbox.configure(state="normal")
            self.xml_textbox.delete("1.0", "end")
            self.xml_textbox.insert("end", f"Error reading file: {exc}")
            self.xml_textbox.configure(state="disabled")

    def show_preview_report(self, bp_name: str, mode: str, report: str):
        """
        Backward-compatible API with richer rendering.
        """
        self.show_preview_diff({}, {}, f"DRY-RUN PREVIEW: {bp_name}\nMode: {mode}\n\n{report}")
        self.tabview.set("PREVIEW")

    def show_preview_diff(
        self,
        before_counts: Dict[str, int],
        after_counts: Dict[str, int],
        summary_text: str,
    ):
        self._set_textbox_content(
            self.preview_before_text,
            self._format_counts(before_counts, "No matching source blocks found."),
        )
        self._set_textbox_content(
            self.preview_after_text,
            self._format_counts(after_counts, "No resulting target blocks."),
        )
        self._set_textbox_content(self.preview_summary_text, summary_text or "No changes.")
        self.tabview.set("PREVIEW")

    def update_analytics(self, analytics_result, comparison: Optional[ConversionComparison] = None):
        self.metric_labels["Blocks"].configure(text=f"{analytics_result.block_count:,}")
        self.metric_labels["PCU"].configure(text=f"{analytics_result.pcu_total:,}")
        self.metric_labels["Mass"].configure(text=f"{analytics_result.mass_total:,.2f}")

        convertible = 0
        if comparison:
            convertible = sum(comparison.block_changes.values())
        self.metric_labels["Convertible"].configure(text=f"{convertible:,}")

        self._draw_category_chart(analytics_result.category_counts)
        self._set_textbox_content(
            self.resource_tree,
            self._build_resource_tree_text(analytics_result, comparison),
        )
        self._populate_health_issues(analytics_result.health_issues)

    def clear_analytics(self):
        for label in self.metric_labels.values():
            label.configure(text="0")
        self.chart_canvas.delete("all")
        self._set_textbox_content(self.resource_tree, "Select a blueprint to analyze.")
        self._populate_health_issues([])

    def _populate_health_issues(self, issues: Iterable[HealthIssue]):
        self._latest_health_issues = list(issues)
        for child in self.issues_container.winfo_children():
            child.destroy()

        if not self._latest_health_issues:
            ctk.CTkLabel(
                self.issues_container,
                text="No health issues detected.",
                font=TacticalTheme.FONT_SMALL,
                text_color=TacticalTheme.GREEN_PRIMARY,
            ).pack(anchor="w", pady=2)
            return

        for issue in self._latest_health_issues:
            color = {
                SEVERITY_INFO: TacticalTheme.CYAN_PRIMARY,
                SEVERITY_WARNING: TacticalTheme.ORANGE_PRIMARY,
                SEVERITY_ERROR: TacticalTheme.RED_PRIMARY,
            }.get(issue.severity, TacticalTheme.CYAN_PRIMARY)
            row = ctk.CTkFrame(self.issues_container, fg_color=TacticalTheme.BG_DARK, corner_radius=4)
            row.pack(fill="x", pady=2)
            text = f"[{issue.severity}] {issue.message}\nSuggestion: {issue.suggestion}"
            ctk.CTkLabel(
                row,
                text=text,
                justify="left",
                anchor="w",
                wraplength=700,
                text_color=color,
                font=TacticalTheme.FONT_SMALL,
            ).pack(side="left", fill="x", expand=True, padx=8, pady=6)
            if issue.fix_id:
                ctk.CTkButton(
                    row,
                    text="APPLY FIX",
                    width=90,
                    height=26,
                    font=TacticalTheme.FONT_SMALL,
                    fg_color="transparent",
                    border_width=1,
                    border_color=TacticalTheme.GREEN_PRIMARY,
                    text_color=TacticalTheme.GREEN_PRIMARY,
                    hover_color=TacticalTheme.BG_MEDIUM,
                    command=lambda fix=issue.fix_id: self._emit_fix(fix),
                ).pack(side="right", padx=6, pady=6)

    def _emit_fix(self, fix_id: str):
        if self._on_apply_fix:
            self._on_apply_fix(fix_id)

    def _draw_category_chart(self, category_counts: Dict[str, int]):
        self.chart_canvas.delete("all")
        if not category_counts:
            self.chart_canvas.create_text(
                10,
                20,
                text="No category data available.",
                fill=TacticalTheme.TEXT_GRAY,
                anchor="w",
            )
            return

        width = max(self.chart_canvas.winfo_width(), 320)
        height = max(self.chart_canvas.winfo_height(), 220)
        self.chart_canvas.config(scrollregion=(0, 0, width, height))
        max_value = max(category_counts.values()) if category_counts else 1

        bar_h = max(18, min(30, int((height - 20) / max(len(category_counts), 1))))
        y = 12
        palette = [
            TacticalTheme.CYAN_PRIMARY,
            TacticalTheme.ORANGE_PRIMARY,
            TacticalTheme.GREEN_PRIMARY,
            "#38bdf8",
            "#f97316",
            "#14b8a6",
        ]
        for idx, (name, value) in enumerate(sorted(category_counts.items(), key=lambda item: item[1], reverse=True)):
            ratio = value / max_value if max_value else 0
            bar_w = int((width - 180) * ratio)
            color = palette[idx % len(palette)]
            self.chart_canvas.create_rectangle(150, y, 150 + bar_w, y + bar_h, fill=color, outline="")
            self.chart_canvas.create_text(10, y + (bar_h / 2), text=name, fill=TacticalTheme.TEXT_CYAN, anchor="w")
            self.chart_canvas.create_text(
                160 + bar_w,
                y + (bar_h / 2),
                text=str(value),
                fill=TacticalTheme.TEXT_WHITE,
                anchor="w",
            )
            y += bar_h + 8

    @staticmethod
    def _set_textbox_content(textbox: ctk.CTkTextbox, text: str):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", text)
        textbox.configure(state="disabled")

    @staticmethod
    def _format_counts(counts: Dict[str, int], empty_text: str) -> str:
        if not counts:
            return empty_text
        lines = []
        for subtype, qty in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            lines.append(f"{subtype:45} x{qty}")
        return "\n".join(lines)

    @staticmethod
    def _build_resource_tree_text(analytics_result, comparison: Optional[ConversionComparison]) -> str:
        lines: List[str] = []
        lines.append("ORES")
        for ore, qty in analytics_result.ore_totals.items():
            lines.append(f"  - {ore}: {qty:,.2f}")
        lines.append("")
        lines.append("INGOTS")
        for ingot, qty in analytics_result.ingot_totals.items():
            lines.append(f"  - {ingot}: {qty:,.2f}")
        lines.append("")
        lines.append("COMPONENTS")
        for component, qty in analytics_result.component_totals.items():
            lines.append(f"  - {component}: {qty:,}")
        lines.append("")
        lines.append("TOP BLOCKS")
        for subtype, qty in list(analytics_result.block_counts.items())[:15]:
            lines.append(f"  - {subtype}: {qty:,}")

        if comparison:
            lines.append("")
            lines.append("CONVERSION DELTAS")
            lines.append(f"  - PCU: {comparison.pcu_delta:+d}")
            lines.append(f"  - Mass: {comparison.mass_delta:+.2f}")
            for component, delta in sorted(comparison.component_delta.items()):
                if delta:
                    lines.append(f"  - {component}: {delta:+d}")
        return "\n".join(lines)

    def switch_to_xml(self):
        self.tabview.set("XML SOURCE")

