# Call Center Analytics

A desktop tool that imports raw call-detail-record (CDR) text files into SQL
Server, classifies and enriches them, then lets you filter, browse, chart, and
export the results — a small, self-contained data engineering pipeline (extract
→ validate → transform → load → serve) wrapped in a Tkinter UI.

## Background

This project started life around 2020 as an internal tool for a call center: a
telephone switch would produce a raw CDR text file, and this app's job was to
load that file into SQL Server, derive a few useful fields from it (which
"section" a number belonged to, when a call happened, how long it lasted), and
let staff filter and browse the result. That's the shape of a small data
engineering job — extract, transform, load, serve — even though nobody involved
would necessarily have called it that at the time.

The application was written in Persian (both the UI text and a good part of the
code), built as a single monolithic Tkinter script, and never really finished:
several features existed in the code but didn't actually work. It sat untouched
for years. This document is a record of what was wrong with it and what it took
to bring it back into a working, professional, English-language state — kept
here so the reasoning behind the current structure isn't lost.

## The problem we inherited

Going through the original codebase surfaced a long list of issues, roughly in
four categories:

**Correctness bugs — features that looked like they worked but didn't:**
- Caller/called number classification relied on a `queue.Queue` that nothing
  ever populated. Calling that code path would have hung or produced empty
  results.
- The Excel export loop started at index 1 instead of 0, silently dropping the
  first row of every export.
- The code that inserted search results into the results table lived entirely
  inside a commented-out block. The active code path fetched data from the
  database and then did nothing with it.
- The "show call details" (per-number pie charts) feature was wired to a
  button that was permanently disabled, because no input field ever existed
  for the phone number it needed. The feature was unreachable.
- Column headers and Treeview sizing were recomputed from scratch on every
  single search, instead of once at startup.

**Security and robustness:**
- Every SQL query — search filters, dropdown population, per-number chart
  queries, the bulk insert during import — was built by concatenating strings,
  making the app vulnerable to SQL injection through user-entered filter text.
- The database connection was opened once, at import time, with no error
  handling. If SQL Server wasn't reachable, the app crashed on startup with a
  raw Python traceback instead of a usable message.
- There was no logging and no input validation. A malformed row in the source
  file either crashed the import or was silently skipped with no record of
  what was skipped or why.
- There were no automated tests of any kind.

**Structure and maintainability:**
- Everything lived in two folders (`Control`, `View`) with a mix of English
  and transliterated-Persian ("Finglish") identifiers and comments, and
  PascalCase variable names throughout — not idiomatic Python, and hard for
  a second person to pick up.
- Configuration (database server, driver, credentials) was hardcoded directly
  in source.
- The UI text was entirely in Persian, which was appropriate for its original
  users but made the codebase itself harder to work on for anyone not fluent
  in it, and coupled the display language to the source code.

**UI:**
- The window used fixed pixel coordinates (`.place(x=, y=)`) everywhere,
  wasn't resizable, and had no visual system — no consistent colors, spacing,
  or typography.
- "Reporting" — the one feature meant to turn raw call data into insight —
  was completely inert, for the reasons above.
- Exporting data meant exporting to Excel and nothing else: no way to keep a
  filtered view around inside the database itself, and no record of what
  filter had produced a given export.

## What we did about it

The rework happened in phases, each building on the last:

1. **Translate and rewrite.** Every identifier, UI label, comment, and message
   moved to English. The codebase was rewritten module-by-module in idiomatic
   Python (PEP 8 naming, small single-purpose functions), fixing the dead-code
   bugs above along the way: number classification now actually runs during
   the transform step, Excel export (later replaced — see below) stopped
   dropping the first row, and search results are now genuinely inserted into
   the results table.
2. **Make the queries safe.** Every SQL statement — search filters, dropdown
   population, inserts — was rewritten to use parameterized queries
   (`cursor.execute(sql, params)`) instead of string concatenation.
3. **Give it a real structure.** The code was split into focused packages by
   responsibility: `core` (shared constants/logging), `database` (connection
   and config), `etl` (the import/validate/transform/dedup pipeline),
   `reporting` (export and analytics), and `ui` (the Tkinter layer) — see
   *Project layout* below.
4. **Make failure survivable.** The database connection became lazy and
   wrapped in a clear `DatabaseConnectionError` instead of a bare `pyodbc`
   exception at import time. Every button click that touches the database is
   wrapped so a failure shows a message box and updates the status bar
   instead of crashing the app. Logging (rotating file + console) replaced
   the silence.
5. **Validate the data, don't just hope.** `etl/record_validator.py` checks
   every parsed row before it reaches the database — field count, a plausible
   date/time, numeric caller/called numbers, non-empty channels, duration-
   shaped ring/talk times, a non-empty status. Rejected rows are written to
   `logs/rejected_rows.csv` with the reason, instead of vanishing.
6. **Add tests.** A pytest suite now covers every pure-logic module: number
   classification, datetime splitting, query building, filter description,
   record validation, table-name sanitization.
7. **Redesign the UI.** A single theme module (`ui/theme.py`) defines the
   app's colors, fonts, and `ttk` styles. The old pixel-coordinate layout
   became a responsive grid (header, toolbar, filters sidebar, results table,
   status bar), and the window is resizable.
8. **Fix reporting for real.** The dead "show details" feature was replaced
   with a working Dashboard: five charts (see *Dashboard* below), computed
   with aggregate SQL queries and rendered with matplotlib embedded directly
   in the window, with a tab bar to switch between them and a clean empty
   state when there's no data yet.
9. **Turn "export" into a small data warehouse pattern.** "Export to Excel"
   became "Export to Table": the currently displayed rows (filtered or not)
   are saved into a SQL Server table, tracked through a shared
   `Export_Batches` metadata table that records *when* each export happened,
   *what filter* produced it, and *how many rows* — see *Export to Table*
   below. A small "Delete" control lets you clean up tables you created this
   way, with a confirmation prompt first.

The result is the same idea the 2020 version was reaching for — get data out
of a text file and into something people can filter, browse, and learn from —
but built the way that job is actually done: parameterized queries, validated
input, tracked lineage, tests, and a UI that doesn't fall over when the
database isn't there.

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
- The same dialog has a "Delete" button for removing a table you picked from
  the list — it asks for confirmation first, then drops the table and removes
  its rows from `Export_Batches`. This only works on tables already in the
  list (i.e. `Export_*` tables created this way); it can't target arbitrary
  tables by typing a name.

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

If there's no data in `Separated_Info` yet, the window shows a single "No data
yet" placeholder instead of five empty or misleading charts.

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
splitting, query building, filter description, record validation, table-name
sanitization) — nothing that touches a live database or the GUI.

## Known limitations

- The section/status constants in `core/constants.py` (`External`, `Brokerage`,
  `Box`, `Invalid`, `All`) are English, but a database that was populated by an
  earlier, Persian-language version of this app will still contain the old Persian
  values in `Dropdown_*`, `Unique_Info`, and `Separated_Info`. Filtering will not
  match existing rows until the database is migrated to the new values.
- `Separated_Info` is a single denormalized table, not a dimensional
  (fact/dimension) model. That's a reasonable next step if this ever needs to
  scale beyond one call center's worth of data, but it's a bigger change than
  anything above and hasn't been done here.
- The pipeline runs on demand (button click), not on a schedule or file-watch
  trigger. There's no orchestration layer (Airflow, cron, etc.) — this is a
  desktop tool, not a service.
