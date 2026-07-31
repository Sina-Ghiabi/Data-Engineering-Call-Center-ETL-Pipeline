from ui.dropdown_widget import Dropdown

DROPDOWN_SPECS = (
    ("Caller Section", "IO_Caller_Section"),
    ("Caller Channel Code", "Caller_Channel_Code"),
    ("Called Section", "IO_Called_Section"),
    ("Called Channel Code", "Called_Channel_Code"),
    ("Status", "Status"),
)


def build(parent, start_row: int) -> int:
    row = start_row
    for label_text, field_name in DROPDOWN_SPECS:
        dropdown = Dropdown(parent, label_text, field_name)
        dropdown.create(row)
        row += 2
    return row
