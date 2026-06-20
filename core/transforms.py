from typing import Callable

from core.thresholding import threshold
from core.linear import linear_transformation, autoscale
from core.equalize import equalize
from core.match import match
from core.types import ProcessingResult

# A transform takes the original image array plus keyword params and returns a
# ProcessingResult.
TransformFn = Callable[..., ProcessingResult]

TRANSFORMS: dict[str, TransformFn] = {
    "Limiarização": threshold,
    "Transformação Linear": linear_transformation,
    "Autoescala": autoscale,
    "Equalização": equalize,
    "Casamento de Histograma": match,
}
