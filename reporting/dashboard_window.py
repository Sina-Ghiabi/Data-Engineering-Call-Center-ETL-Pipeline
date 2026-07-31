from tkinter import Toplevel

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # noqa: E402

from reporting import dashboard_data  # noqa: E402
from reporting.duration import from_seconds  # noqa: E402
from ui import theme  # noqa: E402


def _draw_pie(ax, labels, values, title) -> None:
    ax.set_title(title, fontsize=10, fontweight="bold")
    if not values:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.axis("off")
        return
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)


def _draw_bar(ax, labels, values, title, value_formatter=None) -> None:
    ax.set_title(title, fontsize=10, fontweight="bold")
    if not values:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.axis("off")
        return
    bars = ax.bar(labels, values, color=theme.COLOR_ACCENT)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    if value_formatter:
        for bar, value in zip(bars, values):
            ax.annotate(
                value_formatter(value),
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom", fontsize=8,
            )


def open_dashboard(parent) -> None:
    window = Toplevel(parent)
    window.title("Call Center Dashboard")
    window.geometry("1200x760")
    window.minsize(900, 600)

    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5))
    fig.subplots_adjust(hspace=0.55, wspace=0.4)

    _draw_pie(axes[0][0], *dashboard_data.status_breakdown(), "Call Status Breakdown")
    _draw_pie(axes[0][1], *dashboard_data.origin_mix(), "Call Origin Mix")
    _draw_bar(axes[0][2], *dashboard_data.monthly_call_volume(), "Call Volume by Month")

    labels, seconds = dashboard_data.average_talk_time_by_origin()
    _draw_bar(axes[1][0], labels, seconds, "Avg Talk Time by Origin", value_formatter=from_seconds)

    _draw_bar(axes[1][1], *dashboard_data.top_channels(), "Top 10 Busiest Channels")
    axes[1][2].axis("off")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
