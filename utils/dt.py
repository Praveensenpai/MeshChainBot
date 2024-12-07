from datetime import datetime, timedelta
from typing import List


def iso_to_datetime(iso_timestamp: str) -> datetime:
    """Convert an ISO 8601 string with Z timezone to a datetime object."""
    return datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))


def human_readable(delta: timedelta) -> str:
    days: int = delta.days
    hours: int
    remainder: int
    minutes: int
    seconds: int
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts: List[str] = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)
