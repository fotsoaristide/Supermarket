import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme


class SettingsView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Settings")

        self.ui = ui
        self.auth = ui.auth_service

        self.build_ui()
        self.load_users()

    # =========================
    # UI
    # =========================
    def build_ui(self):

        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        # ================= AUTH =================
        auth_frame = ctk.CTkFrame(self.body)
        auth_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            auth_frame,
            text="AUTH SETTINGS",
            font=Theme.SUBTITLE
        ).pack(pady=10)

        self.login_toggle = ctk.CTkSwitch(
            auth_frame,
            text="Enable Login"
        )
        self.login_toggle.pack(pady=10)

        self.login_toggle.select() if self.auth.login_enabled() else self.login_toggle.deselect()

        ctk.CTkButton(
            auth_frame,
            text="SAVE AUTH SETTINGS",
            command=self.save_auth
        ).pack(fill="x", pady=10)

        # ================= USERS =================
        user_frame = ctk.CTkFrame(self.body)
        user_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            user_frame,
            text="USERS MANAGEMENT",
            font=Theme.SUBTITLE
        ).pack(pady=10)

        self.users_box = ctk.CTkScrollableFrame(user_frame)
        self.users_box.pack(fill="both", expand=True)

        # add user form
        self.username_entry = ctk.CTkEntry(user_frame, placeholder_text="Username")
        self.username_entry.pack(fill="x", pady=5)

        self.password_entry = ctk.CTkEntry(user_frame, placeholder_text="Password")
        self.password_entry.pack(fill="x", pady=5)

        self.role_menu = ctk.CTkOptionMenu(
            user_frame,
            values=["ADMIN", "USER"]
        )
        self.role_menu.pack(fill="x", pady=5)

        ctk.CTkButton(
            user_frame,
            text="ADD USER",
            command=self.add_user
        ).pack(fill="x", pady=5)

    # =========================
    # AUTH SAVE
    # =========================
    def save_auth(self):

        if not self.ask_confirmation(
            "Confirmation",
            "Save authentication settings ?"
        ):
            return

        value = self.login_toggle.get() == 1

        self.auth.set_login_enabled(value)

        self.show_success(
            "Settings saved"
        )

    # =========================
    # USERS
    # =========================
    def load_users(self):

        for w in self.users_box.winfo_children():
            w.destroy()

        users = self.auth.get_users()

        for u in users:

            row = ctk.CTkFrame(self.users_box)
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row,
                text=f"{u['username']} ({u['role']})"
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                row,
                text="DEL",
                width=60,
                fg_color="red",
                command=lambda name=u["username"]: self.delete_user(name)
            ).pack(side="right", padx=5)

    def add_user(self):

        if not self.ask_confirmation(
            "Confirmation",
            "Create this user ?"
        ):
            return

        try:

            self.auth.add_user(
                self.username_entry.get(),
                self.password_entry.get(),
                self.role_menu.get()
            )

            self.load_users()

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            self.show_success(
                "User added"
            )

        except Exception as e:

            self.show_message(
                str(e)
            )

    def delete_user(self, username):

        if not self.ask_confirmation(
            "Confirmation",
            f"Delete user '{username}' ?"
        ):
            return

        self.auth.delete_user(username)

        self.load_users()

        self.show_success(
            "User deleted"
        )

    # =========================
    # UI MESSAGE
    # =========================
    def show_message(self, text):

        popup = ctk.CTkToplevel(self)
        popup.geometry("250x120")
        popup.title("Info")
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text=text
        ).pack(expand=True)

    # =========================
    # CONFIRMATION
    # =========================
    def ask_confirmation(self, title, message):

        popup = ctk.CTkToplevel(self)

        popup.title(title)
        popup.geometry("350x180")
        popup.transient(self)
        popup.grab_set()

        popup.update_idletasks()

        x = self.winfo_rootx() + (
            self.winfo_width() // 2
        ) - 175

        y = self.winfo_rooty() + (
            self.winfo_height() // 2
        ) - 90

        popup.geometry(f"350x180+{x}+{y}")

        result = {"ok": False}

        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 16, "bold")
        ).pack(pady=(30, 20))

        frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        frame.pack(pady=10)

        def yes():
            result["ok"] = True
            popup.destroy()

        def no():
            popup.destroy()

        ctk.CTkButton(
            frame,
            text="YES",
            width=100,
            fg_color="#16a34a",
            command=yes
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="NO",
            width=100,
            fg_color="#dc2626",
            command=no
        ).pack(side="left", padx=10)

        popup.wait_window()

        return result["ok"]

    # =========================
    # SUCCESS MESSAGE
    # =========================
    def show_success(self, text):

        popup = ctk.CTkToplevel(self)

        popup.title("Success")
        popup.geometry("300x140")
        popup.transient(self)
        popup.grab_set()

        popup.update_idletasks()

        x = self.winfo_rootx() + (
            self.winfo_width() // 2
        ) - 150

        y = self.winfo_rooty() + (
            self.winfo_height() // 2
        ) - 70

        popup.geometry(f"300x140+{x}+{y}")

        ctk.CTkLabel(
            popup,
            text="✓",
            font=("Arial", 30, "bold"),
            text_color="#16a34a"
        ).pack(pady=(20, 0))

        ctk.CTkLabel(
            popup,
            text=text,
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.after(
            1500,
            popup.destroy
        )
    

