import customtkinter as ctk

BOTTOM_BAR_HEIGHT: int = 32


class BottomBar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, height=BOTTOM_BAR_HEIGHT, **kwargs)

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.status: ctk.CTkLabel = ctk.CTkLabel(
            self, text="Controles inferiores", anchor="w"
        )
        self.status.grid(row=0, column=0, sticky="ew", padx=12)
