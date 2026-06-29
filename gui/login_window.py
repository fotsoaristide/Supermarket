import customtkinter as ctk
import tkinter as tk
from services.auth_service import AuthService


class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.auth = AuthService()
        self.result = None

        self.title("Login POS")
        self.geometry("400x300")
        self.update_idletasks()

        width = 400
        height = 300

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )
        self.resizable(False, False)

        self.build_ui()

        # si login désactivé → bypass automatique
        if not self.auth.login_enabled():
            self.result = ("admin", "ADMIN")
            self.after(200, self.auto_close)

    def build_ui(self):

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            self.frame,
            text="Connexion",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username"
        )
        self.username_entry.pack(
            pady=10,
            fill="x"
        )

        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.pack(
            pady=10,
            fill="x"
        )

        # curseur automatique
        self.after(
            100,
            lambda: self.username_entry.focus_force()
        )

        # ENTER sur username -> password
        self.username_entry.bind(
            "<Return>",
            lambda e: self.password_entry.focus_force()
        )

        # ENTER sur password -> login
        self.password_entry.bind(
            "<Return>",
            lambda e: self.login()
        )

        self.status = ctk.CTkLabel(
            self.frame,
            text="",
            text_color="red"
        )
        self.status.pack(pady=5)

        ctk.CTkButton(
            self.frame,
            text="LOGIN",
            command=self.login
        ).pack(pady=10, fill="x")

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        result = self.auth.authenticate(username, password)

        if result:
            self.result = result
            self.auto_close()
        else:
            self.status.configure(text="Invalid credentials")

    def auto_close(self):
        self.quit()
        self.destroy()
