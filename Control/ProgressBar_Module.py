from tkinter import *
from tkinter.ttk import Progressbar

from View import Frame_View

#A Class To Create Multiple ProgressBars
class ProgressBar():
    def __init__(self, Text):
        self.Text = Text
        self.PB_Value = 0

    def Create_ProgressBar(self):
        self.PB_Label = Label(Frame_View.Window, text=self.Text)
        self.PB = Progressbar(Frame_View.Window, orient=HORIZONTAL, length=250, mode='determinate')
        self.PB['value'] = int(self.PB_Value)
        self.PB.place(x=375, y=550)
        self.PB_Label.place(x=450, y=570)

    def Calculate_ProgressBar (self , Index , Length):
        self.PB_Value = ((Index / Length) * 100)
        self.PB['value'] = int(self.PB_Value)

    def Destroy_ProgressBar (self) :
        self.PB.destroy()
        self.PB_Label.destroy()
