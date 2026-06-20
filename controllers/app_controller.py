from typing import Protocol

import numpy as np

from core.transforms import TRANSFORMS
from core.utils import load, save_array
from ui.state import AppState


class View(Protocol):
    def refresh(self) -> None: ...
    def get_current_params(self) -> dict: ...


class Dialogs(Protocol):
    def ask_open_image(self) -> str: ...
    def ask_save_image(self) -> str: ...
    def show_info(self, title: str, message: str) -> None: ...
    def show_warning(self, title: str, message: str) -> None: ...
    def show_error(self, title: str, message: str) -> None: ...


class AppController:
    def __init__(self, state: AppState, view: View, dialogs: Dialogs) -> None:
        self.state = state
        self.view = view
        self.dialogs = dialogs

    def on_load(self) -> None:
        path = self.dialogs.ask_open_image()
        if not path:
            return

        try:
            _img, arr = load(path)
        except Exception as e:
            self.dialogs.show_error(
                title="Erro ao carregar",
                message=f"Não foi possível abrir a imagem.\n"
                f"Verifique se o arquivo é uma imagem válida.\n\n{e}",
            )
            return

        self.state.original_image = arr
        self.state.result_image = None
        self.view.refresh()

    def on_apply(self) -> None:
        s = self.state
        if s.original_image is None:
            self.dialogs.show_warning(
                title="Nenhuma imagem",
                message="Carregue uma imagem antes de aplicar uma transformação.",
            )
            return

        func = TRANSFORMS.get(s.selected_transform)
        if func is None:
            self.dialogs.show_error(
                title="Erro",
                message=f"Transformação '{s.selected_transform}' não encontrada.",
            )
            return

        try:
            params = self.view.get_current_params()
            result = func(s.original_image, **params)
        except ValueError as e:
            self.dialogs.show_warning(title="Parâmetro inválido", message=str(e))
            return
        except Exception as e:
            self.dialogs.show_error(
                title="Erro ao aplicar",
                message=f"Falha ao aplicar a transformação.\n\n{e}",
            )
            return

        s.result_image = np.asarray(result.image, dtype=np.uint8)
        self.view.refresh()

    def on_transform_change(self, name: str) -> None:
        self.state.selected_transform = name

    def on_reset(self) -> None:
        self.state.result_image = None
        self.view.refresh()

    def on_use_result(self) -> None:
        s = self.state
        if s.result_image is None:
            return
        s.original_image = s.result_image.copy()
        s.result_image = None
        self.view.refresh()

    def on_save(self) -> None:
        path = self.dialogs.ask_save_image()
        if not path:
            return

        try:
            save_array(self.state.result_image, path)
            self.dialogs.show_info(title="Sucesso", message="Imagem salva com sucesso!")
        except Exception as e:
            self.dialogs.show_error(
                title="Erro", message=f"Não foi possível salvar a imagem:\n{str(e)}"
            )
