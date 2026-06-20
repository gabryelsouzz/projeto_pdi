from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import NDArray
from numpy import uint8, float64, int64
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from PIL.Image import Image as IMG

from core.types import ProcessingResult


def linear_transformation(vector_image: NDArray[uint8], c: float64, b: float64) -> ProcessingResult:

    from core.basics import compute_pdf
    
    result: NDArray[uint8]
    pdf:    NDArray[float64]

    result  = np.clip(c * vector_image.astype(np.float64) + b, 0, 255).astype(uint8)
    pdf = compute_pdf(result)
    hist: NDArray[int64] = np.bincount(result.ravel(), minlength=256).astype(int64)

    fig: Figure
    ax:  Axes

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(np.arange(256), pdf, width=1, color='steelblue')
    ax.set_xlim(-1, 256)
    ax.set_ylim(0, pdf.max() * 1.1)
    ax.set_title(f'Histograma Resultante  (c={c}, b={b})')
    ax.set_xlabel('Nível de Cinza ($r_k$)')
    ax.set_ylabel('Probabilidade $p(r_k)$')
    fig.tight_layout()
    plt.close(fig)

    pil_image: IMG = Image.fromarray(result, mode='L')

    return ProcessingResult(process_name="Linear Transformation" ,image=pil_image, histogram=hist, figure=fig)


def autoscale(vector_image: NDArray[uint8]) -> ProcessingResult:
    r_min: float64 = float64(vector_image.min())
    r_max: float64 = float64(vector_image.max())

    if r_max == r_min:
        c: float64 = float64(1.0)
        b: float64 = float64(0.0)
    else:
        c = float64(255.0 / (r_max - r_min))
        b = float64(-c * r_min)


    return linear_transformation(vector_image, c, b)

