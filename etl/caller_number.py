from typing import Tuple

from core import constants
from etl.classify_number import classify_by_length


def resolve(number) -> Tuple[str, str]:
    text = str(number)
    try:
        if text.startswith("42170") and len(text) > 4:
            text = text[5:]
        elif text.startswith("2142170") and len(text) > 4:
            text = text[7:]
        elif text.startswith("21") and len(text) > 4:
            text = text[2:]
        return classify_by_length(text), text
    except Exception:
        return constants.SECTION_UNKNOWN, text
