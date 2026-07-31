from tkinter import Label

import constants
import db_connection

DROPDOWN_COLUMNS = {
    "IO_Caller_Section": "IO_Caller_Number_Section",
    "Caller_Channel_Code": "Caller_Channel_Code",
    "IO_Called_Section": "IO_Called_Number_Section",
    "Called_Channel_Code": "Called_Channel_Code",
    "Status": "Status",
}

PERIOD_COLUMNS = (
    ("ring_time", "Ring_Time"),
    ("talk_time", "Talk_Time"),
    ("date", "Date"),
    ("time", "Time"),
)

_success_label = None


def _build_query(dropdown_selections, period_entries):
    conditions = []
    params = []

    for field_name, column_name in DROPDOWN_COLUMNS.items():
        value = dropdown_selections.get(field_name)
        if value and value != constants.SELECT_ALL_LABEL:
            conditions.append(f"{column_name} = ?")
            params.append(value)

    for field_name, column_name in PERIOD_COLUMNS:
        entry_from, entry_to = period_entries[field_name]
        value_from = entry_from.get()
        value_to = entry_to.get()
        if value_from and value_to:
            conditions.append(f"? <= {column_name} AND {column_name} <= ?")
            params.extend([value_from, value_to])
        elif value_from:
            conditions.append(f"? <= {column_name}")
            params.append(value_from)
        elif value_to:
            conditions.append(f"{column_name} <= ?")
            params.append(value_to)

    query = "SELECT * FROM Separated_Info"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    return query, params


def _show_success_label(window):
    global _success_label
    if _success_label is None:
        _success_label = Label(window, text="Report generated successfully")
        _success_label.place(x=425, y=550)


def search(window, tree, dropdown_selections, period_entries):
    tree.delete(*tree.get_children())

    query, params = _build_query(dropdown_selections, period_entries)

    cursor = db_connection.connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    db_connection.connection.commit()

    for index, row in enumerate(rows):
        tree.insert("", "end", f"item{index}", text=str(index), values=tuple(row[1:]))

    _show_success_label(window)
    dropdown_selections.clear()
