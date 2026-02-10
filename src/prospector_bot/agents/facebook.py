"""
================================================================================
DATA ADAPTER: FACEBOOK MARKETPLACE (DOM SCRAPER)
================================================================================
FUNCTION:
Acts as a translation layer (Driver) between the unstructured HTML of the site
and the standardized JSON format of GarimpoBot.

[LEGAL & FINANCE ALIGNMENT - ANDRE]
Risk Mitigation (Q1): Operating in 'Stateless' mode (No login/session). 
Decision: Avoids LGPD/GDPR liabilities regarding user data storage and eliminates 
the high OPEX (Operational Expenditure) of maintaining residential proxies 
needed to bypass Facebook's aggressive anti-scraping blocks for this MVP.

[PRODUCT & TECH LEAD - GABRIEL]
Architecture: DOM-based scraping (Headless Browser) is highly memory-intensive.
RAM Saver: Enforced a strict Early-Stop loop (SCRAPE_LIMIT = 5) to prevent 
the browser from causing OOM (Out-of-Memory) crashes on our 1GB MVP server.
================================================================================
"""
from __future__ import annotations
import re
from ..utils import parse_price

def scrape(page, client: dict, seen_ids: set[str]) -> list[dict]:
    # --- CONFIGURATION & RAM SAVER ---
    # Critical for 1GB RAM Servers: Limits the DOM objects in memory.
    SCRAPE_LIMIT = 5 
    # ---------------------------------

    source = client.get("sources", {}).get("facebook")
    if not source or not source.get("active"):
        return []

    url = source.get("url")
    if not url:
        return []

    print("      🟦 [FB] Accessing Marketplace...")

    try:
        page.goto(url)
        try:
            # Wait for the feed to load (max 8s to avoid zombie processes)
            page.wait_for_selector('a[href*="/marketplace/item/"]', timeout=8000)
        except Exception:
            return []

        cards = page.query_selector_all('a[href*="/marketplace/item/"]')
        results = []

        for card in cards:
            # [CRITICAL] RAM SAVER: Early Stop to prevent OOM (Out Of Memory)
            if len(results) >= SCRAPE_LIMIT:
                print(f"      🛑 [FB] Limit of {SCRAPE_LIMIT} items reached. Stopping.")
                break

            try:
                link_raw = card.get_attribute("href")
                if not link_raw:
                    continue

                # Regex is safer/cleaner than split (Tech Lead optimization)
                match = re.search(r"/marketplace/item/(\d+)", link_raw)
                item_id = match.group(1) if match else None
                
                if not item_id:
                    continue

                # Standardize ID key
                item_key = f"fb_{item_id}"
                
                # Deduplication Check
                if item_key in seen_ids:
                    continue

                text_full = card.inner_text() or ""

            except Exception:
                continue

            # [LOGIC RESTORED] City Target Filter
            # Prevents fetching items from other states/cities
            target_city = client.get("target_city", "")
            if target_city and target_city.lower() not in text_full.lower():
                continue

            # Negative Keywords Filter
            if any(neg in text_full.lower() for neg in client.get("negative_keywords", [])):
                continue

            # Parsing Logic
            lines = [line.strip() for line in text_full.split("\n") if line.strip()]
            price_str = "0"
            for line in lines:
                if any(char.isdigit() for char in line):
                    price_str = line
                    break

            price_val = parse_price(price_str)
            
            # Price Range Filter
            if price_val < client.get("price_min", 0) or price_val > client.get("price_max", 999999):
                continue

            info_extra = lines[-1] if lines else ""

            results.append(
                {
                    "source": "FACEBOOK",  # Standardized English Key
                    "id": item_key,
                    "title": lines[0] if lines else "Facebook Listing",
                    "price_text": price_str,
                    "extra_info": info_extra,
                    "link": f"https://facebook.com/marketplace/item/{item_id}/",
                }
            )

        return results

    except Exception as exc:
        print(f"      ⚠️ [FB] Error: {exc}")
        return []
