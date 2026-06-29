import customtkinter as ctk
from gui.theme import Theme


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, on_change_page, role):
        super().__init__(
            master,
            width=Theme.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=Theme.SIDEBAR
        )

        self.on_change_page = on_change_page
        self.role = role
        self.pack_propagate(False)

        self.build_ui()

    def build_ui(self):

        self.buttons = {}

        title = ctk.CTkLabel(
            self,
            text="ASTRO SYSTEM",
            font=Theme.TITLE,
            text_color=Theme.TEXT_INVERT
        )
        title.pack(pady=20)

        if self.role == "ADMIN":

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

        else:

            buttons = [
                ("Dashboard", "Dashboard"),
                ("Sales", "Sales"),
                ("History", "History"),
            ]

        for label, page in buttons:

            btn = ctk.CTkButton(
                self,
                text=label,
                fg_color="transparent",
                text_color=Theme.TEXT_INVERT,
                hover_color="#1f2937",
                anchor="w",
                command=lambda p=page: self.change_page(p)
            )

            btn.pack(
                fill="x",
                padx=12,
                pady=4
            )

            self.buttons[page] = btn

        # pousse le bouton EXIT en bas
        spacer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        spacer.pack(
            expand=True,
            fill="both"
        )

        self.exit_btn = ctk.CTkButton(
            self,
            text="EXIT",
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.confirm_exit
        )

        self.exit_btn.pack(
            fill="x",
            padx=12,
            pady=15
        )
    
    def change_page(self, page):

        self.highlight(page)

        self.on_change_page(page)

    def highlight(self, active):

        for page, btn in self.buttons.items():

            if page == active:

                btn.configure(
                    fg_color=Theme.PRIMARY,
                    hover_color=Theme.PRIMARY
                )

            else:

                btn.configure(
                    fg_color="transparent",
                    hover_color="#1f2937"
                )
    def confirm_exit(self):

        popup = ctk.CTkToplevel(self)

        popup.title("Exit")
        popup.geometry("320x160")
        popup.grab_set()

        popup.update_idletasks()

        x = self.winfo_rootx() + (
            self.winfo_width() // 2
        ) - 160

        y = self.winfo_rooty() + (
            self.winfo_height() // 2
        ) - 80

        popup.geometry(
            f"320x160+{x}+{y}"
        )

        ctk.CTkLabel(
            popup,
            text="Quitter l'application ?",
            font=("Arial",16,"bold")
        ).pack(
            pady=25
        )

        frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        frame.pack()

        ctk.CTkButton(
            frame,
            text="YES",
            width=100,
            fg_color="#16a34a",
            command=lambda: (
                popup.destroy(),
                self.master.destroy()
            )
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            frame,
            text="NO",
            width=100,
            fg_color="#dc2626",
            command=popup.destroy
        ).pack(
            side="left",
            padx=10
        )
