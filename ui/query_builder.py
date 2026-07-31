from typing import Dict, List, Tuple

import constants

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


def build_search_query(dropdown_selections: Dict[str, str], period_values: Dict[str, Tuple[str, str]]) -> Tuple[str, List[str]]:
    conditions = []
    params: List[str] = []

    for field_name, column_name in DROPDOWN_COLUMNS.items():
        value = dropdown_selections.get(field_name)
        if value and value != constants.SELECT_ALL_LABEL:
            conditions.append(f"{column_name} = ?")
            params.append(value)

    for field_name, column_name in PERIOD_COLUMNS:
        value_from, value_to = period_values.get(field_name, ("", ""))
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
