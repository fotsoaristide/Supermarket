import customtkinter as ctk
from gui.theme import Theme


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, on_change_page):
        super().__init__(
            master,
            width=Theme.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=Theme.SIDEBAR
        )

        self.on_change_page = on_change_page
        self.pack_propagate(False)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="POS SYSTEM",
            font=Theme.TITLE,
            text_color=Theme.TEXT_INVERT
        )
        title.pack(pady=20)

        buttons = [
            ("Dashboard", "Dashboard"),
            ("Products", "Products"),
            ("Sales", "Sales"),
            ("History", "History"),
            ("Accounting", "Accounting"),
            ("Export", "Export"),
            ("Backup", "Backup"),
            ("Settings", "Settings"),
        ]

        for label, page in buttons:
            btn = ctk.CTkButton(
                self,
                text=label,
                fg_color="transparent",
                text_color=Theme.TEXT_INVERT,
                hover_color="#1f2937",
                anchor="w",
                command=lambda p=page: self.on_change_page(p)
            )
            btn.pack(fill="x", padx=12, pady=4)
