from core import constants


def classify_by_length(number: str) -> str:
    length = len(number)
    if length > 4:
        return constants.SECTION_EXTERNAL
    if length == 4:
        return constants.SECTION_BROKERAGE
    if length == 3:
        return constants.SECTION_BOX
    return constants.SECTION_INVALID
