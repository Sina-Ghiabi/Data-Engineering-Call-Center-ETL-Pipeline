from database import db_connection

ALLOWED_DROPDOWNS = {
    "IO_Caller_Section",
    "Caller_Channel_Code",
    "IO_Called_Section",
    "Called_Channel_Code",
    "Status",
}


def fetch(dropdown_name):
    if dropdown_name not in ALLOWED_DROPDOWNS:
        raise ValueError(f"Unknown dropdown: {dropdown_name}")

    connection = db_connection.get_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT {dropdown_name} FROM Dropdown_{dropdown_name}")
    rows = cursor.fetchall()
    connection.commit()
    return [" | ".join(row) for row in rows]
