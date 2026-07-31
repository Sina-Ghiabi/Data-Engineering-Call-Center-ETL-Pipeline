from core import constants
from ui.query_builder import build_search_query, describe_filters


def test_no_filters_returns_unfiltered_query():
    query, params = build_search_query({}, {})
    assert query == "SELECT * FROM Separated_Info"
    assert params == []


def test_select_all_label_is_not_treated_as_a_filter():
    query, params = build_search_query({"Status": constants.SELECT_ALL_LABEL}, {})
    assert query == "SELECT * FROM Separated_Info"
    assert params == []


def test_dropdown_filter_is_parameterized():
    query, params = build_search_query({"Status": "answered"}, {})
    assert query == "SELECT * FROM Separated_Info WHERE Status = ?"
    assert params == ["answered"]


def test_period_range_with_both_bounds():
    query, params = build_search_query({}, {"date": ("1402/01/01", "1402/06/01")})
    assert query == "SELECT * FROM Separated_Info WHERE ? <= Date AND Date <= ?"
    assert params == ["1402/01/01", "1402/06/01"]


def test_period_range_with_only_lower_bound():
    query, params = build_search_query({}, {"date": ("1402/01/01", "")})
    assert query == "SELECT * FROM Separated_Info WHERE ? <= Date"
    assert params == ["1402/01/01"]


def test_period_range_with_only_upper_bound():
    query, params = build_search_query({}, {"date": ("", "1402/06/01")})
    assert query == "SELECT * FROM Separated_Info WHERE Date <= ?"
    assert params == ["1402/06/01"]


def test_combines_dropdown_and_period_filters():
    query, params = build_search_query(
        {"Status": "answered"}, {"ring_time": ("0:05", "1:00")}
    )
    assert query == "SELECT * FROM Separated_Info WHERE Status = ? AND ? <= Ring_Time AND Ring_Time <= ?"
    assert params == ["answered", "0:05", "1:00"]


def test_describe_filters_with_no_filters():
    assert describe_filters({}, {}) == "No filter (all records)"


def test_describe_filters_ignores_select_all():
    assert describe_filters({"Status": constants.SELECT_ALL_LABEL}, {}) == "No filter (all records)"


def test_describe_filters_reports_dropdown_and_range():
    description = describe_filters(
        {"Status": "answered"}, {"date": ("1402/01/01", "1402/06/01")}
    )
    assert description == "Status = answered; 1402/01/01 <= Date <= 1402/06/01"
