from core.thresholding import threshold
from core.linear import linear_transformation, autoscale
from core.equalize import equalize
from core.match import match
from ui.components.panels import MockPanel, ThresholdPanel, LinearPanel, MatchPanel, EmptyPanel

REGISTRY: dict[str, tuple] = {
    "Limiarização": (threshold, ThresholdPanel),  
    "Transformação Linear": (linear_transformation, LinearPanel),
    "Alargamento de Contraste": (autoscale, MockPanel),
    "Equalização": (equalize,  EmptyPanel),
    "Casamento de Histograma": (match, MatchPanel),
}