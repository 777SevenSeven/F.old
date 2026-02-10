"""
================================================================================
COMMUNICATION CHANNEL: TELEGRAM HANDLER (MVP)
================================================================================
FUNCTION:
Acts as an asynchronous notification and command interface for GarimpoBot, 
connecting the user to the core AI Engine.

[PRODUCT STRATEGY ALIGNMENT - ANDRE (PM)]
UX Decision (Q1): Telegram was selected as the MVP channel specifically to test 
the 'Sniper' persona, leveraging native push-notifications for immediate alerts. 
Roadmap Q2: This is strictly a traction channel. The long-term interface is the 
fully responsive Web Application, where PRO Tier monetization and advanced 
dashboards are located.

[LEGAL & COMPLIANCE - ANDRE]
Data Policy: No sensitive user data or credentials must be stored in this layer. 
The handler strictly relays chat_ids and parameters to the AI Core, adhering 
to minimum-data-retention principles to mitigate data-breach risks during 
the MVP validation phase.
================================================================================
"""
from __future__ import annotations

from typing import Callable
import threading

from telebot import TeleBot

from .i18n import SUPPORTED_LOCALES, language_name, resolve_locale, select_locale, t
from .storage import create_client_from_request, save_preferences, upsert_client
from .utils import timestamp


def register_handlers(bot: TeleBot, state: dict, ai_client, settings) -> None:
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        chat_id = str(message.chat.id)
        name = getattr(message.from_user, "first_name", "there") or "there"
        text = message.text or ""

        lock = _get_lock(state)
        with lock:
            client = _find_client(state.get("clients", []), chat_id)

        locale = _resolve_locale(settings, state, message, chat_id, client)

        lowered = text.lower().strip()
        if lowered.startswith("/lang"):
            _handle_language_command(bot, message, settings, state, chat_id, client, locale, text)
            return

        if client:
            if lowered in {"/stop", "stop", "pause"}:
                _set_client_active(state, settings, client, False)
                _safe_reply(bot, message, t(locale, "paused"))
                return
            if lowered in {"/status", "status"}:
                _safe_reply(
                    bot,
                    message,
                    t(
                        locale,
                        "status",
                        search_term=client.get("search_term", ""),
                        target_city=client.get("target_city", ""),
                    ),
                )
                return
            if lowered in {"/resume", "resume", "start"}:
                _set_client_active(state, settings, client, True)
                _safe_reply(bot, message, t(locale, "resumed"))
                return

        bot.send_chat_action(chat_id, "typing")
        response_text, request_payload = ai_client.parse_message(text, locale)
        _safe_reply(bot, message, response_text)

        if request_payload:
            new_client = create_client_from_request(chat_id, name, request_payload, locale)
            lock = _get_lock(state)
            with lock:
                state["clients"] = upsert_client(state.get("clients", []), new_client)
                pending_locales = state.get("pending_locales", {})
                if chat_id in pending_locales:
                    pending_locales.pop(chat_id, None)
                save_preferences(settings, state["clients"])

            confirmation = t(
                locale,
                "config_confirmed",
                persona=new_client["persona"],
                search_term=new_client["search_term"],
                target_city=new_client["target_city"],
                price_max=new_client["price_max"],
            )
            safe_send(bot, chat_id, confirmation)


def _safe_reply(bot: TeleBot, message, text: str) -> None:
    try:
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception:
        try:
            bot.reply_to(message, text)
        except Exception:
            print(f"[{timestamp()}] Failed to reply to user.")


def safe_send(bot: TeleBot, chat_id: str, text: str) -> None:
    try:
        bot.send_message(chat_id, text, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception:
        try:
            bot.send_message(chat_id, text, disable_web_page_preview=True)
        except Exception:
            print(f"[{timestamp()}] Failed to send message to {chat_id}.")


def _find_client(clients: list[dict], chat_id: str) -> dict | None:
    for client in clients:
        if str(client.get("chat_id")) == str(chat_id):
            return client
    return None


def _set_client_active(state: dict, settings, client: dict, active: bool) -> None:
    lock = _get_lock(state)
    with lock:
        client["active"] = active
        save_preferences(settings, state.get("clients", []))


def _resolve_locale(settings, state: dict, message, chat_id: str, client: dict | None) -> str:
    pending = state.get("pending_locales", {}).get(chat_id)
    preferred = client.get("locale") if client else pending
    language_code = getattr(getattr(message, "from_user", None), "language_code", None)
    locale = select_locale(preferred, language_code, getattr(settings, "default_locale", "en"))

    if client is not None and client.get("locale") != locale:
        lock = _get_lock(state)
        with lock:
            client["locale"] = locale
            save_preferences(settings, state.get("clients", []))
    elif client is None and pending != locale:
        lock = _get_lock(state)
        with lock:
            pending_locales = state.setdefault("pending_locales", {})
            pending_locales[chat_id] = locale

    return locale


def _handle_language_command(
    bot: TeleBot,
    message,
    settings,
    state: dict,
    chat_id: str,
    client: dict | None,
    current_locale: str,
    text: str,
) -> None:
    parts = text.strip().split(maxsplit=1)
    if len(parts) == 1:
        locales = _format_locale_list()
        _safe_reply(bot, message, t(current_locale, "lang_prompt", locales=locales))
        return

    requested = parts[1].strip()
    normalized = resolve_locale(requested)
    if not normalized:
        locales = _format_locale_list()
        _safe_reply(bot, message, t(current_locale, "lang_unknown", locales=locales))
        return

    lock = _get_lock(state)
    with lock:
        if client is None:
            pending_locales = state.setdefault("pending_locales", {})
            pending_locales[chat_id] = normalized
        else:
            client["locale"] = normalized
            save_preferences(settings, state.get("clients", []))

    locale_name = language_name(normalized) or normalized
    _safe_reply(bot, message, t(normalized, "lang_updated", locale=locale_name))


def _format_locale_list() -> str:
    items = []
    for code in sorted(SUPPORTED_LOCALES):
        name = language_name(code)
        if name:
            items.append(f"{code} ({name})")
        else:
            items.append(code)
    return ", ".join(items)


def _get_lock(state: dict) -> threading.Lock:
    lock = state.get("lock")
    if not hasattr(lock, "acquire"):
        lock = threading.Lock()
        state["lock"] = lock
    return lock
