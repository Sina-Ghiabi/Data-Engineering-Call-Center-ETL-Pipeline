from tkinter import ttk

from ui import theme


def build(window) -> ttk.Frame:
    frame = ttk.Frame(window, style="Header.TFrame", padding=(theme.PAD, theme.PAD_SMALL))

    ttk.Label(frame, text="Call Center Analytics", style="HeaderTitle.TLabel").pack(anchor="w")
    ttk.Label(
        frame, text="Import call records, filter them, and export or chart the results.", style="HeaderSubtitle.TLabel"
    ).pack(anchor="w")

    return frame
