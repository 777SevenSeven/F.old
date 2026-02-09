"""
================================================================================
DATA ADAPTER: CRAIGSLIST MARKETPLACE (RSS INTEGRATION)
================================================================================
FUNCTION:
Acts as a translation layer (Driver) between the Craigslist public RSS Feeds
and the standardized JSON format of GarimpoBot.

[LEGAL & COMPLIANCE ALIGNMENT - IASMIN]
Risk Mitigation (Q1): Craigslist explicitly restricts unauthorized web scraping.
Decision: To ensure 100% legal compliance during the MVP phase, this module 
operates STRICTLY via their public, authorized RSS XML feeds. 
It operates in 'Stateless' mode: No logins, no interaction, and zero data 
liability to prevent IP bans and comply with data protection regulations.

[PRODUCT & TECH LEAD - ANDR]
Performance & Strategy: RSS feeds are inherently lightweight (Low RAM footprint),
ideal for our 1GB server constraint. 
Business Logic: Implemented a strict 'City Target' filter to automatically 
reject sponsored nationwide ads that pollute the feed, ensuring the 'Sniper' 
persona only receives hyper-local opportunities.
================================================================================
"""
from __future__ import annotations

import re
import hashlib
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from ..utils import fetch_rss_items, parse_price
from ..utils.urls import build_craigslist_url


def scrape(page, client: dict, seen_ids: set[str]) -> list[dict]:
    # --- CONFIGURATION & RAM SAVER ---
    # Limits the number of processed XML objects to save memory footprint.
    SCRAPE_LIMIT = 5 
    # ---------------------------------

    source = client.get("sources", {}).get("craigslist")
    if not source or not source.get("active"):
        return []

    url = source.get("url") or ""
    if not url:
        url = build_craigslist_url(
            client.get("search_term", ""),
            client.get("price_min", 0),
            client.get("price_max", 999999),
            client.get("target_city", ""),
        )

    url = _ensure_rss_url(
        url,
        client.get("search_term", ""),
        client.get("price_min", 0),
        client.get("price_max", 999999),
    )

    print(f"       [CL] Reading RSS feed...")

    items = fetch_rss_items(url)
    results = []

    for item in items:
        # [CRITICAL] RAM SAVER: Early Stop to prevent memory overload
        if len(results) >= SCRAPE_LIMIT:
            print(f"       [CL] Limit of {SCRAPE_LIMIT} items reached. Stopping.")
            break

        title = item.get("title") or "Craigslist Listing"
        link = item.get("link") or ""
        guid = item.get("guid") or link
        item_id = _extract_item_id(guid) or _extract_item_id(link) or f"cl_{_stable_id(guid or link)}"
        
        # Deduplication Check
        if item_id in seen_ids:
            continue

        combined = f"{title} {item.get('description','')}".lower()

        # [LOGIC RESTORED] City Target Filter
        # Ensures items strictly match the user's local city, ignoring promoted nationwide ads.
        target_city = client.get("target_city", "")
        if target_city and target_city.lower() not in combined:
            continue

        # Negative Keywords Filter
        if any(neg in combined for neg in client.get("negative_keywords", [])):
            continue

        price_val = parse_price(title)
        if price_val <= 0:
            price_val = parse_price(item.get("description", ""))

        # Price Range Filter
        if price_val < client.get("price_min", 0) or price_val > client.get("price_max", 999999):
            continue

        results.append(
            {
                "source": "CRAIGSLIST",
                "id": item_id,
                "title": title,
                "price_text": f"$ {price_val:,.0f}" if price_val else "",
                "extra_info": item.get("description", ""),
                "region": target_city,
                "link": link,
            }
        )

    return results


def _ensure_rss_url(url: str, search_term: str, price_min: float, price_max: float) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "format" not in query:
        query["format"] = ["rss"]
    if "query" not in query and search_term:
        query["query"] = [search_term]
    if "min_price" not in query and price_min:
        query["min_price"] = [str(int(price_min))]
    if "max_price" not in query and price_max:
        query["max_price"] = [str(int(price_max))]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def _extract_item_id(text: str) -> str:
    if not text:
        return ""
    match = re.search(r"/(\d+)\.html", text)
    if match:
        return f"cl_{match.group(1)}"
    match = re.search(r"(\d{6,})", text)
    if match:
        return f"cl_{match.group(1)}"
    return ""


def _stable_id(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]

