import keyboard


def format_time_entry(entry):
    value = entry.get()
    if 2 <= len(value) < 3:
        entry.insert(2, ":")
    if 5 <= len(value) < 6:
        entry.insert(5, ":")
    if keyboard.is_pressed("backspace"):
        entry.delete(len(entry.get()) - 1)
    entry.delete(7, "end")
