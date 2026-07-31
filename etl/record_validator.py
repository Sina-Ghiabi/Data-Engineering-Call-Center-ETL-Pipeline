import re
from typing import List, Optional

REQUIRED_FIELD_COUNT = 10

DATE_TIME_PATTERN = re.compile(r"^\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{2}:\d{2}$")
NUMBER_PATTERN = re.compile(r"^\d+$")
DURATION_PATTERN = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")


def validate(fields: List[str]) -> Optional[str]:
    """Return None if the parsed fields form a valid record, otherwise a reason string."""
    if len(fields) < REQUIRED_FIELD_COUNT:
        return f"expected at least {REQUIRED_FIELD_COUNT} comma-separated fields, got {len(fields)}"

    (
        date_and_time, caller_number, caller_channel, called_number,
        called_channel, ring_time, talk_time, status, _details,
    ) = fields[1:10]

    if not DATE_TIME_PATTERN.match(date_and_time):
        return f"invalid Date_And_Time: {date_and_time!r}"
    if not NUMBER_PATTERN.match(caller_number):
        return f"invalid Caller_Number: {caller_number!r}"
    if not NUMBER_PATTERN.match(called_number):
        return f"invalid Called_Number: {called_number!r}"
    if not caller_channel:
        return "Caller_Channel is empty"
    if not called_channel:
        return "Called_Channel is empty"
    if not DURATION_PATTERN.match(ring_time):
        return f"invalid Ring_Time: {ring_time!r}"
    if not DURATION_PATTERN.match(talk_time):
        return f"invalid Talk_Time: {talk_time!r}"
    if not status:
        return "Status is empty"

    return None
