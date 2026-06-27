import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme


class SettingsView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Settings")

        self.ui = ui

        self.build_ui()

    def build_ui(self):

        # =========================
        # GENERAL SETTINGS
        # =========================

        self.general_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.general_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.general_frame,
            text="General Settings",
            font=Theme.SUBTITLE
        )
        title.pack(anchor="w", pady=(0, 10))

        self.store_name = ctk.CTkEntry(
            self.general_frame,
            placeholder_text="Store name"
        )
        self.store_name.pack(fill="x", pady=5)

        self.currency = ctk.CTkOptionMenu(
            self.general_frame,
            values=["FCFA", "EUR", "USD"]
        )
        self.currency.pack(fill="x", pady=5)

        # =========================
        # UI SETTINGS (MOCK)
        # =========================

        self.ui_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.ui_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        ui_title = ctk.CTkLabel(
            self.ui_frame,
            text="Interface Settings",
            font=Theme.SUBTITLE
        )
        ui_title.pack(anchor="w", pady=(0, 10))

        self.theme_mode = ctk.CTkOptionMenu(
            self.ui_frame,
            values=["Light", "Dark (future)"]
        )
        self.theme_mode.pack(fill="x", pady=5)

        # =========================
        # SAVE ACTION
        # =========================

        self.action_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=20)

        self.save_btn = ctk.CTkButton(
            self.action_frame,
            text="SAVE SETTINGS",
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER
        )
        self.save_btn.pack(fill="x")

        self.status_label = ctk.CTkLabel(
            self.action_frame,
            text="Settings loaded",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        self.status_label.pack(pady=10)
