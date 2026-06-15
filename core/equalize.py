import numpy as np

from PIL import Image
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8

def equalize(img: IMG) -> tuple[IMG, NDArray[uint8]]:
    
    from core.basics import compute_cdf

    arr: NDArray[uint8] = np.array(img, np.uint8)
    
    _, cdf_values = compute_cdf(arr, plot=False)
    
    lut_equalized: NDArray[uint8] = np.round(cdf_values * 255).astype(uint8)
    arr_equalized: NDArray[uint8] = lut_equalized[arr]
    img_equalized: IMG = Image.fromarray(arr_equalized, mode='L')
    
    return (img_equalized, arr_equalized)