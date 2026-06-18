from core.thresholding import threshold
from core.linear import linear_transformation, autoscale
from core.equalize import equalize
from core.match import match
from ui.components.panels import MockPanel, ThresholdPanel  

REGISTRY: dict[str, tuple] = {
    "Limiarização": (threshold, ThresholdPanel),  
    "Transformação Linear": (linear_transformation, MockPanel),
    "Alargamento de Contraste": (autoscale, MockPanel),
    "Equalização": (equalize, MockPanel),
    "Casamento de Histograma": (match, MockPanel),
}