from tkinter import *

from Control import Get_Dropdown_Values
from View import Main_View

Dictionary = {}

#A Class To Create Multiple Dropdowns
class Dropdown:
    def __init__(self, Dropdown_Label, Dropdown, Dropdown_Row, Dropdown_Column):
        self.Dropdown_Label = Dropdown_Label
        self.Dropdown = Dropdown
        self.Dropdown_Row = Dropdown_Row
        self.Dropdown_Column = Dropdown_Column
        self.Result = None
        self.Dropdown_Value = None
        self.List = []

    def Create_Dropdown(self):
        self.Dropdown_Value = StringVar(Main_View.Frame_View.Window)
        self.Dropdown_Value.set("انتخاب")
        Dropdown_Label = Label(Main_View.Dropdowns_Frame, text=self.Dropdown_Label)
        Dropdown = OptionMenu(Main_View.Dropdowns_Frame, self.Dropdown_Value, Get_Dropdown_Values.Get_Dropdown_Value(self),
                              command=self.Return_Value)
        Dropdown.configure(width=10)

        Dropdown_Label.grid(row=self.Dropdown_Row, column=self.Dropdown_Column + 1, pady=7)
        Dropdown.grid(row=self.Dropdown_Row, column=self.Dropdown_Column, pady=5)

    def Return_Value(self, event):
        Value = self.Dropdown_Value.get()
        Dictionary[self.Dropdown] = Value
