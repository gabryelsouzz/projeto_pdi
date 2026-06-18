from core.thresholding import threshold
from core.linear import linear_transformation, autoscale
from core.equalize import equalize
from core.match import match
from ui.components.panels import MockPanel

REGISTRY: dict[str, tuple] = {
    "Limiarização": (threshold, MockPanel),
    "Transformação Linear": (linear_transformation, MockPanel),
    "Alargamento de Contraste": (autoscale, MockPanel),
    "Equalização": (equalize, MockPanel),
    "Casamento de Histograma": (match, MockPanel),
}
