from reporting.duration import from_seconds, to_seconds


def test_to_seconds_parses_minutes_and_seconds():
    assert to_seconds("2:05") == 125


def test_to_seconds_returns_none_for_malformed_input():
    assert to_seconds("not-a-duration") is None
    assert to_seconds(None) is None


def test_from_seconds_formats_as_minutes_colon_seconds():
    assert from_seconds(125) == "2:05"
    assert from_seconds(59) == "0:59"


def test_round_trip():
    assert to_seconds(from_seconds(187)) == 187
