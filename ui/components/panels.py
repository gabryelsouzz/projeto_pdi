import customtkinter as ctk


class ParamPanel(ctk.CTkFrame):
    def get_params(self) -> dict:
        return {}


class MockPanel(ParamPanel):
    def __init__(self, master, transform_name: str = "", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.transform_name: str = transform_name
        ctk.CTkLabel(
            self,
            text="Parâmetros (em breve)",
            anchor="w",
            text_color="gray60",
        ).pack(fill="x", padx=4, pady=4)
