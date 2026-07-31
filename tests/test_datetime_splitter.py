from etl.datetime_splitter import split


def test_splits_date_and_time():
    assert split("1402/05/10 14:32:07") == ("1402/05/10", "1402", "05", "10", "14:32:07")


def test_malformed_input_returns_none_placeholders():
    assert split("not-a-date") == ("None", "None", "None", "None", "None")


def test_non_string_input_returns_none_placeholders():
    assert split(None) == ("None", "None", "None", "None", "None")
