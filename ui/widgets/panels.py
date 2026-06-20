from tkinter import filedialog
from typing import Any

import customtkinter as ctk

from config.assets import (
    ICON_CHECK,
    ICON_ERROR,
    ICON_FOLDER,
    ICON_IMAGE,
)
from config.params import (
    B_DEFAULT,
    B_RANGE,
    C_DEFAULT,
    C_RANGE,
    THRESHOLD_DEFAULT,
    THRESHOLD_RANGE,
)
from core.utils import load
from ui.icons import load_icon


class ParamPanel(ctk.CTkFrame):
    """Base class for transformation parameter panels.

    Subclasses build their own widgets and expose the chosen parameters as a
    keyword-argument dict via ``get_params()``.
    """

    def get_params(self) -> dict[str, Any]:
        return {}


class MockPanel(ParamPanel):
    def __init__(
        self, master: ctk.CTkBaseClass, transform_name: str = "", **kwargs
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.transform_name: str = transform_name
        ctk.CTkLabel(
            self,
            text="Parâmetros (em breve)",
            anchor="w",
            text_color="gray60",
        ).pack(fill="x", padx=4, pady=4)


class ThresholdPanel(ParamPanel):
    def __init__(
        self, master: ctk.CTkBaseClass, transform_name: str = "", **kwargs
    ) -> None:
        super().__init__(master, **kwargs)

        self.threshold_value = ctk.IntVar(value=THRESHOLD_DEFAULT)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=15)

        label = ctk.CTkLabel(frame, text="Limiar (T):", font=("Arial", 13))
        label.pack(side="left", padx=5)

        self.slider = ctk.CTkSlider(
            frame,
            from_=THRESHOLD_RANGE[0],
            to=THRESHOLD_RANGE[1],
            variable=self.threshold_value,
            width=180,
        )
        self.slider.pack(side="left", padx=10)

        self.value_label = ctk.CTkLabel(
            frame, text=str(THRESHOLD_DEFAULT), font=("Arial", 13, "bold")
        )
        self.value_label.pack(side="left", padx=5)

        self.slider.configure(command=self._update_label)

    def _update_label(self, value: float) -> None:
        self.value_label.configure(text=f"{int(value)}")

    def get_params(self) -> dict[str, Any]:
        return {"T": self.threshold_value.get()}


class LinearPanel(ParamPanel):
    def __init__(
        self, master: ctk.CTkBaseClass, transform_name: str = "", **kwargs
    ) -> None:
        super().__init__(master, **kwargs)

        self.c_value = ctk.DoubleVar(value=C_DEFAULT)
        self.b_value = ctk.DoubleVar(value=B_DEFAULT)

        frame_c = ctk.CTkFrame(self, fg_color="transparent")
        frame_c.pack(fill="x", padx=15, pady=5)

        label_c = ctk.CTkLabel(frame_c, text="Fator C (contraste):", font=("Arial", 12))
        label_c.pack(side="left", padx=5)

        slider_c = ctk.CTkSlider(
            frame_c,
            from_=C_RANGE[0],
            to=C_RANGE[1],
            variable=self.c_value,
            width=150,
        )
        slider_c.pack(side="left", padx=10)

        self.c_label = ctk.CTkLabel(frame_c, text="1.0", font=("Arial", 12, "bold"))
        self.c_label.pack(side="left", padx=5)
        slider_c.configure(command=self._update_c_label)

        frame_b = ctk.CTkFrame(self, fg_color="transparent")
        frame_b.pack(fill="x", padx=15, pady=5)

        label_b = ctk.CTkLabel(frame_b, text="Fator B (brilho):", font=("Arial", 12))
        label_b.pack(side="left", padx=5)

        slider_b = ctk.CTkSlider(
            frame_b,
            from_=B_RANGE[0],
            to=B_RANGE[1],
            variable=self.b_value,
            width=150,
        )
        slider_b.pack(side="left", padx=10)

        self.b_label = ctk.CTkLabel(frame_b, text="0", font=("Arial", 12, "bold"))
        self.b_label.pack(side="left", padx=5)
        slider_b.configure(command=self._update_b_label)

    def _update_c_label(self, value: float) -> None:
        self.c_label.configure(text=f"{float(value):.1f}")

    def _update_b_label(self, value: float) -> None:
        self.b_label.configure(text=f"{int(value)}")

    def get_params(self) -> dict[str, Any]:
        return {"c": self.c_value.get(), "b": self.b_value.get()}


class MatchPanel(ParamPanel):
    def __init__(
        self, master: ctk.CTkBaseClass, transform_name: str = "", **kwargs
    ) -> None:
        super().__init__(master, **kwargs)

        self.reference_path: str | None = None
        self.reference_array = None

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=15)

        self._image_icon = load_icon(ICON_IMAGE)
        label = ctk.CTkLabel(
            frame,
            text="Imagem de Referência:",
            image=self._image_icon,
            compound="left",
            font=("Arial", 13),
        )
        label.pack(pady=(5, 5))

        self.file_label = ctk.CTkLabel(
            frame,
            text="Nenhum arquivo selecionado",
            font=("Arial", 12, "italic"),
        )
        self.file_label.pack(pady=5)

        self._check_icon = load_icon(ICON_CHECK)
        self._error_icon = load_icon(ICON_ERROR)

        self._folder_icon = load_icon(ICON_FOLDER, white=True)
        btn_select = ctk.CTkButton(
            frame,
            text="Selecionar imagem",
            image=self._folder_icon,
            compound="left",
            command=self._select_file,
            width=180,
        )
        btn_select.pack(pady=10)

    def _select_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecione a imagem de referência",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")],
        )

        if path:
            try:
                _img, self.reference_array = load(path)
                self.reference_path = path

                name = path.split("/")[-1]
                self.file_label.configure(
                    text=name,
                    image=self._check_icon,
                    compound="left",
                    text_color="green",
                )

            except Exception as e:
                self.file_label.configure(
                    text=f"Erro: {e}",
                    image=self._error_icon,
                    compound="left",
                    text_color="red",
                )
                self.reference_array = None

    def get_params(self) -> dict[str, Any]:
        if self.reference_array is None:
            raise ValueError("Selecione uma imagem de referência!")
        return {"img_ref": self.reference_array}


class EmptyPanel(ParamPanel):
    def __init__(
        self, master: ctk.CTkBaseClass, transform_name: str = "", **kwargs
    ) -> None:
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(
            self,
            text="Nenhum parâmetro necessário",
            font=("Arial", 14, "italic"),
        )
        label.pack(pady=30, padx=20)

    def get_params(self) -> dict[str, Any]:
        return {}


# Maps each transformation name (see core.transforms.TRANSFORMS) to the panel
# class that collects its parameters.
PANEL_FOR: dict[str, type[ParamPanel]] = {
    "Limiarização": ThresholdPanel,
    "Transformação Linear": LinearPanel,
    "Alargamento de Contraste": MockPanel,
    "Equalização": EmptyPanel,
    "Casamento de Histograma": MatchPanel,
}
