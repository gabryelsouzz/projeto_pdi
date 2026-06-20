import customtkinter as ctk


class LabeledFrame(ctk.CTkFrame):

    def __init__(self, master: ctk.CTkBaseClass, title: str, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label: ctk.CTkLabel = ctk.CTkLabel(
            self, text=title, anchor="w", font=ctk.CTkFont(weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=8, pady=(6, 2))

        self.content: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
