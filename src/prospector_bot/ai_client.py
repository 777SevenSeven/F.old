"""
================================================================================
CORE MODULE: AI CLIENT & NLP PROCESSOR
================================================================================
FUNCTION:
Parses natural language input from users into structured JSON queries using 
the Gemini LLM, driving the parameters of the scraping engine.

[FINANCIAL & COMPLIANCE ALIGNMENT - IASMIN]
OPEX Control (Q1): DOM scraping incurs high server burn rates (RAM/CPU).
Monetization Decision: We abandoned feature-based pricing. Monetization is now 
strictly tied to SERVER EFFICIENCY. 
- VIP/Sponsors: Fund the server = Zero queue, instant scraping.
- Free Users: Rate-limited to prevent financial loss. 
- Boost Mode: Micro-transactions for users with urgent needs (legacy "Sniper" 
  behavior) who can't afford monthly plans but need temporary high-speed access.

[PRODUCT & TECH LEAD - ANDRE]
Feature Scope (MVP): Dropped the legacy "Persona" classification logic. It added 
useless token overhead and latency. 
Refactoring: The AI prompt was hyper-compressed to extract ONLY Product, Price, 
and City. This minimalist approach saves tokens and passes control to the Engine 
Layer, which handles user throttling based on their Subscription Tier.
================================================================================
"""
from __future__ import annotations

import json
import re
from typing import Any

from .i18n import language_name, t
from .utils import extract_first_number, remove_fragments

try:
    from google import genai as _genai
except Exception:  # pragma: no cover - optional dependency
    _genai = None

# [TECH NOTE] Hyper-compressed prompt. Persona logic removed. Focus: Extraction Speed.
SYSTEM_PROMPT = """
You are a parameter extractor.
Your only job is to extract: Product, Maximum Price, and City from the user text.
Do NOT chat. Do NOT explain. Output ONLY valid JSON.
{
  "status": "READY",
  "product": "...",
  "max_price": 0.0,
  "city": "..."
}
""".strip()


class AIClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._client = None
        if _genai and api_key:
            try:
                self._client = _genai.Client(api_key=api_key)
            except Exception:
                self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    def parse_message(self, message: str, locale: str | None = None) -> tuple[str, dict | None]:
        if not self.available:
            return self._fallback_response(message, locale)

        prompt = f"{SYSTEM_PROMPT}"
        locale_name = language_name(locale)
        if locale_name:
            prompt = f"{prompt}\n\nUser language: {locale_name}."
        prompt = f"{prompt}\n\nUser: {message}"
        try:
            response = self._client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            text = response.text or ""
        except Exception:
            return self._fallback_response(message, locale)

        reply_text, parsed = _extract_json_payload(text)
        normalized = _normalize_ai_payload(parsed)
        if normalized:
            return reply_text or t(locale, "ai_ready"), normalized
        return reply_text or t(locale, "ai_missing_fields"), None

    def _fallback_response(self, message: str, locale: str | None) -> tuple[str, dict | None]:
        request = _heuristic_parse(message)
        if request:
            return t(locale, "ai_fallback_starting"), request

        return (t(locale, "ai_fallback_prompt"), None)


def _extract_json_payload(text: str) -> tuple[str, dict | None]:
    if not text:
        return "", None

    if "```json" in text:
        parts = text.split("```json")
        reply = parts[0].strip()
        try:
            payload = parts[1].split("```")[0].strip()
            return reply, json.loads(payload)
        except Exception:
            return reply, None

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            return text.replace(match.group(0), "").strip(), json.loads(match.group(0))
        except Exception:
            return text.strip(), None

    return text.strip(), None


def _normalize_ai_payload(payload: dict | None) -> dict | None:
    if not payload or not isinstance(payload, dict):
        return None

    status = payload.get("status") or payload.get("STATUS") or ""
    status = str(status).upper().strip()
    if status and status != "READY":
        return None

    product = payload.get("product") or payload.get("produto") or payload.get("item")
    max_price = payload.get("max_price") or payload.get("preco") or payload.get("price")
    city = payload.get("city") or payload.get("cidade")

    if product is None or max_price is None or city is None:
        return None

    try:
        max_price = float(max_price)
    except Exception:
        max_price = 0.0

    if not product or not city:
        return None

    return {
        "product": str(product).strip(),
        "max_price": max_price,
        "city": str(city).strip(),
    }


def _heuristic_parse(message: str) -> dict | None:
    if not message:
        return None

    text = str(message).strip()
    price = extract_first_number(text)
    city = None

    lower = text.lower()
    if " in " in lower:
        city = text.split(" in ", 1)[1].strip()
    elif " em " in lower:
        city = text.split(" em ", 1)[1].strip()

    product = re.sub(r"\d+[\d.,]*", " ", text)
    if city:
        product = remove_fragments(product, [city])
    product = product.strip()

    if not product or price is None or not city:
        return None

    return {
        "product": product,
        "max_price": float(price),
        "city": city,
    }
