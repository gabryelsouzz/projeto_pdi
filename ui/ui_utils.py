import customtkinter as ctk


def clear_frame(frame: ctk.CTkFrame) -> None:
    for child in frame.winfo_children():
        child.destroy()
