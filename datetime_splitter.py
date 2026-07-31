def split(date_and_time):
    try:
        date_part, time_part = date_and_time.split(" ", 1)
        year, month, day = date_part.split("/")
        return date_part, year, month, day, time_part
    except (ValueError, AttributeError):
        return "None", "None", "None", "None", "None"
