from app.container import Container


def main():

    container = Container()

    # 👉 TEMPORAIRE : choix GUI / CLI
    USE_GUI = True

    if USE_GUI:
        from gui.app import App

        app = App(container)
        app.mainloop()

    else:
        container.app.run()


if __name__ == "__main__":
    main()
