from typing import NamedTuple
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8, int64
from matplotlib.figure import Figure

class ProcessingResult(NamedTuple):
    """
    Attributes
    ----------
    process_name: str
        Nome do processo aplicado

    image : IMG
        Imagem resultante da operação, no formato PIL (modo 'L', escala de cinza 8 bits).

    histogram : NDArray[uint8]
        Histograma da imagem resultante como vetor de contagem bruta (``np.bincount``).
        Shape: ``(256,)`` — cada índice ``i`` contém o número de pixels com intensidade ``i``.

    figure : Figure
        Figura Matplotlib com o gráfico de barras do histograma resultante.
    """
    process_name: str
    image: IMG
    histogram: NDArray[uint8] | NDArray[int64]
    figure: Figure