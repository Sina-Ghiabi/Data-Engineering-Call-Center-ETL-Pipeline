import pytest

from reporting.export_table import InvalidTableNameError, full_table_name, sanitize_table_name


def test_sanitize_keeps_simple_names():
    assert sanitize_table_name("MonthlyReport") == "MonthlyReport"


def test_sanitize_replaces_invalid_characters():
    assert sanitize_table_name("My Report! 2026") == "My_Report_2026"


def test_sanitize_strips_leading_trailing_underscores():
    assert sanitize_table_name("  spaced out  ") == "spaced_out"


def test_sanitize_prefixes_names_starting_with_a_digit():
    assert sanitize_table_name("2026_calls") == "T_2026_calls"


def test_sanitize_rejects_empty_or_symbol_only_names():
    with pytest.raises(InvalidTableNameError):
        sanitize_table_name("   ")
    with pytest.raises(InvalidTableNameError):
        sanitize_table_name("!!!")


def test_full_table_name_adds_prefix():
    assert full_table_name("MonthlyReport") == "Export_MonthlyReport"
