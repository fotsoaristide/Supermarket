import customtkinter as ctk
from gui.theme import Theme


class StatCard(ctk.CTkFrame):

    def __init__(self, master, title, value, color):
        super().__init__(master)

        self.configure(
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS,
            height=120
        )

        self.grid_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=Theme.CARD_TITLE,
            text_color=Theme.TEXT_LIGHT
        )
        self.title_label.pack(pady=(15, 5))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=Theme.CARD_VALUE,
            text_color=color
        )
        self.value_label.pack(pady=(0, 10))

        self.current_value = value

    # =========================
    # MÉTHODE MANQUANTE (FIX)
    # =========================
    def update_value(self, new_value: str):
        """
        Update displayed value safely.
        """
        self.current_value = new_value
        self.value_label.configure(text=new_value)
