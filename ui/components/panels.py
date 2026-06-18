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
    
class LinearPanel(ParamPanel):
    def __init__(self, master, transform_name: str = "", **kwargs):
        super().__init__(master, **kwargs)
        
        self.valor_c = ctk.DoubleVar(value=1.0)  
        self.valor_b = ctk.DoubleVar(value=0)    
        
        frame_c = ctk.CTkFrame(self, fg_color="transparent")
        frame_c.pack(fill="x", padx=15, pady=5)
        
        label_c = ctk.CTkLabel(frame_c, text="Fator C (contraste):", font=("Arial", 12))
        label_c.pack(side="left", padx=5)
        
        slider_c = ctk.CTkSlider(
            frame_c,
            from_=0.0,
            to=3.0,
            variable=self.valor_c,
            width=150
        )
        slider_c.pack(side="left", padx=10)
        
        self.label_c = ctk.CTkLabel(frame_c, text="1.0", font=("Arial", 12, "bold"))
        self.label_c.pack(side="left", padx=5)
        slider_c.configure(command=self._atualizar_label_c)
        
        frame_b = ctk.CTkFrame(self, fg_color="transparent")
        frame_b.pack(fill="x", padx=15, pady=5)
        
        label_b = ctk.CTkLabel(frame_b, text="Fator B (brilho):", font=("Arial", 12))
        label_b.pack(side="left", padx=5)
        
        slider_b = ctk.CTkSlider(
            frame_b,
            from_=-255,
            to=255,
            variable=self.valor_b,
            width=150
        )
        slider_b.pack(side="left", padx=10)
        
        self.label_b = ctk.CTkLabel(frame_b, text="0", font=("Arial", 12, "bold"))
        self.label_b.pack(side="left", padx=5)
        slider_b.configure(command=self._atualizar_label_b)
    
    def _atualizar_label_c(self, valor):
        self.label_c.configure(text=f"{float(valor):.1f}")
    
    def _atualizar_label_b(self, valor):
        self.label_b.configure(text=f"{int(valor)}")
    
    def get_params(self) -> dict:
        return {"c": self.valor_c.get(), "b": self.valor_b.get()}
    
class MatchPanel(ParamPanel):
    def __init__(self, master, transform_name: str = "", **kwargs):
        super().__init__(master, **kwargs)
        
        from tkinter import filedialog
        from PIL import Image
        import numpy as np
        
        self.caminho_referencia = None
        self.imagem_referencia = None
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=15)
        
        label = ctk.CTkLabel(
            frame,
            text="📸 Imagem de Referência:",
            font=("Arial", 13)
        )
        label.pack(pady=(5, 5))
        
        self.label_arquivo = ctk.CTkLabel(
            frame,
            text="Nenhum arquivo selecionado",
            font=("Arial", 12, "italic")
        )
        self.label_arquivo.pack(pady=5)
        
        btn_selecionar = ctk.CTkButton(
            frame,
            text="📁 Selecionar imagem",
            command=self._selecionar_arquivo,
            width=180
        )
        btn_selecionar.pack(pady=10)
    
    def _selecionar_arquivo(self):
        from tkinter import filedialog
        from PIL import Image
        import numpy as np
        
        arquivo = filedialog.askopenfilename(
            title="Selecione a imagem de referência",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if arquivo:
            try:
                img = Image.open(arquivo).convert('L')
                self.imagem_referencia = np.array(img)
                self.caminho_referencia = arquivo
                
                nome = arquivo.split("/")[-1]
                self.label_arquivo.configure(text=f"✅ {nome}", text_color="green")
                print(f"📸 Referência carregada: {nome}")
                
            except Exception as e:
                self.label_arquivo.configure(text=f"❌ Erro: {e}", text_color="red")
                self.imagem_referencia = None
    
    def get_params(self) -> dict:
        if self.imagem_referencia is None:
            raise ValueError("Selecione uma imagem de referência!")
        return {"img_ref": self.imagem_referencia}