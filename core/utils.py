from PIL import Image
import numpy as np

from numpy import uint8
from PIL.Image import Image as IMG
from numpy.typing import NDArray


def load(path: str) -> tuple[IMG, NDArray[uint8]]:
    with Image.open(path) as _img:
        img: IMG = _img.convert("L")
        arr: NDArray[uint8] = np.array(img, dtype=uint8)
    return img, arr


def save(img: IMG, path: str) -> None:
    img.save(path)


def save_array(arr: NDArray[uint8], path: str) -> None:
    save(Image.fromarray(arr, mode="L"), path)
