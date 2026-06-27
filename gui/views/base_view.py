import customtkinter as ctk


class BaseView(ctk.CTkFrame):

    def __init__(self, master, title):
        super().__init__(master)

        self.title = title

        # FULL EXPANSION SAFE FIX
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # HEADER (FIXED)
        self.header = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 26, "bold")
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # BODY (EXPAND ONLY AREA)
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)
