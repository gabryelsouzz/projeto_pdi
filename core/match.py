import numpy as np

from PIL import Image
from typing import Final
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8
from basics import compute_cdf

def match(img_orig: IMG, img_ref: IMG) -> tuple[IMG, NDArray[uint8]]:
    
    arr_orig: NDArray[uint8] = np.array(img_orig, dtype=np.uint8)
    arr_ref: NDArray[uint8] = np.array(img_ref, dtype=np.uint8)
    
    _, cdf_orig = compute_cdf(arr_orig, plot=False)
    _, cdf_ref = compute_cdf(arr_ref, plot=False)
    
    lut_match: Final[list[int]] = np.zeros(256, dtype=np.uint8)

    for g_orig in range(256):
        
        differences = np.abs(cdf_ref - cdf_orig[g_orig])
        g_ref = np.argmin(differences)
        
        lut_match[g_orig] = g_ref
        
    arr_matched: NDArray[uint8] = lut_match[arr_orig]
    
    img_matched: IMG = Image.fromarray(arr_matched, mode='L')
    
    return img_matched, arr_matched