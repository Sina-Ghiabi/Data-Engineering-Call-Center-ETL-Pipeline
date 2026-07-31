import buttons_frame
import dropdown_widget
import dropdowns_frame
import treeview_frame
from main_window import window
from period_frame import PeriodFrame


def main():
    dropdowns_frame.build(window)

    period_frame = PeriodFrame(window)
    period_frame.build()

    tree = treeview_frame.build(window)

    buttons_frame.build(window, tree, dropdown_widget.selections, period_frame.entries)

    window.mainloop()


if __name__ == "__main__":
    main()
