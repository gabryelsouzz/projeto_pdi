import numpy as np

from PIL import Image
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8
from matplotlib.figure import Figure

from core.types import ProcessingResult


def equalize(arr: NDArray[uint8]) -> ProcessingResult:

    from core.basics import compute_cdf

    _, cdf_values = compute_cdf(arr, plot=False)

    lut_equalized: NDArray[uint8] = np.round(cdf_values * 255).astype(np.uint8)
    arr_equalized: NDArray[uint8] = lut_equalized[arr]
    img_equalized: IMG = Image.fromarray(arr_equalized, mode='L')

    hist_equalized: NDArray[uint8] = np.bincount(arr_equalized.ravel(), minlength=256).astype(uint8)

    fig: Figure = Figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(np.arange(256), hist_equalized, width=1, color='steelblue')
    ax.set_xlim(-1, 256)
    ax.set_title('Histograma Resultante')
    ax.set_xlabel('Nível de Cinza ($r_k$)')
    ax.set_ylabel('Contagem')
    fig.tight_layout()

    return ProcessingResult(process_name="Equalize" ,image=img_equalized, histogram=hist_equalized, figure=fig)