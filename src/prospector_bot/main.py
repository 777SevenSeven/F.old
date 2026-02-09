"""Entry point for ProspectorBot."""
from __future__ import annotations

import argparse
import threading
import os

try:
    import telebot
except Exception:  # pragma: no cover - optional dependency
    telebot = None

from .ai_client import AIClient
from .engine import run_scraper_loop
from .settings import load_settings
from .storage import ensure_directories, load_preferences, migrate_legacy_paths
from .telegram_handlers import register_handlers
from .utils import timestamp


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    settings = load_settings()
    _apply_cli_overrides(settings, args)

    migrate_legacy_paths(settings)
    ensure_directories(settings)

    state = {
        "clients": load_preferences(settings),
        "running": True,
        "lock": threading.Lock(),
        "last_offers": {},
        "pending_locales": {},
    }

    ai_client = AIClient(settings.gemini_api_key)

    bot = None
    if args.mode in {"telegram", "both"}:
        bot = _setup_telegram(settings, state, ai_client)

    if _needs_login(settings):
        _manual_login(settings)

    if bot:
        thread = threading.Thread(target=bot.infinity_polling, daemon=True)
        thread.start()

    if args.mode == "telegram":
        run_scraper_loop(settings, state, bot)
        return

    engine_thread = threading.Thread(target=run_scraper_loop, args=(settings, state, bot), daemon=True)
    state["engine_thread"] = engine_thread
    engine_thread.start()

    if args.mode in {"api", "both"}:
        _run_api(settings, state, ai_client, bot)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ProspectorBot runner")
    parser.add_argument(
        "--mode",
        default=os.getenv("RUN_MODE", "telegram"),
        choices=("telegram", "api", "both"),
        help="Startup mode: telegram, api, or both.",
    )
    parser.add_argument("--api-host", default=None, help="API host override.")
    parser.add_argument("--api-port", type=int, default=None, help="API port override.")
    return parser.parse_args(argv)


def _apply_cli_overrides(settings, args: argparse.Namespace) -> None:
    if args.api_host:
        settings.api_host = args.api_host
    if args.api_port:
        settings.api_port = args.api_port


def _setup_telegram(settings, state, ai_client):
    if not telebot:
        print(f"[{timestamp()}] telebot is not installed. Telegram bot disabled.")
        return None
    if not settings.telegram_token:
        print(f"[{timestamp()}] TELEGRAM_TOKEN is missing. Telegram bot disabled.")
        return None

    try:
        bot = telebot.TeleBot(settings.telegram_token)
        register_handlers(bot, state, ai_client, settings)
        return bot
    except Exception as exc:
        print(f"[{timestamp()}] Failed to initialize Telegram bot: {exc}")
        return None


def _run_api(settings, state, ai_client, bot) -> None:
    try:
        import uvicorn
    except Exception as exc:
        print(f"[{timestamp()}] uvicorn not available: {exc}")
        return

    from .api.app import create_app

    app = create_app(state=state, settings=settings, ai_client=ai_client, bot=bot)
    uvicorn.run(app, host=settings.api_host, port=settings.api_port, log_level="info")


def _needs_login(settings) -> bool:
    return bool(settings.force_login)


def _manual_login(settings) -> None:
    print("=" * 60)
    print("MANUAL LOGIN MODE")
    print("A browser window will open. Log in, then press ENTER.")
    print("=" * 60)

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        print(f"[{timestamp()}] Playwright not available: {exc}")
        return

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(settings.session_dir),
            headless=False,
            channel=settings.browser_channel,
            args=["--start-maximized"],
            viewport=None,
        )
        try:
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("about:blank")
        except Exception:
            pass

        input("Press ENTER after login to continue...")
        try:
            browser.close()
        except Exception:
            pass

    print("Session saved. Starting engines...")


if __name__ == "__main__":
    main()

