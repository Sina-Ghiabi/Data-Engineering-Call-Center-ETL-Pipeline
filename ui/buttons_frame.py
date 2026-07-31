import logging
from tkinter import filedialog, messagebox, ttk

import pyodbc

from database.db_connection import DatabaseConnectionError
from etl import insert_data, sort_data
from reporting import charts, export_excel
from ui import search_button, theme

logger = logging.getLogger(__name__)


def _run_safely(status_bar, action_label, action) -> None:
    try:
        action()
    except DatabaseConnectionError as error:
        logger.error("%s failed: %s", action_label, error)
        messagebox.showerror("Database Connection Failed", f"Could not connect to the database.\n\n{error}")
        status_bar.finish_progress(f"{action_label} failed: could not connect to the database.", kind="error")
    except pyodbc.Error as error:
        logger.exception("%s failed", action_label)
        messagebox.showerror("Database Error", str(error))
        status_bar.finish_progress(f"{action_label} failed.", kind="error")
    except Exception as error:
        logger.exception("%s failed", action_label)
        messagebox.showerror("Unexpected Error", str(error))
        status_bar.finish_progress(f"{action_label} failed.", kind="error")


def _import_file(tree, status_bar) -> None:
    path = filedialog.askopenfilename(title="Select a File", filetypes=(("Text files", "*.txt"),))
    if not path:
        return

    def action():
        tree.delete(*tree.get_children())

        status_bar.start_progress("Reading data...")
        insert_data.load_file(path, progress_callback=status_bar.update_progress)

        status_bar.start_progress("Processing data...")
        sort_data.transform(progress_callback=status_bar.update_progress)

        status_bar.finish_progress("Import completed successfully.")

    _run_safely(status_bar, "Import", action)


def _generate_report(tree, dropdown_selections, period_entries, status_bar) -> None:
    def action():
        search_button.search(tree, dropdown_selections, period_entries, status_bar)

    _run_safely(status_bar, "Report generation", action)


def _export(tree, status_bar) -> None:
    def action():
        export_excel.export(tree)
        status_bar.finish_progress(f"Exported to {export_excel.OUTPUT_FILE}")

    _run_safely(status_bar, "Export", action)


def build(window, tree, dropdown_selections, period_entries, status_bar) -> ttk.Frame:
    toolbar = ttk.Frame(window, style="Toolbar.TFrame", padding=(theme.PAD, 0, theme.PAD, theme.PAD_SMALL))
    toolbar.grid(row=1, column=0, columnspan=2, sticky="ew")

    ttk.Button(
        toolbar, text="Select File...", style="Secondary.TButton",
        command=lambda: _import_file(tree, status_bar),
    ).pack(side="left", padx=(0, theme.PAD_SMALL))

    ttk.Button(
        toolbar, text="Generate Report", style="Accent.TButton",
        command=lambda: _generate_report(tree, dropdown_selections, period_entries, status_bar),
    ).pack(side="left", padx=(0, theme.PAD_SMALL))

    ttk.Button(
        toolbar, text="Export to Excel", style="Secondary.TButton",
        command=lambda: _export(tree, status_bar),
    ).pack(side="left", padx=(0, theme.PAD_SMALL))

    # Disabled until the UI offers a way to pick a caller/called number to chart.
    ttk.Button(
        toolbar, text="Show Details", style="Secondary.TButton", state="disabled", command=charts.show_details
    ).pack(side="left")

    return toolbar
