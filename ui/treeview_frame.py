from tkinter import Frame
from tkinter import ttk

COLUMNS = (
    "Date", "Year", "Month", "Day", "Time", "IO_Caller_Number", "IO_Caller_Number_Section", "Caller_Number",
    "Caller_Channel_Code", "Caller_Channel", "IO_Called_Number", "IO_Called_Number_Section", "Called_Number",
    "Called_Channel_Code", "Called_Channel", "Ring_Time", "Talk_Time", "Status", "Details",
)


def build(window):
    container = Frame(window, relief="raised", borderwidth=5)
    tree = ttk.Treeview(container)
    y_scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    tree["columns"] = COLUMNS

    tree.heading("#0", text="ID", anchor="w")
    for column_name in COLUMNS:
        tree.column(column_name, anchor="w", width=75, stretch=False)
        tree.heading(column_name, text=column_name, anchor="w")

    container.place(width=1000, y=250)
    y_scrollbar.pack(side="left", fill="y")
    tree.pack()
    x_scrollbar.pack(side="bottom", fill="x")

    return tree
