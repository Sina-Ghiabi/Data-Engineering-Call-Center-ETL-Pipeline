from typing import Optional


def to_seconds(text: str) -> Optional[int]:
    try:
        minutes, seconds = text.split(":")
        return int(minutes) * 60 + int(seconds)
    except (ValueError, AttributeError):
        return None


def from_seconds(seconds: float) -> str:
    total = int(round(seconds))
    return f"{total // 60}:{total % 60:02d}"
