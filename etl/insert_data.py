from database import db_connection

BATCH_SIZE = 100

INSERT_SQL = """
INSERT INTO [dbo].[Unique_Info]
    (Date_And_Time, Caller_Number, Caller_Channel, Called_Number, Called_Channel, Ring_Time, Talk_Time, Status, Details)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

REMOVE_DUPLICATES_SQL = """
WITH cte AS (
    SELECT Date_And_Time, Caller_Number, Caller_Channel, Called_Number, Called_Channel,
           Ring_Time, Talk_Time, Status, Details,
           ROW_NUMBER() OVER (
               PARTITION BY Date_And_Time, Caller_Number, Caller_Channel, Called_Number,
                            Called_Channel, Ring_Time, Talk_Time, Status, Details
               ORDER BY Date_And_Time
           ) AS row_number
    FROM Unique_Info
)
DELETE FROM cte WHERE row_number > 1
"""


def load_file(path, progress_callback=None):
    with open(path, encoding="utf-8") as handle:
        lines = [line for line in handle if line.strip() and not line.startswith("#")]

    connection = db_connection.get_connection()
    cursor = connection.cursor()
    total = len(lines)
    batch = []

    for index, line in enumerate(lines):
        fields = line.strip().split(",")
        if len(fields) < 10:
            continue
        batch.append(tuple(fields[1:10]))

        if len(batch) >= BATCH_SIZE:
            cursor.executemany(INSERT_SQL, batch)
            connection.commit()
            batch.clear()
            if progress_callback:
                progress_callback(index, total)

    if batch:
        cursor.executemany(INSERT_SQL, batch)
        connection.commit()

    cursor.execute(REMOVE_DUPLICATES_SQL)
    connection.commit()
