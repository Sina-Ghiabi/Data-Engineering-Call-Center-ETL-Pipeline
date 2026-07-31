from etl.record_validator import validate

VALID_FIELDS = [
    "0", "1402/05/10 14:32:07", "912345678", "9:12345", "021123456",
    "9:67890", "0:15", "3:42", "answered", "note",
]


def test_valid_record_passes():
    assert validate(VALID_FIELDS) is None


def test_too_few_fields_is_rejected():
    assert validate(["0", "1402/05/10 14:32:07"]) is not None


def test_bad_date_and_time_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[1] = "not-a-date"
    assert validate(fields) is not None


def test_non_numeric_caller_number_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[2] = "abc"
    assert validate(fields) is not None


def test_non_numeric_called_number_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[4] = "abc"
    assert validate(fields) is not None


def test_empty_caller_channel_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[3] = ""
    assert validate(fields) is not None


def test_bad_ring_time_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[6] = "not-a-duration"
    assert validate(fields) is not None


def test_empty_status_is_rejected():
    fields = VALID_FIELDS.copy()
    fields[8] = ""
    assert validate(fields) is not None
