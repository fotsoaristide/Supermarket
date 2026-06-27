import customtkinter as ctk
from datetime import datetime
from gui.theme import Theme


class TopBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            height=Theme.TOPBAR_HEIGHT,
            corner_radius=0,
            fg_color=Theme.TOPBAR
        )

        self.pack_propagate(False)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Supermarket POS",
            font=Theme.SUBTITLE,
            text_color=Theme.TEXT
        )
        title.pack(side="left", padx=20)

        date = ctk.CTkLabel(
            self,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        date.pack(side="right", padx=20)
