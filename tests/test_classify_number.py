import constants
from etl.classify_number import classify_by_length


def test_more_than_four_digits_is_external():
    assert classify_by_length("123456") == constants.SECTION_EXTERNAL


def test_four_digits_is_brokerage():
    assert classify_by_length("1234") == constants.SECTION_BROKERAGE


def test_three_digits_is_box():
    assert classify_by_length("123") == constants.SECTION_BOX


def test_fewer_than_three_digits_is_invalid():
    assert classify_by_length("12") == constants.SECTION_INVALID
    assert classify_by_length("") == constants.SECTION_INVALID
