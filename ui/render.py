import customtkinter as ctk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageTk
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.basics import get_histogram

from ui.mocks import clear_frame

# Size used when the frame has not been sized by the layout yet.
_FALLBACK_SIZE: int = 200


def array_to_pil(array: NDArray[uint8]) -> IMG:
    return Image.fromarray(array, mode="L")


def fit_photoimage(
    array: NDArray[uint8], max_width: int, max_height: int
) -> ImageTk.PhotoImage:
    img: IMG = array_to_pil(array)
    width, height = img.size

    if max_width > 0 and max_height > 0:
        scale = min(max_width / width, max_height / height, 1.0)
        if scale < 1.0:
            img = img.resize(
                (max(1, int(width * scale)), max(1, int(height * scale))),
                Image.LANCZOS,
            )

    return ImageTk.PhotoImage(img)


def render_image(frame: ctk.CTkFrame, array: NDArray[uint8]) -> None:
    clear_frame(frame)
    frame.update_idletasks()

    max_width = frame.winfo_width() or _FALLBACK_SIZE
    max_height = frame.winfo_height() or _FALLBACK_SIZE

    photo = fit_photoimage(array, max_width, max_height)
    label = ctk.CTkLabel(frame, image=photo, text="")

    label.image = photo
    frame.photo_reference = photo
    label.pack(expand=True, fill="both", padx=4, pady=4)

def render_histogram(frame: ctk.CTkFrame, arr_image) -> None:
    clear_frame(frame)
    frame.update_idletasks()

    if arr_image is None:
        return

    try:
        arr_image = np.asarray(arr_image, dtype=np.uint8)
    
        _, fig_matplotlib = get_histogram(arr_image)

        fig_matplotlib.patch.set_facecolor('#242424')
        for ax in fig_matplotlib.axes:
            ax.set_facecolor('#242424')
            ax.tick_params(colors='gray', labelsize=8)
            ax.title.set_color('white')
            ax.title.set_size(9)
            ax.spines['bottom'].set_color('gray')
            ax.spines['left'].set_color('gray')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        fig_matplotlib.set_size_inches(4.0, 2.5)
        fig_matplotlib.tight_layout()

        canvas = FigureCanvasTkAgg(fig_matplotlib, master=frame)
        canvas_widget = canvas.get_tk_widget()
        
        canvas_widget.configure(bg='#242424', highlightthickness=0)
        canvas_widget.pack(expand=True, fill="both", padx=4, pady=4)
        
        canvas.draw()

        plt.close(fig_matplotlib)

    except Exception as e:
        print(f"[ERRO NO HISTOGRAMA]: {e}")