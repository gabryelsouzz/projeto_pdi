import customtkinter as ctk

from PIL import Image as PILImage
from PIL.Image import Image as IMG

# Tint colors for monochrome placeholder icons, per appearance mode.
# Light gray for dark backgrounds, darker gray for light backgrounds.
LIGHT_TINT: tuple[int, int, int] = (110, 110, 110)
DARK_TINT: tuple[int, int, int] = (160, 160, 160)


def tint_icon(img: IMG, color: tuple[int, int, int]) -> IMG:
    """Recolor a monochrome icon to a flat color, keeping its alpha silhouette."""
    img = img.convert("RGBA")
    solid = PILImage.new("RGBA", img.size, color + (0,))
    solid.putalpha(img.getchannel("A"))
    return solid


def load_icon(path: str, size: int = 28) -> ctk.CTkImage:
    """Load a PNG icon as a theme-aware CTkImage tinted for light/dark modes."""
    base = PILImage.open(path).convert("RGBA")
    return ctk.CTkImage(
        light_image=tint_icon(base, LIGHT_TINT),
        dark_image=tint_icon(base, DARK_TINT),
        size=(size, size),
    )
