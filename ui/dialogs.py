from tkinter import filedialog, messagebox


class DialogService:
    def __init__(self, parent=None) -> None:
        self._parent = parent

    def ask_open_image(self) -> str:
        return filedialog.askopenfilename(
            title="Carregar imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("Todos", "*.*"),
            ],
        )

    def ask_save_image(self) -> str:
        return filedialog.asksaveasfilename(
            title="Salvar imagem",
            defaultextension=".png",
            filetypes=[
                ("Imagem PNG", "*.png"),
                ("Imagem JPEG", "*.jpg;*.jpeg"),
                ("Imagem BMP", "*.bmp"),
                ("Todos os arquivos", "*.*"),
            ],
        )

    def show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title=title, message=message)

    def show_warning(self, title: str, message: str) -> None:
        messagebox.showwarning(title=title, message=message)

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title=title, message=message)
