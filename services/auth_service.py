import json
import os


class AuthService:

    def __init__(self):

        self.file = "config/users.json"

        os.makedirs("config", exist_ok=True)

        if not os.path.exists(self.file):
            self._create_default()

    def _create_default(self):

        data = {
            "login_enabled": True,
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "ADMIN"
                },
                {
                    "username": "cashier",
                    "password": "1234",
                    "role": "USER"
                }
            ]
        }

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load(self):

        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def login_enabled(self):

        return self.load()["login_enabled"]

    def authenticate(self, username, password):

        data = self.load()

        for user in data["users"]:

            if (
                user["username"] == username
                and
                user["password"] == password
            ):
                return (
                    user["username"],
                    user["role"]
                )

        return None
    
    def get_users(self):
        data = self.load()
        return data.get("users", [])


    def set_login_enabled(self, value: bool):
        data = self.load()
        data["login_enabled"] = value
        self.save(data)


    def add_user(self, username, password, role="USER"):
        data = self.load()

        # éviter doublons
        for u in data["users"]:
            if u["username"] == username:
                raise Exception("User already exists")

        data["users"].append({
            "username": username,
            "password": password,
            "role": role
        })

        self.save(data)


    def delete_user(self, username):
        data = self.load()
        data["users"] = [
            u for u in data["users"]
            if u["username"] != username
        ]
        self.save(data)


    def update_password(self, username, new_password):
        data = self.load()

        for u in data["users"]:
            if u["username"] == username:
                u["password"] = new_password
                break

        self.save(data)
