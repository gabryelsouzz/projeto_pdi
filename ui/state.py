from dataclasses import dataclass

from numpy.typing import NDArray
from numpy import uint8


@dataclass
class AppState:
    original_image: NDArray[uint8] | None = None
    result_image: NDArray[uint8] | None = None
    selected_transform: str | None = None
