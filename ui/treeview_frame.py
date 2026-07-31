from tkinter import ttk

from ui import theme

COLUMNS = (
    "Date", "Year", "Month", "Day", "Time", "IO_Caller_Number", "IO_Caller_Number_Section", "Caller_Number",
    "Caller_Channel_Code", "Caller_Channel", "IO_Called_Number", "IO_Called_Number_Section", "Called_Number",
    "Called_Channel_Code", "Called_Channel", "Ring_Time", "Talk_Time", "Status", "Details",
)


def build(window) -> ttk.Treeview:
    card = ttk.Frame(window, style="Card.TFrame", padding=theme.PAD)
    card.columnconfigure(0, weight=1)
    card.rowconfigure(1, weight=1)
    card.grid(row=2, column=1, sticky="nsew", padx=(0, theme.PAD), pady=(0, theme.PAD))

    ttk.Label(card, text="Results", style="CardSection.TLabel").grid(row=0, column=0, sticky="w", pady=(0, theme.PAD_SMALL))

    table_frame = ttk.Frame(card, style="Card.TFrame")
    table_frame.grid(row=1, column=0, sticky="nsew")
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    tree = ttk.Treeview(table_frame, columns=COLUMNS, show="headings")
    y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    for column_name in COLUMNS:
        tree.column(column_name, anchor="w", width=110, stretch=False)
        tree.heading(column_name, text=column_name.replace("_", " "), anchor="w")

    tree.tag_configure("odd", background=theme.COLOR_SURFACE)
    tree.tag_configure("even", background=theme.COLOR_ROW_ALT)

    tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")

    return tree
