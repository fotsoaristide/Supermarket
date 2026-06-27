import customtkinter as ctk

from gui.theme import Theme


class SectionTitle(ctk.CTkLabel):

    def __init__(self, master, text):

        super().__init__(
            master,
            text=text,
            font=Theme.SUBTITLE,
            text_color=Theme.TEXT
        )
