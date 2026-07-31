from tkinter import ttk

COLOR_BACKGROUND = "#F3F4F6"
COLOR_SURFACE = "#FFFFFF"
COLOR_BORDER = "#E2E5EA"
COLOR_HEADER = "#1F2937"
COLOR_HEADER_TEXT = "#F9FAFB"
COLOR_HEADER_SUBTEXT = "#9CA3AF"
COLOR_ACCENT = "#2563EB"
COLOR_ACCENT_HOVER = "#1D4ED8"
COLOR_ACCENT_TEXT = "#FFFFFF"
COLOR_TEXT_PRIMARY = "#111827"
COLOR_TEXT_SECONDARY = "#6B7280"
COLOR_SUCCESS = "#15803D"
COLOR_ERROR = "#B91C1C"
COLOR_ROW_ALT = "#F8FAFC"

FONT_FAMILY = "Segoe UI"
FONT_BASE = (FONT_FAMILY, 10)
FONT_BASE_BOLD = (FONT_FAMILY, 10, "bold")
FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 9)
FONT_SECTION = (FONT_FAMILY, 10, "bold")
FONT_TREE_HEADING = (FONT_FAMILY, 9, "bold")

PAD = 12
PAD_SMALL = 6


def apply(window) -> ttk.Style:
    window.configure(background=COLOR_BACKGROUND)

    style = ttk.Style(window)
    style.theme_use("clam")

    style.configure(".", font=FONT_BASE, background=COLOR_BACKGROUND, foreground=COLOR_TEXT_PRIMARY)

    style.configure("App.TFrame", background=COLOR_BACKGROUND)
    style.configure("Card.TFrame", background=COLOR_SURFACE, relief="flat", borderwidth=1)
    style.configure("Header.TFrame", background=COLOR_HEADER)
    style.configure("Toolbar.TFrame", background=COLOR_BACKGROUND)
    style.configure("StatusBar.TFrame", background=COLOR_SURFACE)

    style.configure("Card.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_PRIMARY, font=FONT_BASE)
    style.configure("CardSection.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_PRIMARY, font=FONT_SECTION)
    style.configure("CardMuted.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_SECONDARY, font=FONT_SUBTITLE)
    style.configure("HeaderTitle.TLabel", background=COLOR_HEADER, foreground=COLOR_HEADER_TEXT, font=FONT_TITLE)
    style.configure("HeaderSubtitle.TLabel", background=COLOR_HEADER, foreground=COLOR_HEADER_SUBTEXT, font=FONT_SUBTITLE)
    style.configure("Status.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_SECONDARY, font=FONT_BASE)
    style.configure("StatusSuccess.TLabel", background=COLOR_SURFACE, foreground=COLOR_SUCCESS, font=FONT_BASE_BOLD)
    style.configure("StatusError.TLabel", background=COLOR_SURFACE, foreground=COLOR_ERROR, font=FONT_BASE_BOLD)

    style.configure(
        "Accent.TButton",
        font=FONT_BASE_BOLD,
        foreground=COLOR_ACCENT_TEXT,
        background=COLOR_ACCENT,
        borderwidth=0,
        focuscolor=COLOR_ACCENT,
        padding=(14, 8),
    )
    style.map(
        "Accent.TButton",
        background=[("active", COLOR_ACCENT_HOVER), ("disabled", "#93A6C2")],
        foreground=[("disabled", "#E5E7EB")],
    )

    style.configure(
        "Secondary.TButton",
        font=FONT_BASE,
        foreground=COLOR_TEXT_PRIMARY,
        background=COLOR_SURFACE,
        borderwidth=1,
        relief="solid",
        padding=(14, 8),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLOR_ROW_ALT), ("disabled", COLOR_SURFACE)],
        foreground=[("disabled", "#C1C5CC")],
    )

    style.configure("TMenubutton", font=FONT_BASE, background=COLOR_SURFACE, relief="solid", borderwidth=1, padding=(8, 4))

    style.configure("TEntry", padding=(8, 6), relief="solid", borderwidth=1)

    style.configure(
        "Treeview",
        background=COLOR_SURFACE,
        fieldbackground=COLOR_SURFACE,
        foreground=COLOR_TEXT_PRIMARY,
        rowheight=26,
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        font=FONT_TREE_HEADING,
        background=COLOR_HEADER,
        foreground=COLOR_HEADER_TEXT,
        relief="flat",
        padding=(6, 6),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", COLOR_HEADER)],
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_ACCENT)],
        foreground=[("selected", COLOR_ACCENT_TEXT)],
    )

    style.configure("TProgressbar", background=COLOR_ACCENT, troughcolor=COLOR_BACKGROUND, borderwidth=0)

    return style
