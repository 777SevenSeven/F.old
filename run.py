"""Convenience entry point for local runs."""
from __future__ import annotations

import sys
from pathlib import Path

root = Path(__file__).resolve().parent
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from prospector_bot.main import main

if __name__ == "__main__":
    main()

