from tkinter import Entry, Frame, Label, StringVar

import date_format
import time_format
import timer_format

FIELD_SPECS = (
    ("ring_time", "Ring time from:", "0:00", timer_format.format_timer_entry),
    ("talk_time", "Talk time from:", "0:00", timer_format.format_timer_entry),
    ("date", "Date from:", "1399/01/01", date_format.format_date_entry),
    ("time", "Time from:", "08:00:00", time_format.format_time_entry),
)


class PeriodFrame:
    def __init__(self, window):
        self.window = window
        self.entries = {}

    def build(self):
        container = Frame(self.window, relief="raised")
        container.place(x=100, y=15)

        labels_frame = Frame(container)
        textboxes_frame = Frame(container)
        placeholders_frame = Frame(container)

        labels_frame.grid(row=0, column=2)
        textboxes_frame.grid(row=0, column=1)
        placeholders_frame.grid(row=0, column=0)

        for row, (field_name, label_text, placeholder, formatter) in enumerate(FIELD_SPECS):
            Label(labels_frame, text=label_text, pady=8).grid(row=row, column=3)
            Label(placeholders_frame, text=placeholder, fg="snow4", pady=8).grid(row=row, column=0)

            entry_from = Entry(textboxes_frame, width=25, textvariable=StringVar())
            entry_from.bind("<Key>", lambda _event, e=entry_from, f=formatter: f(e))
            entry_from.grid(row=row, column=2, pady=8)

            Label(textboxes_frame, text="to", pady=8).grid(row=row, column=1)

            entry_to = Entry(textboxes_frame, width=25, textvariable=StringVar())
            entry_to.bind("<Key>", lambda _event, e=entry_to, f=formatter: f(e))
            entry_to.grid(row=row, column=0, pady=8)

            self.entries[field_name] = (entry_from, entry_to)

        return container
