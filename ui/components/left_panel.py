from typing import Callable

import customtkinter as ctk

from ui.registry import REGISTRY
from ui.components.panels import ParamPanel

LEFT_PANEL_WIDTH: int = 260


class LeftPanel(ctk.CTkFrame):

    def __init__(
        self,
        master,
        on_transform_change: Callable[[str], None] | None = None,
        **kwargs,
    ):
        super().__init__(master, width=LEFT_PANEL_WIDTH, **kwargs)

        # Prevent children from forcing a resize: width stays fixed.
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self._on_transform_change_cb = on_transform_change

        self.header: ctk.CTkLabel = ctk.CTkLabel(
            self,
            text="Transformação",
            anchor="w",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)

        names: list[str] = list(REGISTRY.keys())
        self.transform_menu: ctk.CTkOptionMenu = ctk.CTkOptionMenu(
            self, values=names, command=self._on_transform_change
        )
        self.transform_menu.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))

        # Container that hosts the current parameter panel (polymorphic swap).
        self.panel_container: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_container.grid(row=2, column=0, sticky="new", padx=12, pady=(0, 8))
        self.panel_container.grid_columnconfigure(0, weight=1)

        self.current_panel: ParamPanel | None = None
        self._on_transform_change(names[0])  # instantiate the initial panel

        self.grid_rowconfigure(3, weight=1)

        self.btn_apply: ctk.CTkButton = ctk.CTkButton(self, text="Aplicar")
        self.btn_apply.grid(row=4, column=0, sticky="ew", padx=12, pady=12)

    def _on_transform_change(self, name: str) -> None:
        if self.current_panel is not None:
            self.current_panel.destroy()

        _, panel_cls = REGISTRY[name]
        self.current_panel = panel_cls(self.panel_container, transform_name=name)
        self.current_panel.grid(row=0, column=0, sticky="ew")

        if self._on_transform_change_cb is not None:
            self._on_transform_change_cb(name)
