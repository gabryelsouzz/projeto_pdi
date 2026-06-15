import numpy as np

from PIL import Image
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8
from matplotlib.figure import Figure

def equalize(arr: NDArray[uint8]) -> tuple[IMG, NDArray[uint8], Figure]:

    from core.basics import compute_cdf

    _, cdf_values = compute_cdf(arr, plot=False)

    lut_equalized: NDArray[uint8] = np.round(cdf_values * 255).astype(np.uint8)
    arr_equalized: NDArray[uint8] = lut_equalized[arr]
    img_equalized: IMG = Image.fromarray(arr_equalized, mode='L')

    hist_equalized: NDArray[uint8] = np.bincount(arr_equalized.ravel(), minlength=256)

    fig: Figure = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(arr_equalized, cmap='gray', vmin=0, vmax=255)
    ax.axis('off')

    return img_equalized, hist_equalized, fig