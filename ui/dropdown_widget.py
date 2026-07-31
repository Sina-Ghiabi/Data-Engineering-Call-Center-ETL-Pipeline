from tkinter import StringVar, ttk

import constants
from database import dropdown_values
from ui import theme

selections = {}


class Dropdown:
    def __init__(self, parent, label_text, field_name):
        self.parent = parent
        self.label_text = label_text
        self.field_name = field_name
        self.variable = StringVar()

    def create(self, row: int) -> None:
        ttk.Label(self.parent, text=self.label_text, style="Card.TLabel").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )

        options = dropdown_values.fetch(self.field_name)
        combo = ttk.Combobox(self.parent, textvariable=self.variable, values=options, state="readonly")
        combo.set(constants.SELECT_PLACEHOLDER)
        combo.grid(row=row + 1, column=0, sticky="ew", pady=(0, theme.PAD_SMALL))
        combo.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, _event) -> None:
        selections[self.field_name] = self.variable.get()
