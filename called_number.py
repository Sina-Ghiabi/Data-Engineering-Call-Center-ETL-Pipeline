import constants
from classify_number import classify_by_length


def resolve(number):
    text = str(number)
    try:
        if text.startswith("9") and len(text) > 4:
            text = text[1:]
            if text.startswith("42170"):
                text = text[5:]
            elif text.startswith("21") and len(text) > 4:
                text = text[2:]
        elif text.startswith("42170") and len(text) > 4:
            text = text[5:]
        elif text.startswith("21") and len(text) > 4:
            text = text[2:]
        return classify_by_length(text), text
    except Exception:
        return constants.SECTION_UNKNOWN, text
