# Call Center Analytics

Desktop tool (Tkinter) to import raw call-detail-record text files into SQL Server,
classify and enrich them, then filter, browse, chart, and export the results.

## Project layout

```
database/   config, DB connection, dropdown lookups
etl/        extract/transform/load pipeline (file import, classification, dedup)
reporting/  Excel export, pie charts
ui/         window, theme, frames, formatters
tests/      pytest unit tests for the pure-logic modules
main.py     entry point
```

## Setup

```
pip install -r requirements.txt
python main.py
```

An ODBC driver for SQL Server must be installed separately (this is a system-level
driver, not a Python package).

## Configuration

Connection settings are read from environment variables, with sensible local defaults:

| Variable               | Default     |
|-------------------------|-------------|
| `ANALYZER_DB_DRIVER`    | `SQL Server`|
| `ANALYZER_DB_SERVER`    | `.`         |
| `ANALYZER_DB_NAME`      | `Users`     |
| `ANALYZER_DB_USERNAME`  | *(unset)*   |
| `ANALYZER_DB_PASSWORD`  | *(unset)*   |

If username/password are unset, a trusted (Windows) connection is used.

## Tests

```
pip install pytest
pytest
```

The test suite covers only the pure-logic modules (number classification, datetime
splitting, query building) — nothing that touches a live database or the GUI.

## Known limitations

- The section/status constants in `constants.py` (`External`, `Brokerage`, `Box`,
  `Invalid`, `All`) are English, but a database that was populated by an earlier,
  Persian-language version of this app will still contain the old Persian values in
  `Dropdown_*`, `Unique_Info`, and `Separated_Info`. Filtering will not match existing
  rows until the database is migrated to the new values.
- The "Show Details" button stays disabled: there is no input field yet for the
  caller/called number that `reporting/charts.py` needs to draw its pie charts.
