import customtkinter as ctk

from gui.theme import Theme


class PrimaryButton(ctk.CTkButton):

    def __init__(self, master, text, command):

        super().__init__(
            master,
            text=text,
            command=command,
            height=Theme.BUTTON_HEIGHT,
            corner_radius=Theme.RADIUS,
            font=Theme.BUTTON,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER
        )
