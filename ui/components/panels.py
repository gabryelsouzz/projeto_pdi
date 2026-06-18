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
    

class ThresholdPanel(ParamPanel):
    def __init__(self, master, transform_name: str = "", **kwargs):
        super().__init__(master, **kwargs)
        
        self.valor_T = ctk.IntVar(value=128)
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=15)
        
        label = ctk.CTkLabel(frame, text="Limiar (T):", font=("Arial", 13))
        label.pack(side="left", padx=5)
        
        self.slider = ctk.CTkSlider(
            frame,
            from_=0,
            to=255,
            variable=self.valor_T,
            width=180
        )
        self.slider.pack(side="left", padx=10)
        
        self.label_valor = ctk.CTkLabel(frame, text="128", font=("Arial", 13, "bold"))
        self.label_valor.pack(side="left", padx=5)
        
        self.slider.configure(command=self._atualizar_label)
    
    def _atualizar_label(self, valor):  
        self.label_valor.configure(text=f"{int(valor)}")
    
    def get_params(self) -> dict:  
        return {"T": self.valor_T.get()}