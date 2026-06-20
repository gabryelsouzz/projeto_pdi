import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from numpy.typing import NDArray
from numpy import uint8, float64, intp
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def get_histogram(arr: NDArray[np.uint8]) -> tuple[NDArray[np.int64], Figure]:

    fig: Figure = Figure(figsize=(10, 6))
    ax: Axes = fig.add_subplot(1, 1, 1)

    hist_data: NDArray[np.int64] = np.bincount(arr.ravel(), minlength=256)

    ax.hist(arr.ravel(), bins=256, range=(0, 256))

    fig.tight_layout()
    return hist_data, fig


def compute_pdf(vector_image: NDArray[uint8]) -> NDArray[float64]:

    vector_image = vector_image.astype(uint8)

    pixels_appears: NDArray[intp] = np.bincount(vector_image.ravel(), minlength=256)
    pdf_float: NDArray[float64] = pixels_appears / vector_image.size

    return pdf_float


def compute_cdf(
    vector_image: NDArray[uint8], plot: bool = True
) -> tuple[Figure | None, NDArray[float64]]:

    pdf_values: NDArray[float64] = compute_pdf(vector_image)
    cdf_values: NDArray[float64] = pdf_values.cumsum()

    if not plot:
        return (None, cdf_values)

    fig: Figure = Figure(figsize=(14, 8))

    gs = gridspec.GridSpec(
        nrows=2,
        ncols=2,
        figure=fig,
        width_ratios=[1, 1],
        wspace=0.3,
        height_ratios=[1, 1],
        hspace=0.4,
    )

    ax1: Axes = fig.add_subplot(gs[0, 0])
    ax2: Axes = fig.add_subplot(gs[0, 1])
    ax3: Axes = fig.add_subplot(gs[1, 0])
    ax4: Axes = fig.add_subplot(gs[1, 1])

    sections = [
        (ax1, 0, 101, "Faixa 0-100"),
        (ax2, 100, 151, "Faixa 100-150"),
        (ax3, 150, 256, "Faixa 150-256"),
    ]

    for ax, start, end, title in sections:
        x = np.arange(start, end)
        ax.bar(x, cdf_values[start:end], width=1)

        ax.set_title(title)
        ax.set_xlabel("Nível de cinza")
        ax.set_ylabel("Prob. acumulada")
        ax.set_xlim(start, end - 1)
        ax.set_ylim(cdf_values[start], min(cdf_values[end - 1] + 0.01, 1.0))

    ax4.bar(np.arange(256), cdf_values, width=1, color="gray", alpha=0.6)
    ax4.set_title("CDF Completa (referência)")

    ax4.set_xlabel("Nível de cinza")
    ax4.set_ylabel("Prob. acumulada")
    ax4.set_xlim(0, 255)
    ax4.set_ylim(0, 1)

    return (fig, cdf_values)
