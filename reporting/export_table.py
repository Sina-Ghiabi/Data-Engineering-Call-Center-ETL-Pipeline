import re
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from database import db_connection

TABLE_PREFIX = "Export_"
BATCHES_TABLE_NAME = "Export_Batches"
NAME_PATTERN = re.compile(r"[^A-Za-z0-9_]+")

CREATE_BATCHES_TABLE_SQL = f"""
IF OBJECT_ID('dbo.{BATCHES_TABLE_NAME}', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.{BATCHES_TABLE_NAME} (
        BatchID INT IDENTITY(1,1) PRIMARY KEY,
        TableName NVARCHAR(128) NOT NULL,
        ExportedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        FilterCriteria NVARCHAR(MAX) NOT NULL,
        RecordCount INT NOT NULL
    );
END
"""


class InvalidTableNameError(ValueError):
    pass


@dataclass
class ExportResult:
    table_name: str
    batch_id: int
    row_count: int


def sanitize_table_name(raw_name: str) -> str:
    name = NAME_PATTERN.sub("_", raw_name.strip()).strip("_")
    if not name:
        raise InvalidTableNameError("Table name must contain at least one letter, digit, or underscore.")
    if name[0].isdigit():
        name = f"T_{name}"
    return name[:100]


def full_table_name(raw_name: str) -> str:
    return TABLE_PREFIX + sanitize_table_name(raw_name)


def list_export_tables() -> List[str]:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "SELECT name FROM sys.tables WHERE name LIKE ? AND name <> ? ORDER BY name",
        (f"{TABLE_PREFIX}%", BATCHES_TABLE_NAME),
    )
    return [row.name[len(TABLE_PREFIX):] for row in cursor.fetchall()]


def _ensure_export_table(cursor, full_name: str, columns: Sequence[str]) -> None:
    column_defs = ",\n            ".join(f"[{column}] NVARCHAR(200)" for column in columns)
    cursor.execute(
        f"""
        IF OBJECT_ID('dbo.{full_name}', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.{full_name} (
                ExportRowID INT IDENTITY(1,1) PRIMARY KEY,
                ExportBatchID INT NOT NULL REFERENCES dbo.{BATCHES_TABLE_NAME}(BatchID),
                {column_defs}
            );
        END
        """
    )


def export_rows(
    raw_name: str, columns: Sequence[str], rows: Sequence[Tuple], filter_criteria: str
) -> ExportResult:
    full_name = full_table_name(raw_name)
    connection = db_connection.get_connection()
    cursor = connection.cursor()

    cursor.execute(CREATE_BATCHES_TABLE_SQL)
    _ensure_export_table(cursor, full_name, columns)

    cursor.execute(
        f"INSERT INTO dbo.{BATCHES_TABLE_NAME} (TableName, FilterCriteria, RecordCount) "
        "OUTPUT INSERTED.BatchID VALUES (?, ?, ?)",
        (full_name, filter_criteria, len(rows)),
    )
    batch_id = cursor.fetchone()[0]

    if rows:
        placeholders = ", ".join("?" for _ in columns)
        column_list = ", ".join(f"[{column}]" for column in columns)
        insert_sql = (
            f"INSERT INTO dbo.{full_name} (ExportBatchID, {column_list}) "
            f"VALUES (?, {placeholders})"
        )
        cursor.executemany(insert_sql, [(batch_id, *row) for row in rows])

    connection.commit()
    return ExportResult(table_name=full_name, batch_id=batch_id, row_count=len(rows))
