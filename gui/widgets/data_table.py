import customtkinter as ctk


class DataTable(ctk.CTkFrame):

    def __init__(self, master, columns, data=None):
        super().__init__(master)

        self.columns = columns
        self.data = data or []

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.grid(row=1, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_table()

    # =========================
    # BUILD TABLE
    # =========================
    def build_table(self):

        self.render_header()
        self.render_rows(self.data)

    # =========================
    # HEADER
    # =========================
    def render_header(self):

        for widget in self.header_frame.winfo_children():
            widget.destroy()

        for i, col in enumerate(self.columns):

            lbl = ctk.CTkLabel(
                self.header_frame,
                text=col,
                font=("Arial", 12, "bold"),
                anchor="w"
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=5, pady=5)

            self.header_frame.grid_columnconfigure(i, weight=1)

    # =========================
    # ROWS
    # =========================
    def render_rows(self, data):

        for widget in self.body_frame.winfo_children():
            widget.destroy()

        for row_index, row in enumerate(data):

            row_frame = ctk.CTkFrame(self.body_frame)
            row_frame.grid(row=row_index, column=0, sticky="ew", pady=2)

            for col_index, cell in enumerate(row):

                lbl = ctk.CTkLabel(
                    row_frame,
                    text=str(cell),
                    anchor="w"
                )
                lbl.grid(row=0, column=col_index, sticky="ew", padx=5)

                row_frame.grid_columnconfigure(col_index, weight=1)

    # =========================
    # UPDATE DATA (SAFE)
    # =========================
    def update_data(self, new_data):
        self.data = new_data
        self.render_rows(self.data)
