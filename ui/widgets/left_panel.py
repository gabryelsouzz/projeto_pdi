from typing import Callable

import customtkinter as ctk

from config.assets import ICON_PLAY
from config.layout import BUTTON_HEIGHT, LEFT_PANEL_WIDTH
from core.transforms import TRANSFORMS
from ui.icons import load_icon
from ui.widgets.panels import PANEL_FOR, ParamPanel


class LeftPanel(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_transform_change: Callable[[str], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, width=LEFT_PANEL_WIDTH, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self._on_transform_change_cb = on_transform_change

        self.header = ctk.CTkLabel(
            self,
            text="Transformação",
            anchor="w",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)

        names = list(TRANSFORMS.keys())
        self.transform_menu = ctk.CTkOptionMenu(
            self, values=names, command=self._on_transform_change
        )
        self.transform_menu.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))

        self.panel_container = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_container.grid(row=2, column=0, sticky="new", padx=12, pady=(0, 8))
        self.panel_container.grid_columnconfigure(0, weight=1)

        self.current_panel: ParamPanel | None = None
        self._on_transform_change(names[0])

        self.grid_rowconfigure(3, weight=1)
        # Keep references so the CTkImage objects are not garbage-collected.
        # White while enabled, gray once disabled.
        self._play_icon = load_icon(ICON_PLAY, white=True)
        self._play_icon_disabled = load_icon(ICON_PLAY)
        self.btn_apply = ctk.CTkButton(
            self,
            text="Aplicar",
            image=self._play_icon,
            compound="left",
            height=BUTTON_HEIGHT,
        )
        self.btn_apply.icon_enabled = self._play_icon
        self.btn_apply.icon_disabled = self._play_icon_disabled
        self.btn_apply.grid(row=4, column=0, sticky="ew", padx=12, pady=12)

    def _on_transform_change(self, name: str) -> None:
        if self.current_panel is not None:
            self.current_panel.destroy()

        panel_cls = PANEL_FOR[name]
        self.current_panel = panel_cls(self.panel_container, transform_name=name)
        self.current_panel.grid(row=0, column=0, sticky="ew")

        if self._on_transform_change_cb is not None:
            self._on_transform_change_cb(name)
