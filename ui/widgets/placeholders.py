import customtkinter as ctk

from config.theme import PLACEHOLDER_FONT, PLACEHOLDER_TEXT_COLOR
from ui.icons import load_icon


def show_placeholder(frame: ctk.CTkFrame, icon_path: str, text: str) -> None:
    icon = load_icon(icon_path)
    label = ctk.CTkLabel(
        frame,
        image=icon,
        text=text,
        compound="top",
        font=PLACEHOLDER_FONT,
        text_color=PLACEHOLDER_TEXT_COLOR,
    )
    # Keep a reference so the image is not garbage-collected.
    label.image = icon
    label.pack(expand=True)
