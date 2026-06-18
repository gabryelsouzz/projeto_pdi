import customtkinter as ctk

LEFT_PANEL_WIDTH: int = 260


class LeftPanel(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, width=LEFT_PANEL_WIDTH, **kwargs)

        # Prevent children from forcing a resize: width stays fixed.
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.header: ctk.CTkLabel = ctk.CTkLabel(
            self, text="Controles", anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
