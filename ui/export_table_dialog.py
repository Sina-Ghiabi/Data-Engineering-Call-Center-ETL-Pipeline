from tkinter import StringVar, Toplevel, ttk
from typing import List, Optional

from ui import theme


def ask_table_name(parent, existing_names: List[str]) -> Optional[str]:
    dialog = Toplevel(parent)
    dialog.title("Export to Table")
    dialog.configure(background=theme.COLOR_SURFACE)
    dialog.resizable(False, False)
    dialog.transient(parent)

    result = {"name": None}

    container = ttk.Frame(dialog, style="Card.TFrame", padding=theme.PAD)
    container.pack(fill="both", expand=True)

    ttk.Label(
        container, text="Save the current view to which table?", style="CardSection.TLabel"
    ).pack(anchor="w")
    ttk.Label(
        container,
        text="Pick an existing table, or type a new name to create one.",
        style="CardMuted.TLabel",
    ).pack(anchor="w", pady=(0, theme.PAD_SMALL))

    variable = StringVar()
    combo = ttk.Combobox(container, textvariable=variable, values=existing_names, width=32)
    if existing_names:
        combo.set(existing_names[0])
    combo.pack(fill="x", pady=(0, theme.PAD))
    combo.focus_set()

    button_row = ttk.Frame(container, style="Card.TFrame")
    button_row.pack(fill="x")

    def on_export() -> None:
        result["name"] = variable.get().strip()
        dialog.destroy()

    def on_cancel() -> None:
        dialog.destroy()

    ttk.Button(button_row, text="Export", style="Accent.TButton", command=on_export).pack(
        side="right"
    )
    ttk.Button(button_row, text="Cancel", style="Secondary.TButton", command=on_cancel).pack(
        side="right", padx=(0, theme.PAD_SMALL)
    )

    dialog.bind("<Return>", lambda _event: on_export())
    dialog.bind("<Escape>", lambda _event: on_cancel())

    dialog.update_idletasks()
    dialog.grab_set()
    dialog.wait_window()

    return result["name"] or None
