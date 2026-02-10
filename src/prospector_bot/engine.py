"""
================================================================================
CORE MODULE: MAIN ENGINE (SCRAPING LIFECYCLE)
================================================================================
FUNCTION:
Orchestrates the main asynchronous scraping loop, managing agent execution, 
rate limiting, and the Headless Browser (Playwright) lifecycle.

[BUSINESS & COMPLIANCE ALIGNMENT - ANDRE]
Platform Safety (Q1): Aggressive scraping triggers IP bans and violates the TOS 
of major marketplaces. 
Decision: A central Rate Limiter (`settings.interval_minutes`) was strictly 
enforced. By creating a polite pause between cycles, we stay under the radar 
of anti-bot systems, ensuring zero downtime for the MVP validation.

[PRODUCT & TECH LEAD - GABRIEL]
Infrastructure Cost (Q1): The MVP is hosted on an ultra-low-budget 1GB RAM VPS.
Architecture Solution: Playwright (Chromium) causes severe memory leaks if left 
open indefinitely. This engine is designed to explicitly launch and DESTROY 
the browser context at the end of each cycle. This "self-cleaning" architecture 
prevents "Zombie Processes" and guarantees the server never crashes from OOM 
(Out Of Memory).
================================================================================
"""
from __future__ import annotations

import datetime
import threading
import time

from .agents import AGENTS
from .filters import filter_by_city
from .i18n import select_locale, t
from .storage import load_seen_history, save_seen_history
from .telegram_handlers import safe_send
from .utils import timestamp


def run_scraper_loop(settings, state, bot) -> None:
    seen_history = load_seen_history(settings)

    print(f"[{timestamp()}] Prospector engine started.")

    while state.get("running", True):
        active_clients = _get_active_clients(state)

        if not active_clients:
            print(f"[{timestamp()}] No active clients. Waiting...")
            _sleep(settings.interval_minutes)
            continue

        requires_browser = _needs_browser(active_clients)
        playwright = None
        browser = None
        page = None

        if requires_browser:
            try:
                from playwright.sync_api import sync_playwright
            except Exception as exc:
                print(f"[{timestamp()}] Playwright not available: {exc}")
                requires_browser = False
            else:
                playwright = sync_playwright().start()
                try:
                    browser = playwright.chromium.launch_persistent_context(
                        user_data_dir=str(settings.session_dir),
                        headless=settings.headless,
                        channel=settings.browser_channel,
                        viewport=None,
                    )
                    page = browser.pages[0] if browser.pages else browser.new_page()
                except Exception as exc:
                    print(f"[{timestamp()}] Browser launch failed: {exc}")
                    requires_browser = False

        try:
            print(f"[{timestamp()}] Scanning for {len(active_clients)} clients...")

            for client in active_clients:
                chat_id = str(client.get("chat_id"))
                if chat_id not in seen_history:
                    seen_history[chat_id] = set()

                offers = []
                for agent in AGENTS:
                    if agent.requires_browser and not page:
                        continue
                    try:
                        offers += agent.handler(page, client, seen_history[chat_id])
                    except Exception as exc:
                        print(f"[{timestamp()}] Agent {agent.name} failed: {exc}")

                city_filter = client.get("strict_city") or client.get("target_city") or ""
                filtered = filter_by_city(offers, city_filter)

                _store_offers(state, chat_id, filtered)

                for offer in filtered:
                    locale = _client_locale(client, settings)
                    message = _format_offer_message(offer, locale)
                    if bot:
                        safe_send(bot, chat_id, message)
                    else:
                        print(f"[{timestamp()}] {message}")
                    offer_id = offer.get("id")
                    if offer_id:
                        seen_history[chat_id].add(offer_id)

                time.sleep(1)

            save_seen_history(settings, seen_history)

        except Exception as exc:
            print(f"[{timestamp()}] Cycle error: {exc}")
        finally:
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
            if playwright:
                try:
                    playwright.stop()
                except Exception:
                    pass

        _set_last_scan(state)
        print(f"[{timestamp()}] Waiting {settings.interval_minutes} minutes...")
        _sleep(settings.interval_minutes)


def _sleep(minutes: float) -> None:
    time.sleep(max(minutes, 0.1) * 60)


def _format_offer_message(offer: dict, locale: str) -> str:
    title = offer.get("title") or t(locale, "offer_default_title")
    price = offer.get("price_text", "")
    extra = offer.get("extra_info", "")
    link = offer.get("link", "")
    source = offer.get("source", "")

    lines = [
        t(locale, "offer_found"),
        t(locale, "offer_source", source=source),
        t(locale, "offer_title", title=title),
    ]
    if price:
        lines.append(t(locale, "offer_price", price=price))
    if extra:
        lines.append(t(locale, "offer_info", extra=extra))
    if link:
        lines.append(t(locale, "offer_link", link=link))
    return "\n".join(lines)


def _get_active_clients(state: dict) -> list[dict]:
    lock = _get_lock(state)
    with lock:
        clients = list(state.get("clients", []))
    return [c for c in clients if c.get("active")]


def _get_lock(state: dict) -> threading.Lock:
    lock = state.get("lock")
    if not hasattr(lock, "acquire"):
        lock = threading.Lock()
        state["lock"] = lock
    return lock


def _needs_browser(clients: list[dict]) -> bool:
    for client in clients:
        sources = client.get("sources", {})
        for agent in AGENTS:
            if agent.requires_browser and sources.get(agent.name, {}).get("active"):
                return True
    return False


def _store_offers(state: dict, chat_id: str, offers: list[dict]) -> None:
    if not offers:
        return
    lock = _get_lock(state)
    with lock:
        last_offers = state.setdefault("last_offers", {})
        existing = last_offers.get(chat_id, [])
        merged = (offers + existing)[:50]
        last_offers[chat_id] = merged


def _set_last_scan(state: dict) -> None:
    lock = _get_lock(state)
    with lock:
        state["last_scan_at"] = datetime.datetime.utcnow().isoformat() + "Z"


def _client_locale(client: dict, settings) -> str:
    preferred = client.get("locale") if isinstance(client, dict) else None
    return select_locale(preferred, None, getattr(settings, "default_locale", "en"))

