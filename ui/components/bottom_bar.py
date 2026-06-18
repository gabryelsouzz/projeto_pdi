import customtkinter as ctk

BOTTOM_BAR_HEIGHT: int = 32


class BottomBar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, height=BOTTOM_BAR_HEIGHT, **kwargs)

        self.pack_propagate(False)

        self.btn_load: ctk.CTkButton = ctk.CTkButton(self, text="Carregar", width=100)
        self.btn_load.pack(side="left", padx=(12, 4), pady=2)

        self.btn_reset: ctk.CTkButton = ctk.CTkButton(self, text="Resetar", width=100)
        self.btn_reset.pack(side="left", pady=2)

        self.btn_save: ctk.CTkButton = ctk.CTkButton(
            self, 
            text="Salvar", 
            width=120,
        )
        self.btn_save.pack(side="right", padx=12, pady=2)
