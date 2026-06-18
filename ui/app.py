from tkinter import filedialog

import customtkinter as ctk
import numpy as np

from core.utils import load
from ui.state import AppState
from ui.render import render_image
from ui.mocks import render_histogram, clear_frame
from ui.components.left_panel import LeftPanel
from ui.components.central_area import CentralArea
from ui.components.bottom_bar import BottomBar


class App(ctk.CTk):

    def __init__(self, state: AppState):
        super().__init__()

        self.state_data: AppState = state

        self.title("Projeto PDI")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self._build_layout()

    def _build_layout(self) -> None:
        # Row 0: content (expands). Row 1: bottom bar (fixed).
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # Column 0: left panel (fixed). Column 1: central area (expands).
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.left_panel: LeftPanel = LeftPanel(self)
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=(8, 4), pady=8)

        self.central_area: CentralArea = CentralArea(self)
        self.central_area.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)

        self.bottom_bar: BottomBar = BottomBar(self)
        self.bottom_bar.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
        )

        self.bottom_bar.btn_load.configure(command=self._on_load)
        self.bottom_bar.btn_reset.configure(command=self._on_reset)
        self.central_area.btn_use_result.configure(command=self._on_use_result)

        self.update_screens()

    def update_screens(self) -> None:
        s = self.state_data
        ca = self.central_area

        if s.original_image is not None:
            render_image(ca.original_image, s.original_image)
            render_histogram(
                ca.original_hist,
                np.bincount(s.original_image.ravel(), minlength=256),
            )
        else:
            clear_frame(ca.original_image)
            clear_frame(ca.original_hist)

        if s.result_image is not None:
            render_image(ca.result_image, s.result_image)
            render_histogram(
                ca.result_hist,
                np.bincount(s.result_image.ravel(), minlength=256),
            )
        else:
            clear_frame(ca.result_image)
            clear_frame(ca.result_hist)

    def _on_load(self) -> None:
        path = filedialog.askopenfilename(
            title="Carregar imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("Todos", "*.*"),
            ],
        )
        if not path:
            return
        _img, arr = load(path)
        self.state_data.original_image = arr
        self.state_data.result_image = None
        self.update_screens()

    def _on_reset(self) -> None:
        self.state_data.result_image = None
        self.update_screens()

    def _on_use_result(self) -> None:
        s = self.state_data
        if s.result_image is None:
            return
        s.original_image = s.result_image.copy()
        s.result_image = None
        self.update_screens()
