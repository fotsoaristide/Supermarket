from app.container import Container
from gui.app import App
from gui.login_window import LoginWindow

def main():

    login = LoginWindow()
    login.protocol("WM_DELETE_WINDOW", login.quit)
    login.mainloop()

    if login.result:

        username, role = login.result

        container = Container()

        container.current_user = username
        container.current_role = role

        app = App(container)
        app.mainloop()


if __name__ == "__main__":
    main()
