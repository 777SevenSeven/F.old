"""Time helpers."""
from __future__ import annotations

import datetime


def timestamp() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

