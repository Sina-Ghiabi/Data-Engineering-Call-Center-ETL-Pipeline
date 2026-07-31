import keyboard


def format_date_entry(entry):
    value = entry.get()
    if 4 <= len(value) < 5:
        entry.insert(4, "/")
    if 7 <= len(value) < 8:
        entry.insert(7, "/")
    if keyboard.is_pressed("backspace"):
        entry.delete(len(entry.get()) - 1)
    if 9 <= len(entry.get()) < 10:
        entry.insert(9, "/")
    entry.delete(9, "end")
