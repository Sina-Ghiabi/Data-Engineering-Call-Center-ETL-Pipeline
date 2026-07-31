import keyboard


def format_timer_entry(entry):
    value = entry.get()
    if 1 <= len(value) < 2:
        entry.insert(1, ":")
    if keyboard.is_pressed("backspace"):
        entry.delete(len(entry.get()) - 1)
    entry.delete(3, "end")
