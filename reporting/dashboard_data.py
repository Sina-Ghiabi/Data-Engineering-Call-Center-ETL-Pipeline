from collections import defaultdict
from typing import List, Tuple

from database import db_connection
from reporting.duration import to_seconds

ChartData = Tuple[List[str], List[float]]


def status_breakdown() -> ChartData:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "SELECT Status, COUNT(*) AS Total FROM Separated_Info GROUP BY Status ORDER BY Total DESC"
    )
    rows = cursor.fetchall()
    return [row.Status for row in rows], [row.Total for row in rows]


def origin_mix() -> ChartData:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "SELECT IO_Caller_Number_Section, COUNT(*) AS Total FROM Separated_Info "
        "GROUP BY IO_Caller_Number_Section ORDER BY Total DESC"
    )
    rows = cursor.fetchall()
    return [row.IO_Caller_Number_Section for row in rows], [row.Total for row in rows]


def monthly_call_volume() -> ChartData:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "SELECT Year, Month, COUNT(*) AS Total FROM Separated_Info "
        "GROUP BY Year, Month ORDER BY Year, CAST(Month AS INT)"
    )
    rows = cursor.fetchall()
    labels = [f"{row.Year}-{int(row.Month):02d}" for row in rows]
    return labels, [row.Total for row in rows]


def average_talk_time_by_origin() -> ChartData:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "SELECT IO_Caller_Number_Section, Talk_Time FROM Separated_Info WHERE Status = 'answered'"
    )
    totals = defaultdict(lambda: [0, 0])
    for row in cursor.fetchall():
        seconds = to_seconds(row.Talk_Time)
        if seconds is None:
            continue
        bucket = totals[row.IO_Caller_Number_Section]
        bucket[0] += seconds
        bucket[1] += 1

    labels = list(totals.keys())
    averages = [total / count for total, count in totals.values()]
    return labels, averages


def top_channels(limit: int = 10) -> ChartData:
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        f"SELECT TOP {int(limit)} Caller_Channel_Code, COUNT(*) AS Total FROM Separated_Info "
        "WHERE Caller_Channel_Code <> '-' GROUP BY Caller_Channel_Code ORDER BY Total DESC"
    )
    rows = cursor.fetchall()
    return [row.Caller_Channel_Code for row in rows], [row.Total for row in rows]
