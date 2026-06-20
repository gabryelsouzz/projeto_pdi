import customtkinter as ctk

from config.assets import ICON_ARROW_BACK
from config.layout import BUTTON_HEIGHT
from ui.icons import load_icon
from ui.widgets.labeled_frame import LabeledFrame


class CentralArea(ctk.CTkFrame):

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, **kwargs)

        # Rows 0 and 2 are the frames (expand); row 1 is the divider (fixed);
        # row 3 holds the "use result as input" button (fixed).
        self.grid_columnconfigure((0, 1), weight=1, uniform="frames")
        self.grid_rowconfigure((0, 2), weight=1, uniform="frames")
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(3, weight=0)

        original_image_frame = LabeledFrame(self, title="Imagem Original")
        original_image_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        original_hist_frame = LabeledFrame(self, title="Histograma Original")
        original_hist_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        # Horizontal divider between the original row and the result row.
        self.divider: ctk.CTkFrame = ctk.CTkFrame(self, height=2, fg_color="gray50")
        self.divider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4)

        result_image_frame = LabeledFrame(self, title="Imagem Resultante")
        result_image_frame.grid(row=2, column=0, sticky="nsew", padx=4, pady=4)

        result_hist_frame = LabeledFrame(self, title="Histograma Resultante")
        result_hist_frame.grid(row=2, column=1, sticky="nsew", padx=4, pady=4)

        # Keep references so the CTkImage objects are not garbage-collected.
        # White while enabled, gray once disabled.
        self._arrow_back_icon = load_icon(ICON_ARROW_BACK, white=True)
        self._arrow_back_icon_disabled = load_icon(ICON_ARROW_BACK)
        self.btn_use_result: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Usar resultado como entrada",
            image=self._arrow_back_icon,
            compound="left",
            height=BUTTON_HEIGHT,
        )
        self.btn_use_result.icon_enabled = self._arrow_back_icon
        self.btn_use_result.icon_disabled = self._arrow_back_icon_disabled
        self.btn_use_result.grid(row=3, column=0, sticky="ew", padx=4, pady=(0, 4))

        self.original_image: ctk.CTkFrame = original_image_frame.content
        self.original_hist: ctk.CTkFrame = original_hist_frame.content
        self.result_image: ctk.CTkFrame = result_image_frame.content
        self.result_hist: ctk.CTkFrame = result_hist_frame.content
