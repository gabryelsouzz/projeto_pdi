import customtkinter as ctk

from PIL import Image as PILImage
from PIL.Image import Image as IMG

from config.assets import ICON_SIZE
from config.theme import DARK_TINT, LIGHT_TINT


def tint_icon(img: IMG, color: tuple[int, int, int]) -> IMG:
    img = img.convert("RGBA")
    solid = PILImage.new("RGBA", img.size, color + (0,))
    solid.putalpha(img.getchannel("A"))
    return solid


def load_icon(path: str, size: int = ICON_SIZE) -> ctk.CTkImage:
    base = PILImage.open(path).convert("RGBA")
    return ctk.CTkImage(
        light_image=tint_icon(base, LIGHT_TINT),
        dark_image=tint_icon(base, DARK_TINT),
        size=(size, size),
    )
