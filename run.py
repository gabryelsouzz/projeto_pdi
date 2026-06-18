from ui.state import AppState
from ui.app import App


def main() -> None:
    app = App(AppState())
    app.mainloop()


if __name__ == "__main__":
    main()
