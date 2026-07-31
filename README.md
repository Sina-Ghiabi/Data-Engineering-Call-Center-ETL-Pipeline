# Call Center Analytics

Desktop tool (Tkinter) to import raw call-detail-record text files into SQL Server,
classify and enrich them, then filter, browse, chart, and export the results.

## Project layout

```
core/         shared constants and logging setup — no dependency on any other package
database/     config, DB connection, dropdown lookups
etl/          extract/transform/load pipeline (file import, validation, classification, dedup)
reporting/    export-to-table (batch-tracked), the analytics dashboard (aggregate queries + charts)
ui/           window, theme, frames, formatters
tests/        pytest unit tests for the pure-logic modules
scripts/      one-off developer scripts (e.g. sample data generation)
sql/          schema and seed scripts, run with sqlcmd
sample_data/  a ready-to-import sample call file for manual testing
logs/         rotating app log + rejected_rows.csv (created at runtime, not tracked in git)
main.py       entry point
```

`core` has no imports from `database`/`etl`/`reporting`/`ui`, so it can be imported
from anywhere without pulling in tkinter, pyodbc, or matplotlib.

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

## Export to Table

The "Export to Table" button saves whatever is currently in the results table
(filtered or not) into a SQL Server table you pick or create — a small
batch/lineage-tracking pattern instead of a plain data dump:

- A dialog lists existing export tables (anything already created this way) in a
  combobox you can also type a new name into. Table names are sanitized (letters,
  digits, underscores only) and always created under the `Export_` prefix, e.g.
  choosing "MonthlyReport" creates/reuses `Export_MonthlyReport` — this keeps
  every export discoverable via `SELECT name FROM sys.tables WHERE name LIKE
  'Export_%'` and out of the way of the app's own tables.
- Every export also inserts one row into a shared `Export_Batches` table
  (`BatchID`, `TableName`, `ExportedAt`, `FilterCriteria`, `RecordCount`), and every
  row written to the target table carries that `ExportBatchID` as a foreign key.
  `FilterCriteria` records whatever was actually applied (e.g. `Status =
  answered; 1402/01/01 <= Date <= 1402/06/01`, or `No filter (all records)`),
  computed in `ui/query_builder.describe_filters` from the same inputs that
  built the query — so every export is traceable back to *when* it was made,
  *what was in it*, and *what filter produced it*, without needing to remember
  or re-derive that later.
- Exporting an empty results table is rejected with a status-bar message rather
  than silently creating an empty table.

## Dashboard

The "Dashboard" button opens a window with five charts computed straight from
`Separated_Info` (`reporting/dashboard_data.py` runs one aggregate SQL query per
chart; `reporting/dashboard_window.py` renders them with matplotlib embedded in
the window, not separate popups):

1. **Call Status Breakdown** — answered / busy / no-answer / failed, as a share of all calls.
2. **Call Origin Mix** — External / Brokerage / Box, by caller section.
3. **Call Volume by Month** — call counts per Year-Month, for spotting trends.
4. **Average Talk Time by Origin** — mean handle time (answered calls only), a core efficiency metric.
5. **Top 10 Busiest Channels** — which trunks/channels carry the most traffic.

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

- The section/status constants in `core/constants.py` (`External`, `Brokerage`,
  `Box`, `Invalid`, `All`) are English, but a database that was populated by an
  earlier, Persian-language version of this app will still contain the old Persian
  values in `Dropdown_*`, `Unique_Info`, and `Separated_Info`. Filtering will not
  match existing rows until the database is migrated to the new values.
