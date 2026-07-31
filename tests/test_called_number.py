from core import constants
from etl.called_number import resolve


def test_strips_leading_9_then_42170():
    assert resolve("9421701234") == (constants.SECTION_BROKERAGE, "1234")


def test_strips_leading_9_then_21():
    assert resolve("921987654") == (constants.SECTION_EXTERNAL, "987654")


def test_short_leading_9_number_is_not_stripped():
    assert resolve("9123") == (constants.SECTION_BROKERAGE, "9123")


def test_strips_42170_prefix_without_leading_9():
    assert resolve("421701234") == (constants.SECTION_BROKERAGE, "1234")


def test_strips_21_prefix_without_leading_9():
    assert resolve("21987654321") == (constants.SECTION_EXTERNAL, "987654321")


def test_no_known_prefix_is_classified_as_is():
    assert resolve("999") == (constants.SECTION_BOX, "999")
