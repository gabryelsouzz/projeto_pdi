import customtkinter as ctk

from PIL import Image, ImageTk
from PIL.Image import Image as IMG
from numpy.typing import NDArray
from numpy import uint8

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
    # Keep the reference alive so the garbage collector does not drop the image.
    label.image = photo
    label.pack(expand=True, fill="both", padx=4, pady=4)
