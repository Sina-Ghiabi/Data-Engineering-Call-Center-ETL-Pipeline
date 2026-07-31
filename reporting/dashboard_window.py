from tkinter import Toplevel, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from reporting import dashboard_data
from reporting.duration import from_seconds
from ui import theme

# Fixed entity -> color-slot order. Never re-sorted by value, so a given
# section keeps the same color across every chart it appears in.
ORIGIN_ORDER = ["External", "Brokerage", "Box", "Invalid", "Unknown"]

# Status colors are reserved for genuine call outcomes, not reused as a
# generic categorical series.
STATUS_COLORS = {
    "answered": theme.CHART_STATUS["good"],
    "busy": theme.CHART_STATUS["warning"],
    "No answer": theme.CHART_STATUS["serious"],
    "Failed": theme.CHART_STATUS["critical"],
}


def _origin_color(label: str, index: int) -> str:
    if label in ORIGIN_ORDER:
        return theme.CHART_CATEGORICAL[ORIGIN_ORDER.index(label)]
    return theme.CHART_CATEGORICAL[index % len(theme.CHART_CATEGORICAL)]


def _style_pie(ax, wedges, texts, autotexts, title) -> None:
    for text in texts:
        text.set_color(theme.CHART_INK)
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_color("#FFFFFF")
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")
    ax.set_title(title, fontsize=12, fontweight="bold", color=theme.CHART_INK, pad=14)


def _style_bar_axes(ax) -> None:
    ax.set_facecolor(theme.CHART_SURFACE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(theme.CHART_GRID)
    ax.spines["bottom"].set_color(theme.CHART_MUTED)
    ax.tick_params(colors=theme.CHART_MUTED, labelsize=9)
    ax.yaxis.grid(True, color=theme.CHART_GRID, linewidth=1)
    ax.set_axisbelow(True)


def _annotate_bars(ax, bars, values, formatter) -> None:
    for bar, value in zip(bars, values):
        ax.annotate(
            formatter(value),
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center", va="bottom", fontsize=8, color=theme.CHART_INK,
        )


def _draw_status_breakdown(ax) -> None:
    labels, values = dashboard_data.status_breakdown()
    colors = [STATUS_COLORS.get(label, theme.CHART_MUTED) for label in labels]
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90,
        wedgeprops={"edgecolor": theme.CHART_SURFACE, "linewidth": 2},
    )
    _style_pie(ax, wedges, texts, autotexts, "Call Status Breakdown")


def _draw_origin_mix(ax) -> None:
    labels, values = dashboard_data.origin_mix()
    colors = [_origin_color(label, index) for index, label in enumerate(labels)]
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90,
        wedgeprops={"edgecolor": theme.CHART_SURFACE, "linewidth": 2},
    )
    _style_pie(ax, wedges, texts, autotexts, "Call Origin Mix")


def _draw_monthly_volume(ax) -> None:
    labels, values = dashboard_data.monthly_call_volume()
    _style_bar_axes(ax)
    bars = ax.bar(labels, values, color=theme.CHART_CATEGORICAL[0], width=0.65,
                   edgecolor=theme.CHART_SURFACE, linewidth=1)
    ax.set_title("Call Volume by Month", fontsize=12, fontweight="bold", color=theme.CHART_INK, pad=14)
    ax.tick_params(axis="x", rotation=45)
    _annotate_bars(ax, bars, values, lambda value: str(int(value)))


def _draw_avg_talk_time(ax) -> None:
    labels, seconds = dashboard_data.average_talk_time_by_origin()
    _style_bar_axes(ax)
    colors = [_origin_color(label, index) for index, label in enumerate(labels)]
    bars = ax.bar(labels, seconds, color=colors, width=0.5, edgecolor=theme.CHART_SURFACE, linewidth=1)
    ax.set_title("Average Talk Time by Origin", fontsize=12, fontweight="bold", color=theme.CHART_INK, pad=14)
    ax.set_ylabel("Seconds", color=theme.CHART_MUTED, fontsize=9)
    _annotate_bars(ax, bars, seconds, from_seconds)


def _draw_top_channels(ax) -> None:
    labels, values = dashboard_data.top_channels()
    _style_bar_axes(ax)
    bars = ax.bar(labels, values, color=theme.CHART_CATEGORICAL[0], width=0.65,
                   edgecolor=theme.CHART_SURFACE, linewidth=1)
    ax.set_title("Top 10 Busiest Channels", fontsize=12, fontweight="bold", color=theme.CHART_INK, pad=14)
    ax.set_xlabel("Channel code", color=theme.CHART_MUTED, fontsize=9)
    _annotate_bars(ax, bars, values, lambda value: str(int(value)))


CHART_SPECS = (
    ("status", "Call Status", _draw_status_breakdown),
    ("origin", "Call Origin", _draw_origin_mix),
    ("volume", "Monthly Volume", _draw_monthly_volume),
    ("talktime", "Avg Talk Time", _draw_avg_talk_time),
    ("channels", "Top Channels", _draw_top_channels),
)


class Dashboard:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Call Center Dashboard")
        self.window.geometry("1100x700")
        self.window.minsize(820, 560)
        self.window.configure(background=theme.COLOR_BACKGROUND)
        self.buttons = {}
        self.figure = None
        self.ax = None
        self.canvas = None

        if dashboard_data.total_calls() == 0:
            self._build_empty_state()
            return

        self._build_selector_bar()
        self._build_chart_area()
        self.show_chart(CHART_SPECS[0][0])

    def _build_empty_state(self) -> None:
        wrapper = ttk.Frame(self.window, style="App.TFrame")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(wrapper, text="No data yet", style="CardSection.TLabel").pack()
        ttk.Label(
            wrapper, text="Import a call file first to see analytics here.", style="CardMuted.TLabel"
        ).pack(pady=(4, 0))

    def _build_selector_bar(self) -> None:
        bar = ttk.Frame(self.window, style="Toolbar.TFrame", padding=(theme.PAD, theme.PAD, theme.PAD, theme.PAD_SMALL))
        bar.pack(fill="x")

        for key, label, _draw in CHART_SPECS:
            button = ttk.Button(bar, text=label, style="Secondary.TButton", command=lambda k=key: self.show_chart(k))
            button.pack(side="left", padx=(0, theme.PAD_SMALL))
            self.buttons[key] = button

    def _build_chart_area(self) -> None:
        card = ttk.Frame(self.window, style="Card.TFrame", padding=theme.PAD)
        card.pack(fill="both", expand=True, padx=theme.PAD, pady=(0, theme.PAD))

        self.figure = Figure(figsize=(9, 6), dpi=100, facecolor=theme.CHART_SURFACE)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_chart(self, key: str) -> None:
        draw_by_key = {k: draw for k, _label, draw in CHART_SPECS}
        self.ax.clear()
        draw_by_key[key](self.ax)
        self.figure.tight_layout()
        self.canvas.draw()

        for button_key, button in self.buttons.items():
            button.configure(style="Accent.TButton" if button_key == key else "Secondary.TButton")


def open_dashboard(parent) -> None:
    Dashboard(parent)
