from tkinter import Label, OptionMenu, StringVar

import constants
from database import dropdown_values

selections = {}


class Dropdown:
    def __init__(self, parent, label_text, field_name, row, column):
        self.parent = parent
        self.label_text = label_text
        self.field_name = field_name
        self.row = row
        self.column = column
        self.value = None

    def create(self):
        self.value = StringVar(self.parent)
        self.value.set(constants.SELECT_PLACEHOLDER)

        label = Label(self.parent, text=self.label_text)
        options = dropdown_values.fetch(self.field_name)
        menu = OptionMenu(self.parent, self.value, *options, command=self._on_select)
        menu.configure(width=10)

        label.grid(row=self.row, column=self.column + 1, pady=7)
        menu.grid(row=self.row, column=self.column, pady=5)

    def _on_select(self, _event):
        selections[self.field_name] = self.value.get()
