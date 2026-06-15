import numpy as np

from PIL import Image
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8
from matplotlib.figure import Figure

def match(arr_orig: NDArray[uint8], img_ref: IMG) -> tuple[IMG, NDArray[uint8], Figure]:

    from core.basics import compute_cdf

    arr_ref: NDArray[uint8] = np.array(img_ref, dtype=np.uint8)

    _, cdf_orig = compute_cdf(arr_orig, plot=False)
    _, cdf_ref  = compute_cdf(arr_ref,  plot=False)

    lut_match: NDArray[uint8] = np.zeros(256, dtype=np.uint8)

    for g_orig in range(256):
        differences = np.abs(cdf_ref - cdf_orig[g_orig])
        g_ref = np.argmin(differences)
        lut_match[g_orig] = g_ref

    arr_matched: NDArray[uint8] = lut_match[arr_orig]
    img_matched: IMG = Image.fromarray(arr_matched, mode='L')

    hist_matched: NDArray[np.uint8] = np.bincount(arr_matched.ravel(), minlength=256)

    fig: Figure = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(arr_matched, cmap='gray', vmin=0, vmax=255)
    ax.axis('off')

    return img_matched, hist_matched, fig