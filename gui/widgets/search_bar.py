import customtkinter as ctk
from gui.theme import Theme


class SearchBar(ctk.CTkFrame):

    def __init__(self, master, placeholder="Search...", command=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.command = command

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=Theme.ENTRY_HEIGHT,
            corner_radius=Theme.RADIUS
        )
        self.entry.pack(side="left", fill="x", expand=True)

        self.button = ctk.CTkButton(
            self,
            text="Search",
            width=120,
            height=Theme.ENTRY_HEIGHT,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER,
            command=self.on_search
        )
        self.button.pack(side="left", padx=Theme.SM)

    def on_search(self):

        if self.command:
            self.command(self.entry.get())
