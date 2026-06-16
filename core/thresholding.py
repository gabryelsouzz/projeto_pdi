from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import NDArray
from numpy import uint8, float64
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from PIL.Image import Image as IMG


def threshold(vector_image: NDArray[uint8], T: int = 128) -> tuple[IMG, NDArray[uint8], Figure]:

    from core.basics import compute_pdf

    result: NDArray[uint8]
    pdf:    NDArray[float64]

    result = np.where(vector_image >= T, 255, 0).astype(uint8)
    pdf, _ = compute_pdf(result)
    hist: NDArray[uint8] = np.bincount(result.ravel(), minlength=256).astype(uint8)

    fig: Figure
    ax:  Axes

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(np.arange(256), pdf, width=1, color='steelblue')
    ax.axvline(x=T, color='red', linestyle='--', label=f'T = {T}')
    ax.set_xlim(-1, 256)
    ax.set_ylim(0, pdf.max() * 1.1)
    ax.set_title(f'Histograma Resultante  (T={T})')
    ax.set_xlabel('Nível de Cinza ($r_k$)')
    ax.set_ylabel('Probabilidade $p(r_k)$')
    ax.legend()
    fig.tight_layout()
    plt.close(fig)

    pil_image: IMG = Image.fromarray(result, mode='L')

    return pil_image, hist, fig