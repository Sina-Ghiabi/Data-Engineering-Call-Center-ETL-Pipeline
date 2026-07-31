from tkinter import Button, Frame, filedialog

from etl import insert_data, sort_data
from reporting import charts, export_excel
from ui import search_button
from ui.progress_bar import ProgressBar


def _choose_file(window, tree):
    path = filedialog.askopenfilename(title="Select a File", filetypes=(("Text files", "*.txt"),))
    if not path:
        return

    tree.delete(*tree.get_children())

    reading_progress = ProgressBar(window, "Reading data...")
    reading_progress.create()
    insert_data.load_file(path, progress_callback=reading_progress.update)
    reading_progress.destroy()

    processing_progress = ProgressBar(window, "Processing data...")
    processing_progress.create()
    sort_data.transform(progress_callback=processing_progress.update)
    processing_progress.destroy()


def build(window, tree, dropdown_selections, period_entries):
    export_button = Button(window, text="Export to Excel", width=15, command=lambda: export_excel.export(tree))
    export_button.place(x=770, y=550)

    choose_file_button = Button(
        window, text="Select File...", width=15, command=lambda: _choose_file(window, tree)
    )
    choose_file_button.place(x=90, y=550)

    button_frame = Frame(window)
    button_frame.place(x=165, y=180)

    generate_report_button = Button(
        button_frame,
        text="Generate Report",
        width=15,
        padx=5,
        command=lambda: search_button.search(window, tree, dropdown_selections, period_entries),
    )
    generate_report_button.grid(row=0, column=0)

    # Disabled until the UI offers a way to pick a caller/called number to chart.
    show_details_button = Button(
        button_frame, text="Show Details", width=15, padx=5, state="disabled", command=charts.show_details
    )
    show_details_button.grid(row=1, column=0)

    return button_frame
