"""Agent registry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .craigslist import scrape as scrape_craigslist
from .ebay import scrape as scrape_ebay
from .facebook import scrape as scrape_facebook
from .rss import scrape as scrape_rss


@dataclass(frozen=True)
class Agent:
    name: str
    handler: Callable
    requires_browser: bool = False


AGENTS = [
    Agent("craigslist", scrape_craigslist, False),
    Agent("ebay", scrape_ebay, False),
    Agent("rss", scrape_rss, False),
    Agent("facebook", scrape_facebook, True),
]

__all__ = ["AGENTS", "Agent"]

