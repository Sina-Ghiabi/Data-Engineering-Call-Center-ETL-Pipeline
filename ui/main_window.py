from tkinter import Tk

from database import config
from ui import theme

window = Tk()
window.geometry(config.WINDOW_SIZE)
window.minsize(1000, 600)
window.title(config.WINDOW_TITLE)

window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(2, weight=1)

theme.apply(window)
