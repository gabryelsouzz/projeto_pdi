from tkinter import filedialog, messagebox

import customtkinter as ctk
import numpy as np

from core.utils import load
from ui.registry import REGISTRY
from ui.state import AppState
from ui.render import render_image, render_histogram
from ui.icons import load_icon
from ui.mocks import clear_frame
from ui.components.left_panel import LeftPanel
from ui.components.central_area import CentralArea
from ui.components.bottom_bar import BottomBar
from PIL import Image as PILImage


class App(ctk.CTk):

    def __init__(self, state: AppState):
        super().__init__()

        self.state_data: AppState = state

        self.title("Projeto PDI")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self._build_layout()

    def _build_layout(self) -> None:
        # Row 0: content (expands). Row 1: bottom bar (fixed).
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # Column 0: left panel (fixed). Column 1: central area (expands).
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.left_panel: LeftPanel = LeftPanel(
            self, on_transform_change=self._on_transform_change
        )
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=(8, 4), pady=8)

        self.central_area: CentralArea = CentralArea(self)
        self.central_area.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)

        self.bottom_bar: BottomBar = BottomBar(self)
        self.bottom_bar.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
        )

        self.bottom_bar.btn_load.configure(command=self._on_load)
        self.bottom_bar.btn_reset.configure(command=self._on_reset)
        self.bottom_bar.btn_save.configure(command=self._on_save)
        self.left_panel.btn_apply.configure(command=self._on_apply)
        self.central_area.btn_use_result.configure(command=self._on_use_result)

        self.update_screens()

    def update_screens(self) -> None:
        s = self.state_data
        ca = self.central_area

        if s.original_image is not None:
            render_image(ca.original_image, s.original_image)

            render_histogram(ca.original_hist, s.original_image)

            self.left_panel.btn_apply.configure(state="normal", fg_color="#1f538d")

        else:
            clear_frame(ca.original_image)
            clear_frame(ca.original_hist)

            self.left_panel.btn_apply.configure(state="disabled", fg_color="#525252")

            icon_img_orig = load_icon("ui/assets/upload.png")

            placeholder_img_orig = ctk.CTkLabel(
                ca.original_image,
                image=icon_img_orig,
                text="\nClique em 'Carregar' para selecionar a imagem",
                compound="top",
                font=("Arial", 13, "italic"),
                text_color="gray",
            )

            placeholder_img_orig.image = icon_img_orig
            placeholder_img_orig.pack(expand=True)

            icon_hist_orig = load_icon("ui/assets/chart-column.png")

            placeholder_hist_orig = ctk.CTkLabel(
                ca.original_hist,
                image=icon_hist_orig,
                text="\nHistograma indisponível",
                compound="top",
                font=("Arial", 13, "italic"),
                text_color="gray",
            )

            placeholder_hist_orig.image = icon_hist_orig
            placeholder_hist_orig.pack(expand=True)

        if s.result_image is not None:
            render_image(ca.result_image, s.result_image)
            render_histogram(ca.result_hist, s.result_image)

            self.bottom_bar.btn_save.configure(state="normal", fg_color="#1f538d")
            self.central_area.btn_use_result.configure(
                state="normal", fg_color="#1f538d"
            )
        else:
            clear_frame(ca.result_image)
            clear_frame(ca.result_hist)

            self.bottom_bar.btn_save.configure(state="disabled", fg_color="#525252")
            self.central_area.btn_use_result.configure(
                state="disabled", fg_color="#525252"
            )

            icon_img_res = load_icon("ui/assets/image.png")

            placeholder_img_res = ctk.CTkLabel(
                ca.result_image,
                image=icon_img_res,
                text="\nO resultado aparecerá aqui",
                compound="top",
                font=("Arial", 13, "italic"),
                text_color="gray",
            )

            placeholder_img_res.image = icon_img_res
            placeholder_img_res.pack(expand=True)

            icon_hist_res = load_icon("ui/assets/chart-column.png")

            placeholder_hist_res = ctk.CTkLabel(
                ca.result_hist,
                image=icon_hist_res,
                text="\nHistograma indisponível",
                compound="top",
                font=("Arial", 13, "italic"),
                text_color="gray",
            )

            placeholder_hist_res.image = icon_hist_res
            placeholder_hist_res.pack(expand=True)

    def _on_load(self) -> None:
        path = filedialog.askopenfilename(
            title="Carregar imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("Todos", "*.*"),
            ],
        )
        if not path:
            return

        try:
            _img, arr = load(path)
        except Exception as e:
            messagebox.showerror(
                title="Erro ao carregar",
                message=f"Não foi possível abrir a imagem.\n"
                f"Verifique se o arquivo é uma imagem válida.\n\n{e}",
            )
            return
        self.state_data.original_image = arr
        self.state_data.result_image = None
        self.update_screens()

    def _on_apply(self) -> None:
        s = self.state_data
        if s.original_image is None:
            messagebox.showwarning(
                title="Nenhuma imagem",
                message="Carregue uma imagem antes de aplicar uma transformação.",
            )
            return
        func, _ = REGISTRY.get(s.selected_transform, (None, None))
        if func is None:
            messagebox.showerror(
                title="Erro",
                message=f"Transformação '{s.selected_transform}' não encontrada.",
            )
            return
        try:
            params = self.left_panel.current_panel.get_params()
            result = func(s.original_image, **params)
        except ValueError as e:
            messagebox.showwarning(title="Parâmetro inválido", message=str(e))
            return
        except Exception as e:
            messagebox.showerror(
                title="Erro ao aplicar",
                message=f"Falha ao aplicar a transformação.\n\n{e}",
            )
            return
        s.result_image = np.asarray(result.image, dtype=np.uint8)
        self.update_screens()

    def _on_transform_change(self, name: str) -> None:
        self.state_data.selected_transform = name

    def _on_reset(self) -> None:
        self.state_data.result_image = None
        self.update_screens()

    def _on_use_result(self) -> None:
        s = self.state_data
        if s.result_image is None:
            return
        s.original_image = s.result_image.copy()
        s.result_image = None
        self.update_screens()

    def _on_save(self) -> None:
        s = self.state_data

        path = filedialog.asksaveasfilename(
            title="Salvar imagem",
            defaultextension=".png",
            filetypes=[
                ("Imagem PNG", "*.png"),
                ("Imagem JPEG", "*.jpg;*.jpeg"),
                ("Imagem BMP", "*.bmp"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if not path:
            return

        try:
            img_to_save = PILImage.fromarray(s.result_image, mode="L")

            img_to_save.save(path)

            messagebox.showinfo(title="Sucesso", message="Imagem salva com sucesso!")

        except Exception as e:
            messagebox.showerror(
                title="Erro", message=f"Não foi possível salvar a imagem:\n{str(e)}"
            )
