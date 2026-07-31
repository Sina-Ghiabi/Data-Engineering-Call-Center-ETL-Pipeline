from tkinter import ttk

from ui import date_format, theme, time_format, timer_format

FIELD_SPECS = (
    ("ring_time", "Ring Time", timer_format.format_timer_entry),
    ("talk_time", "Talk Time", timer_format.format_timer_entry),
    ("date", "Date", date_format.format_date_entry),
    ("time", "Time", time_format.format_time_entry),
)


class PeriodFrame:
    def __init__(self, parent):
        self.parent = parent
        self.entries = {}

    def build(self, start_row: int) -> int:
        row = start_row
        for field_name, label_text, formatter in FIELD_SPECS:
            ttk.Label(self.parent, text=label_text, style="Card.TLabel").grid(row=row, column=0, sticky="w")
            row += 1

            entries_row = ttk.Frame(self.parent, style="Card.TFrame")
            entries_row.grid(row=row, column=0, sticky="ew", pady=(0, theme.PAD_SMALL))
            entries_row.columnconfigure(0, weight=1)
            entries_row.columnconfigure(2, weight=1)
            row += 1

            entry_from = ttk.Entry(entries_row, width=10)
            entry_from.grid(row=0, column=0, sticky="ew")
            entry_from.bind("<Key>", lambda _event, w=entry_from, f=formatter: f(w))

            ttk.Label(entries_row, text="to", style="CardMuted.TLabel").grid(row=0, column=1, padx=6)

            entry_to = ttk.Entry(entries_row, width=10)
            entry_to.grid(row=0, column=2, sticky="ew")
            entry_to.bind("<Key>", lambda _event, w=entry_to, f=formatter: f(w))

            self.entries[field_name] = (entry_from, entry_to)

        return row
