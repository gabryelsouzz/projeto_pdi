from PIL import Image
import numpy as np

from numpy import uint8
from PIL.Image import Image as IMG
from numpy.typing import NDArray

def load(path: str) -> tuple[IMG, NDArray[uint8]]:
    img: IMG = Image.open(path).convert("L")  # escala de cinza de 8 bits
    arr: NDArray[uint8] = np.array(img, dtype=uint8)
    return img, arr

def save(img: IMG, path: str) -> None:
    img.save(path)
