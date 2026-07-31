import called_number
import caller_number
import datetime_splitter
import db_connection

BATCH_SIZE = 100

INSERT_SQL = """
INSERT INTO [dbo].[Separated_Info]
    (Date, Year, Month, Day, Time,
     IO_Caller_Number, IO_Caller_Number_Section, Caller_Number, Caller_Channel_Code, Caller_Channel,
     IO_Called_Number, IO_Called_Number_Section, Called_Number, Called_Channel_Code, Called_Channel,
     Ring_Time, Talk_Time, Status, Details)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

REMOVE_DUPLICATES_SQL = """
WITH cte AS (
    SELECT Date, Year, Month, Day, Time,
           IO_Caller_Number, IO_Caller_Number_Section, Caller_Number, Caller_Channel_Code, Caller_Channel,
           IO_Called_Number, IO_Called_Number_Section, Called_Number, Called_Channel_Code, Called_Channel,
           Ring_Time, Talk_Time, Status, Details,
           ROW_NUMBER() OVER (
               PARTITION BY Date, Year, Month, Day, Time,
                            IO_Caller_Number, IO_Caller_Number_Section, Caller_Number, Caller_Channel_Code, Caller_Channel,
                            IO_Called_Number, IO_Called_Number_Section, Called_Number, Called_Channel_Code, Called_Channel,
                            Ring_Time, Talk_Time, Status, Details
               ORDER BY Date
           ) AS row_number
    FROM Separated_Info
)
DELETE FROM cte WHERE row_number > 1
"""


def _split_channel(channel):
    if channel and ":" in channel:
        code, number = channel.split(":", 1)
        return code, number
    return "-", "-"


def transform(progress_callback=None):
    cursor = db_connection.connection.cursor()
    cursor.execute("SELECT * FROM Unique_Info")
    rows = cursor.fetchall()
    total = len(rows)
    batch = []

    for index, row in enumerate(rows):
        date, year, month, day, time = datetime_splitter.split(row.Date_And_Time)
        caller_section, caller_io_number = caller_number.resolve(row.Caller_Number)
        called_section, called_io_number = called_number.resolve(row.Called_Number)
        caller_channel_code, caller_channel_number = _split_channel(row.Caller_Channel)
        called_channel_code, called_channel_number = _split_channel(row.Called_Channel)

        batch.append((
            date, year, month, day, time,
            caller_io_number, caller_section, row.Caller_Number, caller_channel_code, caller_channel_number,
            called_io_number, called_section, row.Called_Number, called_channel_code, called_channel_number,
            row.Ring_Time, row.Talk_Time, row.Status, row.Details,
        ))

        if len(batch) >= BATCH_SIZE:
            cursor.executemany(INSERT_SQL, batch)
            db_connection.connection.commit()
            batch.clear()
            if progress_callback:
                progress_callback(index, total)

    if batch:
        cursor.executemany(INSERT_SQL, batch)
        db_connection.connection.commit()

    cursor.execute(REMOVE_DUPLICATES_SQL)
    db_connection.connection.commit()
