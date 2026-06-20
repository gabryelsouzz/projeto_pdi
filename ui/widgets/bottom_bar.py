import customtkinter as ctk

from config.assets import ICON_DOWNLOAD, ICON_RESET, ICON_UPLOAD
from config.layout import BUTTON_HEIGHT
from ui.icons import load_icon


class BottomBar(ctk.CTkFrame):

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, **kwargs)

        # Keep references so the CTkImage objects are not garbage-collected.
        self._upload_icon = load_icon(ICON_UPLOAD, white=True)
        self._reset_icon = load_icon(ICON_RESET, white=True)
        self._download_icon = load_icon(ICON_DOWNLOAD, white=True)
        # btn_save toggles disabled; gray variant shown when disabled.
        self._download_icon_disabled = load_icon(ICON_DOWNLOAD)

        self.btn_load: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Carregar",
            image=self._upload_icon,
            compound="left",
            width=100,
            height=BUTTON_HEIGHT,
        )
        self.btn_load.pack(side="left", padx=(12, 4), pady=4)

        self.btn_save: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Salvar",
            image=self._download_icon,
            compound="left",
            width=120,
            height=BUTTON_HEIGHT,
        )
        self.btn_save.icon_enabled = self._download_icon
        self.btn_save.icon_disabled = self._download_icon_disabled
        self.btn_save.pack(side="left", padx=4, pady=4)

        self.btn_reset: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Resetar",
            image=self._reset_icon,
            compound="left",
            width=100,
            height=BUTTON_HEIGHT,
        )
        self.btn_reset.pack(side="left", padx=4, pady=4)
