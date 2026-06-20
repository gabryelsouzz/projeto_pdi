import customtkinter as ctk

from config.theme import ACCENT, DISABLED


def clear_frame(frame: ctk.CTkFrame) -> None:
    for child in frame.winfo_children():
        child.destroy()


def set_button_enabled(btn: ctk.CTkButton, enabled: bool) -> None:
    state = "normal" if enabled else "disabled"
    fg = ACCENT if enabled else DISABLED
    icon = getattr(btn, "icon_enabled" if enabled else "icon_disabled", None)
    if icon is not None:
        btn.configure(state=state, fg_color=fg, image=icon)
    else:
        btn.configure(state=state, fg_color=fg)
