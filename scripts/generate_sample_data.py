import random

OUTPUT_PATH = "sample_data/sample_calls.txt"
ROW_COUNT = 5000

STATUSES = ["answered", "busy", "No answer", "Failed"]
STATUS_WEIGHTS = [0.6, 0.15, 0.15, 0.1]

# Number "shapes" chosen to exercise every branch of etl/caller_number.py
# and etl/called_number.py (External / Brokerage / Box / Invalid).
CALLER_NUMBER_GENERATORS = [
    lambda: "21" + _digits(9),        # External after stripping "21"
    lambda: "42170" + _digits(4),     # Brokerage after stripping "42170"
    lambda: "2142170" + _digits(3),   # Box after stripping "2142170"
    lambda: _digits(3),               # Box as-is
    lambda: _digits(4),               # Brokerage as-is
    lambda: _digits(7),               # External as-is
]
CALLED_NUMBER_GENERATORS = CALLER_NUMBER_GENERATORS + [
    lambda: "9" + "21" + _digits(9),      # leading 9, then "21" stripped -> External
    lambda: "9" + "42170" + _digits(4),   # leading 9, then "42170" stripped -> Brokerage
]


def _digits(count):
    first = random.choice("123456789")
    rest = "".join(random.choice("0123456789") for _ in range(count - 1))
    return first + rest


def _channel(with_colon=True):
    code = random.randint(1, 40)
    number = random.randint(100, 999)
    return f"{code}:{number}" if with_colon else "-"


def _duration(max_minutes=5):
    minutes = random.randint(0, max_minutes)
    seconds = random.randint(0, 59)
    return f"{minutes}:{seconds:02d}"


def _date_and_time():
    year = 1402
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(7, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


def _details(status):
    if status == "Failed":
        return "network error"
    if status == "No answer":
        return "no pickup"
    return ""


def build_row(index):
    caller_number = random.choice(CALLER_NUMBER_GENERATORS)()
    called_number = random.choice(CALLED_NUMBER_GENERATORS)()
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

    fields = [
        str(index),
        _date_and_time(),
        caller_number,
        _channel(),
        called_number,
        _channel(with_colon=random.random() > 0.1),
        _duration(),
        _duration() if status == "answered" else "0:00",
        status,
        _details(status),
    ]
    return ",".join(fields)


def main():
    random.seed(42)
    lines = ["# index,date_and_time,caller_number,caller_channel,called_number,called_channel,ring_time,talk_time,status,details"]
    lines += [build_row(index) for index in range(1, ROW_COUNT + 1)]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")

    print(f"Wrote {ROW_COUNT} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
