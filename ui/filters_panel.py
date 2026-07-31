from tkinter import ttk

from ui import dropdowns_frame, theme
from ui.period_frame import PeriodFrame


class FiltersPanel:
    def __init__(self, window):
        self.card = ttk.Frame(window, style="Card.TFrame", padding=theme.PAD, width=280)
        self.card.grid_propagate(False)
        self.card.columnconfigure(0, weight=1)
        self.period_frame = PeriodFrame(self.card)
        self._next_row = 0

    def build(self) -> ttk.Frame:
        ttk.Label(self.card, text="Filters", style="CardSection.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, theme.PAD_SMALL)
        )
        next_row = dropdowns_frame.build(self.card, start_row=1)

        ttk.Label(self.card, text="Time Range", style="CardSection.TLabel").grid(
            row=next_row, column=0, sticky="w", pady=(theme.PAD, theme.PAD_SMALL)
        )
        self._next_row = self.period_frame.build(start_row=next_row + 1)

        return self.card

    def add_filter_button(self, command) -> ttk.Button:
        button = ttk.Button(self.card, text="Filter", style="Accent.TButton", command=command)
        button.grid(row=self._next_row, column=0, sticky="ew", pady=(theme.PAD, 0))
        return button

    @property
    def entries(self):
        return self.period_frame.entries
