from ui import buttons_frame, dropdown_widget, dropdowns_frame, treeview_frame
from ui.main_window import window
from ui.period_frame import PeriodFrame


def main():
    dropdowns_frame.build(window)

    period_frame = PeriodFrame(window)
    period_frame.build()

    tree = treeview_frame.build(window)

    buttons_frame.build(window, tree, dropdown_widget.selections, period_frame.entries)

    window.mainloop()


if __name__ == "__main__":
    main()
