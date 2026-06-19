"""Mocks das costuras consumidas pelo fluxo principal.

Enquanto os fluxos paralelos (P1: imagem/arquivo, P2: histograma) não entregam,
o principal usa estes mocks. Mock e real devem ter a mesma assinatura — a troca
futura é só apontar o import para o módulo real.
"""

import customtkinter as ctk

from numpy.typing import NDArray
from numpy import uint8


def clear_frame(frame: ctk.CTkFrame) -> None:
    """Remove o conteúdo atual de um quadro (estado vazio / pré-render)."""
    for child in frame.winfo_children():
        child.destroy()


def render_image(frame: ctk.CTkFrame, array: NDArray[uint8]) -> None:
    """Mock: desenha um retângulo cinza rotulado no lugar da imagem real."""
    clear_frame(frame)
    height, width = array.shape[:2]
    placeholder = ctk.CTkLabel(
        frame,
        text=f"[imagem {width}×{height}]",
        fg_color="gray30",
        corner_radius=6,
    )
    placeholder.pack(expand=True, fill="both", padx=4, pady=4)


def render_histogram(frame: ctk.CTkFrame, data: NDArray) -> None:
    """Mock: desenha barras estáticas falsas no lugar do histograma real.

    ``data`` é o vetor de contagem (``np.bincount``, shape ``(256,)``); o mock
    o ignora e apenas indica que há histograma a renderizar.
    """
    clear_frame(frame)
    placeholder = ctk.CTkLabel(
        frame,
        text="▁▃▅▇▅▃▁  (histograma mock)",
        fg_color="gray20",
        corner_radius=6,
    )
    placeholder.pack(expand=True, fill="both", padx=4, pady=4)
