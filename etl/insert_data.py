import csv
import logging
import os
from dataclasses import dataclass
from typing import Optional

from database import db_connection
from etl.record_validator import validate

logger = logging.getLogger(__name__)

BATCH_SIZE = 100
REJECTED_ROWS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "rejected_rows.csv")

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


@dataclass
class ImportResult:
    imported: int
    rejected: int
    rejected_path: Optional[str]


def load_file(path, progress_callback=None) -> ImportResult:
    with open(path, encoding="utf-8") as handle:
        lines = [line for line in handle if line.strip() and not line.startswith("#")]

    connection = db_connection.get_connection()
    cursor = connection.cursor()
    total = len(lines)
    batch = []
    imported = 0
    rejected = []

    for index, line in enumerate(lines):
        fields = line.strip().split(",")
        reason = validate(fields)
        if reason:
            rejected.append((index + 1, reason, line.strip()))
            continue

        batch.append(tuple(fields[1:10]))

        if len(batch) >= BATCH_SIZE:
            cursor.executemany(INSERT_SQL, batch)
            connection.commit()
            imported += len(batch)
            batch.clear()
            if progress_callback:
                progress_callback(index, total)

    if batch:
        cursor.executemany(INSERT_SQL, batch)
        connection.commit()
        imported += len(batch)

    cursor.execute(REMOVE_DUPLICATES_SQL)
    connection.commit()

    rejected_path = _write_rejected_rows(rejected) if rejected else None
    if rejected:
        logger.warning("Rejected %d of %d rows from %s; see %s", len(rejected), total, path, rejected_path)

    return ImportResult(imported=imported, rejected=len(rejected), rejected_path=rejected_path)


def _write_rejected_rows(rejected) -> str:
    os.makedirs(os.path.dirname(REJECTED_ROWS_PATH), exist_ok=True)
    with open(REJECTED_ROWS_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["line_number", "reason", "raw_line"])
        writer.writerows(rejected)
    return REJECTED_ROWS_PATH
