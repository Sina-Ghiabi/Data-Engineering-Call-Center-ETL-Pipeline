import constants
from etl.caller_number import resolve


def test_strips_42170_prefix():
    assert resolve("421701234") == (constants.SECTION_BROKERAGE, "1234")


def test_strips_2142170_prefix():
    assert resolve("2142170123") == (constants.SECTION_BOX, "123")


def test_strips_21_prefix():
    assert resolve("21987654321") == (constants.SECTION_EXTERNAL, "987654321")


def test_no_known_prefix_is_classified_as_is():
    assert resolve("999") == (constants.SECTION_BOX, "999")


def test_non_string_input_is_stringified_before_classifying():
    assert resolve(None) == (constants.SECTION_BROKERAGE, "None")
