"""Lightweight RSS helpers."""
from __future__ import annotations

import html
import re
import urllib.request
import xml.etree.ElementTree as ET


def fetch_rss_items(url: str, timeout: int = 20, user_agent: str | None = None) -> list[dict]:
    if not url:
        return []

    headers = {"User-Agent": user_agent or "ProspectorBot/1.0"}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except Exception:
        return []

    try:
        root = ET.fromstring(raw)
    except Exception:
        return []

    items = []
    for item in root.findall(".//item"):
        title = _safe_text(item, "title")
        link = _safe_text(item, "link")
        guid = _safe_text(item, "guid")
        description = _strip_html(_safe_text(item, "description"))
        pub_date = _safe_text(item, "pubDate") or _safe_text(
            item, "{http://purl.org/dc/elements/1.1/}date"
        )
        items.append(
            {
                "title": title,
                "link": link,
                "guid": guid,
                "description": description,
                "pub_date": pub_date,
            }
        )

    return items


def _safe_text(node: ET.Element, tag: str) -> str:
    try:
        value = node.findtext(tag)
        return value.strip() if value else ""
    except Exception:
        return ""


def _strip_html(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()

