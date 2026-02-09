"""Generic RSS agent for low-friction sources."""
from __future__ import annotations

from urllib.parse import urlparse
import hashlib

from ..utils import fetch_rss_items, parse_price


def scrape(page, client: dict, seen_ids: set[str]) -> list[dict]:
    source = client.get("sources", {}).get("rss")
    if not source or not source.get("active"):
        return []

    urls = []
    if isinstance(source.get("urls"), list):
        urls.extend([str(url) for url in source.get("urls") if url])
    if source.get("url"):
        urls.append(source.get("url"))

    if not urls:
        return []

    results = []
    for url in urls:
        items = fetch_rss_items(url)
        if not items:
            continue
        domain = _domain_from_url(url)
        for item in items:
            link = item.get("link") or ""
            guid = item.get("guid") or link
            item_key = f"rss_{_stable_id(guid or link)}"
            if item_key in seen_ids:
                continue

            title = item.get("title") or "RSS Listing"
            description = item.get("description", "")
            combined = f"{title} {description}".lower()
            if any(neg in combined for neg in client.get("negative_keywords", [])):
                continue

            price_val = parse_price(title)
            if price_val <= 0:
                price_val = parse_price(description)

            if price_val < client.get("price_min", 0) or price_val > client.get("price_max", 999999):
                continue

            results.append(
                {
                    "source": f"RSS:{domain}" if domain else "RSS",
                    "id": item_key,
                    "title": title,
                    "price_text": f"{price_val:,.0f}" if price_val else "",
                    "extra_info": description,
                    "region": client.get("target_city", ""),
                    "link": link,
                }
            )

    return results


def _domain_from_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")
    except Exception:
        return ""


def _stable_id(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]

