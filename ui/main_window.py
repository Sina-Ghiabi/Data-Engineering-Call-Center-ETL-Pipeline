from tkinter import Tk

from database import config

window = Tk()
window.geometry(config.WINDOW_SIZE)
window.resizable(False, False)
window.title(config.WINDOW_TITLE)
