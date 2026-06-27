import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme


class BackupView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Backup")

        self.ui = ui

        self.build_ui()

    def build_ui(self):

        # =========================
        # INFO SYSTEME
        # =========================

        self.info_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.info_frame,
            text="System Backup Manager",
            font=Theme.SUBTITLE
        )
        title.pack(anchor="w", pady=(0, 10))

        info = ctk.CTkLabel(
            self.info_frame,
            text="Manage your POS data backup and restore operations.",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        info.pack(anchor="w")

        # =========================
        # ACTIONS
        # =========================

        self.action_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=20)

        self.backup_btn = ctk.CTkButton(
            self.action_frame,
            text="CREATE BACKUP",
            fg_color=Theme.SUCCESS,
            hover_color="#16a34a"
        )
        self.backup_btn.pack(fill="x", pady=5)

        self.restore_btn = ctk.CTkButton(
            self.action_frame,
            text="RESTORE BACKUP",
            fg_color=Theme.WARNING,
            hover_color="#d97706"
        )
        self.restore_btn.pack(fill="x", pady=5)

        # =========================
        # STATUS
        # =========================

        self.status_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="System ready",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        self.status_label.pack(pady=10)
