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

## Database setup

The app expects a SQL Server database with the tables it reads from and writes to.
If you're starting from scratch (fresh SQL Server install, empty instance):

```
sqlcmd -S <server\instance> -i sql\schema.sql
```

This creates the `Users` database (if missing), `Unique_Info`, `Separated_Info`,
and the five `Dropdown_*` lookup tables, seeded with the section/status values the
app expects (`All`, `External`, `Brokerage`, `Box`, `Invalid`, plus the status
values). The channel-code dropdowns start with just `All`, since real channel codes
come from imported call data, not a fixed list — after your first import, run:

```
sqlcmd -S <server\instance> -i sql\refresh_channel_dropdowns.sql
```

to populate them from whatever codes actually showed up in `Separated_Info`.

## Data validation

Every row parsed from an imported `.txt` file is checked by `etl/record_validator.py`
before it reaches the database: field count, a plausible date/time, numeric caller
and called numbers, non-empty channels, duration-shaped ring/talk times, and a
non-empty status. Rows that fail are skipped (not inserted) and written to
`logs/rejected_rows.csv` with the line number and the reason, instead of silently
disappearing. The import summary in the status bar reports how many rows were
imported vs. rejected.

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
splitting, query building, record validation) — nothing that touches a live
database or the GUI.

## Known limitations

- The section/status constants in `constants.py` (`External`, `Brokerage`, `Box`,
  `Invalid`, `All`) are English, but a database that was populated by an earlier,
  Persian-language version of this app will still contain the old Persian values in
  `Dropdown_*`, `Unique_Info`, and `Separated_Info`. Filtering will not match existing
  rows until the database is migrated to the new values.
- The "Show Details" button stays disabled: there is no input field yet for the
  caller/called number that `reporting/charts.py` needs to draw its pie charts.
