from tkinter import Frame

from dropdown_widget import Dropdown

DROPDOWN_SPECS = (
    ("Caller Section:", "IO_Caller_Section", 0),
    ("Caller Channel Code:", "Caller_Channel_Code", 1),
    ("Called Section:", "IO_Called_Section", 2),
    ("Called Channel Code:", "Called_Channel_Code", 3),
    ("Status:", "Status", 4),
)


def build(window):
    frame = Frame(window, width=150, height=100, relief="raised")
    frame.place(width=200, height=200, x=720, y=10)

    for label_text, field_name, row in DROPDOWN_SPECS:
        dropdown = Dropdown(frame, label_text, field_name, row, 0)
        dropdown.create()

    return frame
