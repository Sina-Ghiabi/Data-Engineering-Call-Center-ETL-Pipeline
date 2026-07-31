from tkinter import HORIZONTAL, Label
from tkinter.ttk import Progressbar


class ProgressBar:
    def __init__(self, window, text):
        self.window = window
        self.text = text
        self.value = 0
        self.label = None
        self.bar = None

    def create(self):
        self.label = Label(self.window, text=self.text)
        self.bar = Progressbar(self.window, orient=HORIZONTAL, length=250, mode="determinate")
        self.bar["value"] = int(self.value)
        self.bar.place(x=375, y=550)
        self.label.place(x=450, y=570)

    def update(self, index, total):
        self.value = (index / total) * 100
        self.bar["value"] = int(self.value)

    def destroy(self):
        self.bar.destroy()
        self.label.destroy()
