import customtkinter as ctk
import os
from datetime import datetime

from gui.views.base_view import BaseView
from gui.cards.stat_card import StatCard
from gui.theme import Theme


class BackupView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Backup")

        self.ui = ui
        self.confirm_window = None

        self.build_ui()
        self.load_backups()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(1, weight=1)

        # ==========================================
        # TOP CARDS
        # ==========================================

        self.cards = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.cards.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.cards.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.total_card = StatCard(
            self.cards,
            "Total Backups",
            "0",
            Theme.PRIMARY
        )
        self.total_card.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.latest_card = StatCard(
            self.cards,
            "Latest Backup",
            "-",
            Theme.SUCCESS
        )
        self.latest_card.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.size_card = StatCard(
            self.cards,
            "Backup Storage",
            "0 MB",
            Theme.WARNING
        )
        self.size_card.grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # ==========================================
        # BACKUP LIST
        # ==========================================

        self.list_frame = ctk.CTkFrame(
            self.body,
            corner_radius=12
        )
        self.list_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.list_frame,
            text="AVAILABLE BACKUPS",
            font=("Arial", 18, "bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        self.backup_list = ctk.CTkScrollableFrame(
            self.list_frame
        )
        self.backup_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # ACTIONS
        # ==========================================

        self.actions = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.actions.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.create_btn = ctk.CTkButton(
            self.actions,
            text="CREATE BACKUP",
            height=45,
            fg_color=Theme.SUCCESS,
            command=self.confirm_backup
        )
        self.create_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.open_btn = ctk.CTkButton(
            self.actions,
            text="OPEN BACKUP FOLDER",
            height=45,
            command=self.open_folder
        )
        self.open_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.status = ctk.CTkLabel(
            self.body,
            text="System ready",
            font=("Arial", 14)
        )
        self.status.grid(
            row=3,
            column=0,
            pady=10
        )

    # =====================================================
    # LOAD
    # =====================================================

    def load_backups(self):

        for w in self.backup_list.winfo_children():
            w.destroy()

        backups = self.ui.backup_service.list_backups()

        total_size = 0

        for backup in backups:

            size = os.path.getsize(backup)
            total_size += size

            row = ctk.CTkFrame(
                self.backup_list
            )
            row.pack(
                fill="x",
                pady=5
            )

            name = os.path.basename(backup)

            ctk.CTkLabel(
                row,
                text=name,
                font=("Arial", 15, "bold")
            ).pack(
                side="left",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=f"{size//1024} KB"
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkButton(
                row,
                text="RESTORE",
                width=100,
                fg_color="#dc2626",
                command=lambda b=backup:
                self.confirm_restore(b)
            ).pack(
                side="right",
                padx=5
            )

        self.total_card.update_value(
            str(len(backups))
        )

        self.size_card.update_value(
            f"{total_size//1024//1024} MB"
        )

        if backups:
            self.latest_card.update_value(
                os.path.basename(backups[0])[-22:-3]
            )

    # =====================================================
    # CREATE BACKUP
    # =====================================================

    def create_backup(self):

        try:

            path = self.ui.backup_service.create_backup()

            self.status.configure(
                text=f"Backup created: {os.path.basename(path)}"
            )

            self.load_backups()

        except Exception as e:

            self.status.configure(
                text=str(e)
            )

    # =====================================================
    # RESTORE
    # =====================================================

    def restore_backup(self, backup):

        try:

            self.ui.backup_service.restore_backup(
                backup
            )

            self.status.configure(
                text="Backup restored successfully"
            )

        except Exception as e:

            self.status.configure(
                text=str(e)
            )

    # =====================================================
    # OPEN
    # =====================================================

    def open_folder(self):

        os.makedirs(
            "backups",
            exist_ok=True
        )

        os.startfile("backups")

    # =====================================================
    # CONFIRM BACKUP
    # =====================================================

    def confirm_backup(self):

        self.confirm(
            "Create a new backup?",
            self.create_backup
        )

    # =====================================================
    # CONFIRM RESTORE
    # =====================================================

    def confirm_restore(
        self,
        backup
    ):

        self.confirm(
            "Restore selected backup?\nCurrent data will be replaced.",
            lambda:
            self.restore_backup(backup)
        )

    # =====================================================
    # GENERIC CONFIRM
    # =====================================================

    def confirm(
        self,
        message,
        callback
    ):

        if (
            self.confirm_window
            and
            self.confirm_window.winfo_exists()
        ):
            self.confirm_window.focus()
            return

        self.confirm_window = ctk.CTkToplevel(self)

        self.confirm_window.title(
            "Confirmation"
        )

        self.confirm_window.geometry(
            "350x170"
        )

        self.confirm_window.grab_set()

        ctk.CTkLabel(
            self.confirm_window,
            text=message,
            font=("Arial", 15)
        ).pack(
            pady=30
        )

        buttons = ctk.CTkFrame(
            self.confirm_window,
            fg_color="transparent"
        )
        buttons.pack()

        ctk.CTkButton(
            buttons,
            text="YES",
            width=100,
            command=lambda: [
                callback(),
                self.confirm_window.destroy()
            ]
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text="NO",
            width=100,
            fg_color="#dc2626",
            command=self.confirm_window.destroy
        ).pack(
            side="left",
            padx=10
        )
