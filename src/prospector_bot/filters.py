"""Offer filters."""
from __future__ import annotations

from .utils import normalize_text


def filter_by_city(offers: list[dict], city: str) -> list[dict]:
    if not city or len(city) < 3:
        return offers

    target = normalize_text(city)
    filtered = []
    for offer in offers:
        extra = offer.get("extra_info", "")
        region = offer.get("region", "")
        combined = f"{extra} {region}"
        if target in normalize_text(combined):
            filtered.append(offer)
    return filtered

