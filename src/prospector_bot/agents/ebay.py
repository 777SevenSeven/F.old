"""
================================================================================
DATA ADAPTER: EBAY MARKETPLACE (API INTEGRATION)
================================================================================
FUNCTION:
Acts as a translation layer (Driver) between the eBay Finding API
and the standardized JSON format of GarimpoBot.

[BUSINESS & COMPLIANCE ALIGNMENT - IASMIN]
Risk Mitigation (Q1): Direct web scraping on eBay carries a high risk of IP 
blacklisting and violates their aggressive anti-scraping TOS. 
Decision: This module strictly utilizes the official eBay Developer API. 
It operates statelessly (no user credentials stored), and respects native API 
Rate Limiting to ensure 100% legal compliance for our MVP.

[PRODUCT & TECH LEAD - ANDR]
Architecture: Currently utilizing the legacy eBay Finding API v1 for speed of 
deployment. 
RAM Saver: Implemented a strict memory ceiling (SCRAPE_LIMIT = 5) per query 
to prevent JSON payload overflow on our 1GB MVP server.
Roadmap Q2: Migrate to the newer OAuth-based eBay Browse API to unlock 
advanced condition filtering (e.g., 'For Parts/Not Working' for technicians).
================================================================================
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

from ..utils import parse_price

FINDING_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"


def scrape(page, client: dict, seen_ids: set[str]) -> list[dict]:
    # --- CONFIGURATION & RAM SAVER ---
    # Limits the number of processed JSON objects to save memory footprint.
    SCRAPE_LIMIT = 5 
    # ---------------------------------

    source = client.get("sources", {}).get("ebay")
    if not source or not source.get("active"):
        return []

    app_id = source.get("app_id") or os.getenv("EBAY_APP_ID") or ""
    if not app_id:
        print("       [EBAY] Missing EBAY_APP_ID. Skipping.")
        return []

    keywords = source.get("keywords") or client.get("search_term", "")
    if not keywords:
        return []

    global_id = source.get("global_id") or os.getenv("EBAY_GLOBAL_ID") or "EBAY-US"
    currency = source.get("currency") or os.getenv("EBAY_CURRENCY") or "USD"

    url = _build_request_url(
        keywords,
        app_id,
        global_id,
        currency,
        client.get("price_min", 0),
        client.get("price_max", 999999),
    )

    print("       [EBAY] Querying API...")

    payload = _fetch_json(url)
    if not payload:
        return []

    items = _extract_items(payload)
    results = []

    for item in items:
        # [CRITICAL] RAM SAVER: Early Stop to prevent memory overload
        if len(results) >= SCRAPE_LIMIT:
            print(f"       [EBAY] Limit of {SCRAPE_LIMIT} items reached. Stopping.")
            break

        item_id = item.get("itemId")
        if not item_id:
            continue
        
        item_key = f"ebay_{item_id}"
        
        # Deduplication Check
        if item_key in seen_ids:
            continue

        title = item.get("title") or "eBay Listing"
        location = item.get("location", "")

        # [LOGIC RESTORED] City Target Filter
        # Prevents fetching items from unwanted regions
        target_city = client.get("target_city", "")
        if target_city and target_city.lower() not in location.lower():
            continue

        # Negative Keywords Filter
        if any(neg in title.lower() for neg in client.get("negative_keywords", [])):
            continue

        price_val = parse_price(item.get("price", ""))
        if price_val < client.get("price_min", 0) or price_val > client.get("price_max", 999999):
            continue

        results.append(
            {
                "source": "EBAY",
                "id": item_key,
                "title": title,
                "price_text": item.get("price", ""),
                "extra_info": location,
                "region": location,
                "link": item.get("link", ""),
            }
        )

    return results


def _build_request_url(
    keywords: str,
    app_id: str,
    global_id: str,
    currency: str,
    price_min: float,
    price_max: float,
) -> str:
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": app_id,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "true",
        "GLOBAL-ID": global_id,
        "keywords": keywords,
        # Fetching a larger pool (20) to ensure we find 5 good matches after filters
        "paginationInput.entriesPerPage": "20", 
    }

    filters = []
    if price_min:
        filters.append(_make_filter("MinPrice", price_min, currency))
    if price_max and price_max < 999999:
        filters.append(_make_filter("MaxPrice", price_max, currency))

    for idx, filter_params in enumerate(filters):
        for key, value in filter_params.items():
            params[f"itemFilter({idx}).{key}"] = value

    return f"{FINDING_ENDPOINT}?{urllib.parse.urlencode(params)}"


def _make_filter(name: str, value: float, currency: str) -> dict:
    return {
        "name": name,
        "value": str(value),
        "paramName": "Currency",
        "paramValue": currency,
    }


def _fetch_json(url: str) -> dict | None:
    headers = {"User-Agent": "ProspectorBot/1.0"}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read()
    except Exception:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


def _extract_items(payload: dict) -> list[dict]:
    root = payload.get("findItemsByKeywordsResponse")
    if not root:
        return []
    block = root[0] if isinstance(root, list) and root else {}
    search = block.get("searchResult")
    if not search:
        return []
    results = search[0] if isinstance(search, list) and search else {}
    items = results.get("item") or []
    parsed = []
    for item in items:
        try:
            item_id = _first(item.get("itemId"))
            title = _first(item.get("title"))
            link = _first(item.get("viewItemURL"))
            location = _first(item.get("location"))
            price = ""
            selling = item.get("sellingStatus")
            if selling and isinstance(selling, list):
                current = selling[0].get("currentPrice") if selling else None
                if current and isinstance(current, list):
                    value = current[0].get("__value__")
                    currency = current[0].get("@currencyId", "")
                    if value:
                        price = f"{currency} {value}" if currency else str(value)
            parsed.append(
                {
                    "itemId": item_id,
                    "title": title,
                    "link": link,
                    "location": location,
                    "price": price,
                }
            )
        except Exception:
            continue
    return parsed


def _first(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""

