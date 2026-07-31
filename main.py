import logging
from tkinter import messagebox

import pyodbc

import app_logging
from database.db_connection import DatabaseConnectionError
from ui import buttons_frame, dropdown_widget, header, theme, treeview_frame
from ui.filters_panel import FiltersPanel
from ui.main_window import window
from ui.status_bar import StatusBar

logger = logging.getLogger(__name__)


def main() -> None:
    app_logging.configure()

    header.build(window).grid(row=0, column=0, columnspan=2, sticky="ew")

    try:
        filters_panel = FiltersPanel(window)
        filters_panel.build().grid(row=2, column=0, sticky="ns", padx=theme.PAD, pady=(0, theme.PAD))
    except DatabaseConnectionError as error:
        logger.error("Startup failed: %s", error)
        messagebox.showerror("Database Connection Failed", f"Could not connect to the database.\n\n{error}")
        window.destroy()
        return
    except pyodbc.Error as error:
        logger.exception("Startup failed")
        messagebox.showerror("Database Error", str(error))
        window.destroy()
        return

    tree = treeview_frame.build(window)

    status_bar = StatusBar(window)
    status_bar.frame.grid(row=3, column=0, columnspan=2, sticky="ew")

    buttons_frame.build(window, tree, status_bar)
    filters_panel.add_filter_button(
        lambda: buttons_frame.generate_report(tree, dropdown_widget.selections, filters_panel.entries, status_bar)
    )

    window.mainloop()


if __name__ == "__main__":
    main()
