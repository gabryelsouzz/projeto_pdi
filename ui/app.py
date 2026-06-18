import customtkinter as ctk

from ui.state import AppState
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
