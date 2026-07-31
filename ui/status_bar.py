from tkinter import ttk

from ui import theme

STYLE_BY_KIND = {
    "info": "Status.TLabel",
    "success": "StatusSuccess.TLabel",
    "error": "StatusError.TLabel",
}


class StatusBar:
    def __init__(self, window):
        self.frame = ttk.Frame(window, style="StatusBar.TFrame", padding=(theme.PAD, theme.PAD_SMALL))
        self.frame.columnconfigure(0, weight=1)

        self.label = ttk.Label(self.frame, text="Ready", style="Status.TLabel")
        self.label.grid(row=0, column=0, sticky="w")

        self.progress = ttk.Progressbar(self.frame, mode="determinate", length=220)

    def set_message(self, text: str, kind: str = "info") -> None:
        self.label.configure(text=text, style=STYLE_BY_KIND.get(kind, "Status.TLabel"))

    def start_progress(self, text: str) -> None:
        self.set_message(text)
        self.progress["value"] = 0
        self.progress.grid(row=0, column=1, sticky="e")
        self.frame.update_idletasks()

    def update_progress(self, index: int, total: int) -> None:
        if total:
            self.progress["value"] = (index / total) * 100
        self.frame.update_idletasks()

    def finish_progress(self, text: str, kind: str = "success") -> None:
        self.progress.grid_forget()
        self.set_message(text, kind=kind)
