from controllers.app_controller import AppController
from ui.app import App
from ui.dialogs import DialogService
from ui.state import AppState


def main() -> None:
    state = AppState()
    view = App(state)
    controller = AppController(state, view, DialogService(view))
    view.bind_controller(controller)
    view.mainloop()


if __name__ == "__main__":
    main()
