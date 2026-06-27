import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme


class ExportView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Export")

        self.ui = ui

        self.build_ui()

    def build_ui(self):

        # =========================
        # EXPORT TYPE
        # =========================

        self.export_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.export_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.export_frame,
            text="Export Data",
            font=Theme.SUBTITLE
        )
        title.pack(anchor="w", pady=(0, 10))

        self.export_type = ctk.CTkOptionMenu(
            self.export_frame,
            values=[
                "Sales Report (CSV)",
                "Products List (CSV)",
                "Accounting Report"
            ]
        )
        self.export_type.pack(fill="x", pady=5)

        # =========================
        # PERIOD (MOCK UI)
        # =========================

        self.period_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.period_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        period_label = ctk.CTkLabel(
            self.period_frame,
            text="Period (mock)",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        period_label.pack(anchor="w", pady=(0, 5))

        self.start_date = ctk.CTkEntry(
            self.period_frame,
            placeholder_text="Start date (dd/mm/yyyy)"
        )
        self.start_date.pack(fill="x", pady=5)

        self.end_date = ctk.CTkEntry(
            self.period_frame,
            placeholder_text="End date (dd/mm/yyyy)"
        )
        self.end_date.pack(fill="x", pady=5)

        # =========================
        # ACTION
        # =========================

        self.action_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=20)

        self.export_btn = ctk.CTkButton(
            self.action_frame,
            text="EXPORT",
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER
        )
        self.export_btn.pack(fill="x")

        self.status_label = ctk.CTkLabel(
            self.action_frame,
            text="Ready to export",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        self.status_label.pack(pady=10)
