"""Text helpers and normalization."""
from __future__ import annotations

import re
import unicodedata

try:
    import unidecode as _unidecode
except Exception:  # pragma: no cover - optional dependency
    _unidecode = None


def normalize_text(text: str) -> str:
    if not text:
        return ""
    try:
        nfkd = unicodedata.normalize("NFKD", str(text))
        no_accents = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return no_accents.lower().strip()
    except Exception:
        return str(text).lower().strip()


def to_slug(text: str) -> str:
    if not text:
        return ""
    raw = str(text).lower()
    if _unidecode:
        raw = _unidecode.unidecode(raw)
    else:
        raw = normalize_text(raw)
    slug = re.sub(r"[^a-z0-9\s-]", "", raw)
    slug = re.sub(r"\s+", "-", slug)
    return slug.strip("-")


def parse_price(text: str) -> float:
    if not text:
        return 0.0
    lower = str(text).lower()
    if "free" in lower or "gratis" in lower:
        return 0.0
    raw = str(text)
    if "," in raw and "." in raw:
        if raw.rfind(",") > raw.rfind("."):
            cleaned = raw.replace(".", "").replace(",", ".")
        else:
            cleaned = raw.replace(",", "")
    elif "," in raw and "." not in raw:
        parts = raw.split(",")
        if len(parts[-1]) == 3:
            cleaned = raw.replace(",", "")
        else:
            cleaned = raw.replace(",", ".")
    else:
        cleaned = raw
    cleaned = cleaned.replace(" ", "")
    numbers = re.sub(r"[^0-9.]", "", cleaned)
    if not numbers:
        return 0.0
    try:
        return float(numbers)
    except Exception:
        return 0.0


def extract_first_number(text: str) -> float | None:
    if not text:
        return None
    match = re.search(r"(\d+[\d.,]*)", str(text))
    if not match:
        return None
    return parse_price(match.group(1))


def remove_fragments(text: str, fragments: list[str]) -> str:
    if not text:
        return ""
    result = str(text)
    for fragment in fragments:
        if fragment:
            result = result.replace(fragment, " ")
    result = re.sub(r"\s+", " ", result)
    return result.strip()

