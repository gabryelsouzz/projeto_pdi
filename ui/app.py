import customtkinter as ctk

from config.assets import ICON_CHART, ICON_IMAGE, ICON_UPLOAD
from config.layout import MIN_SIZE, WINDOW_GEOMETRY, WINDOW_TITLE
from config.theme import ACCENT, DISABLED
from ui.state import AppState
from ui.render import render_image, render_histogram
from ui.ui_utils import clear_frame
from ui.widgets.placeholders import show_placeholder
from ui.widgets.left_panel import LeftPanel
from ui.widgets.central_area import CentralArea
from ui.widgets.bottom_bar import BottomBar


class App(ctk.CTk):
    def __init__(self, state: AppState) -> None:
        super().__init__()

        self.state_data: AppState = state
        self._controller = None

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_GEOMETRY)
        self.minsize(*MIN_SIZE)

        self._build_layout()

    def _build_layout(self) -> None:
        # Row 0: content (expands). Row 1: bottom bar (fixed).
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # Column 0: left panel (fixed). Column 1: central area (expands).
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.left_panel: LeftPanel = LeftPanel(
            self, on_transform_change=self._notify_transform_change
        )
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=(8, 4), pady=8)

        self.central_area: CentralArea = CentralArea(self)
        self.central_area.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)

        self.bottom_bar: BottomBar = BottomBar(self)
        self.bottom_bar.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
        )

        self.refresh()

    def bind_controller(self, controller) -> None:
        self._controller = controller

        self.bottom_bar.btn_load.configure(command=controller.on_load)
        self.bottom_bar.btn_reset.configure(command=controller.on_reset)
        self.bottom_bar.btn_save.configure(command=controller.on_save)
        self.left_panel.btn_apply.configure(command=controller.on_apply)
        self.central_area.btn_use_result.configure(command=controller.on_use_result)

        # Initialize the selected transform from the dropdown's current value
        # (the first registered transform)
        controller.on_transform_change(self.left_panel.transform_menu.get())

    def _notify_transform_change(self, name: str) -> None:
        if self._controller is not None:
            self._controller.on_transform_change(name)

    def get_current_params(self) -> dict:
        return self.left_panel.current_panel.get_params()

    def refresh(self) -> None:
        s = self.state_data
        ca = self.central_area

        if s.original_image is not None:
            render_image(ca.original_image, s.original_image)
            render_histogram(ca.original_hist, s.original_image)

            self.left_panel.btn_apply.configure(state="normal", fg_color=ACCENT)
        else:
            clear_frame(ca.original_image)
            clear_frame(ca.original_hist)

            self.left_panel.btn_apply.configure(state="disabled", fg_color=DISABLED)

            show_placeholder(
                ca.original_image,
                ICON_UPLOAD,
                "\nClique em 'Carregar' para selecionar a imagem",
            )
            show_placeholder(ca.original_hist, ICON_CHART, "\nHistograma indisponível")

        if s.result_image is not None:
            render_image(ca.result_image, s.result_image)
            render_histogram(ca.result_hist, s.result_image)

            self.bottom_bar.btn_save.configure(state="normal", fg_color=ACCENT)
            self.central_area.btn_use_result.configure(state="normal", fg_color=ACCENT)
        else:
            clear_frame(ca.result_image)
            clear_frame(ca.result_hist)

            self.bottom_bar.btn_save.configure(state="disabled", fg_color=DISABLED)
            self.central_area.btn_use_result.configure(
                state="disabled", fg_color=DISABLED
            )

            show_placeholder(
                ca.result_image, ICON_IMAGE, "\nO resultado aparecerá aqui"
            )
            show_placeholder(ca.result_hist, ICON_CHART, "\nHistograma indisponível")
