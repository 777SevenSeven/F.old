"""
================================================================================
CORE MODULE: PERSISTENCE & MIGRATION LAYER
================================================================================
FUNCTION:
Handles state persistence, schema normalization, and user preference storage.
Manages the transition from the legacy (PT-BR) prototype to the new 
internationalized (i18n) architecture.

[BUSINESS & FINANCE ALIGNMENT - ANDRE]
Decision (Q1): Zero-cost infrastructure for the MVP validation phase. 
By utilizing local JSON storage (pathlib) instead of cloud databases, we keep 
our "burn rate" (operational cost) at zero while validating the "Sniper" 
persona retention metrics.

[TECH DEBT & SCALABILITY - ANDRE]
Architecture: This module is strictly designed as an Abstraction Layer (Facade).
Currently implemented for flat files (JSON) for rapid deployment, but structured 
to be seamlessly swapped for a scalable Relational Database (SQL) post-hackathon 
without breaking the Core AI engine.
- Note: Legacy PT-BR file paths are automatically migrated to the Global (EN) standard.
================================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import shutil
import time

from .i18n import normalize_locale
from .settings import Settings
from .utils import (
    build_craigslist_url,
    build_ebay_url,
    build_facebook_url,
    build_mercado_livre_url,
    build_olx_url,
)


def ensure_directories(settings: Settings) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.session_dir.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        _backup_corrupt_file(path)
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=4, ensure_ascii=False)


def _backup_corrupt_file(path: Path) -> None:
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(path.suffix + f".bad_{timestamp}")
        shutil.move(str(path), str(backup_path))
    except Exception:
        return


def migrate_legacy_paths(settings: Settings) -> None:
    base_dir = settings.base_dir

    legacy_session = base_dir / "sessao_facebook"
    if legacy_session.exists() and not settings.session_dir.exists():
        shutil.move(str(legacy_session), str(settings.session_dir))

    legacy_history = base_dir / "historico_vistos.json"
    if legacy_history.exists() and not settings.history_path.exists():
        shutil.move(str(legacy_history), str(settings.history_path))

    legacy_prefs = base_dir / "preferencias_usuario.json"
    if legacy_prefs.exists() and not settings.preferences_path.exists():
        shutil.move(str(legacy_prefs), str(settings.preferences_path))

    legacy_icon = base_dir / "icone.ico"
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    icon_path = assets_dir / "icon.ico"
    if legacy_icon.exists() and not icon_path.exists():
        shutil.move(str(legacy_icon), str(icon_path))


def _normalize_source_config(source: dict, search_term: str, price_min: float, price_max: float, city: str) -> dict:
    if not isinstance(source, dict):
        source = {}

    active = source.get("active")
    if active is None:
        active = source.get("ativo")
    if active is None:
        active = True

    url = source.get("url") or source.get("link") or ""
    normalized = {"active": bool(active)}
    for key, value in source.items():
        if key in {"active", "ativo"}:
            continue
        normalized[key] = value

    normalized.setdefault("url", url or "")
    return normalized


def _ensure_source_urls(sources: dict, search_term: str, price_min: float, price_max: float, city: str) -> dict:
    normalized = {}
    sources = sources if isinstance(sources, dict) else {}

    source_map = {
        "craigslist": ["craigslist", "cl"],
        "ebay": ["ebay", "e-bay"],
        "olx": ["olx"],
        "mercado_livre": ["mercado_livre", "mercadolivre", "ml"],
        "facebook": ["facebook", "fb", "face"],
        "rss": ["rss", "feed", "feeds"],
    }

    for key, aliases in source_map.items():
        cfg = {}
        for alias in aliases:
            if alias in sources:
                cfg = sources.get(alias, {}) or {}
                break
        normalized_cfg = _normalize_source_config(cfg, search_term, price_min, price_max, city)
        auto_url = normalized_cfg.get("auto_url")
        if auto_url is None:
            auto_url = normalized_cfg.get("auto")
        auto_url = True if auto_url is None else bool(auto_url)

        if key == "craigslist" and auto_url:
            normalized_cfg["url"] = build_craigslist_url(
                search_term, price_min, price_max, city, normalized_cfg.get("url")
            )
        elif key == "ebay" and auto_url:
            normalized_cfg["url"] = build_ebay_url(search_term, price_min, price_max)
        elif key == "olx" and auto_url:
            normalized_cfg["url"] = build_olx_url(search_term, price_min, price_max, city, normalized_cfg.get("url"))
        elif key == "mercado_livre" and auto_url:
            normalized_cfg["url"] = build_mercado_livre_url(
                search_term, price_min, price_max, city, normalized_cfg.get("url")
            )
        elif key == "facebook" and auto_url:
            normalized_cfg["url"] = build_facebook_url(
                search_term, price_min, price_max, city, normalized_cfg.get("url")
            )
        elif key == "rss":
            if not normalized_cfg.get("url") and not normalized_cfg.get("urls"):
                normalized_cfg["active"] = False
                normalized_cfg.setdefault("url", "")
        normalized[key] = normalized_cfg
    return normalized


def normalize_client(raw: dict) -> dict:
    name = raw.get("name") or raw.get("nome") or "Unknown"
    chat_id = raw.get("chat_id") or raw.get("chatId") or ""
    active = raw.get("active")
    if active is None:
        active = raw.get("ativo", True)

    search_term = raw.get("search_term") or raw.get("term") or raw.get("termo_busca") or raw.get("termo") or ""
    price_min = raw.get("price_min") or raw.get("preco_min") or 0
    price_max = raw.get("price_max") or raw.get("preco_max") or raw.get("preco") or 999999

    target_city = raw.get("target_city") or raw.get("cidade_alvo") or raw.get("cidade") or ""
    strict_city = raw.get("strict_city") or raw.get("cidade_filtro") or target_city
    persona = raw.get("persona") or raw.get("profile") or "SNIPER"
    locale = raw.get("locale") or raw.get("language") or raw.get("lang") or ""
    if locale:
        locale = normalize_locale(locale, "en")

    negative_keywords = raw.get("negative_keywords") or raw.get("palavras_negativas") or []

    sources_raw = raw.get("sources") or raw.get("fontes") or {}
    sources = _ensure_source_urls(sources_raw, search_term, price_min, price_max, target_city)

    return {
        "chat_id": str(chat_id),
        "name": name,
        "active": bool(active),
        "search_term": search_term,
        "price_min": _to_float(price_min, 0.0),
        "price_max": _to_float(price_max, 999999.0),
        "target_city": target_city,
        "strict_city": strict_city,
        "persona": persona,
        "negative_keywords": list(negative_keywords) if isinstance(negative_keywords, list) else [],
        "sources": sources,
        "locale": locale,
    }


def _to_float(value, default: float) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def merge_client(existing: dict, update: dict) -> dict:
    merged = {**existing, **update}
    if not update.get("negative_keywords"):
        merged["negative_keywords"] = existing.get("negative_keywords", [])
    if not update.get("sources"):
        merged["sources"] = existing.get("sources", {})
    return merged


def upsert_client(clients: list[dict], new_client: dict) -> list[dict]:
    updated = False
    for idx, client in enumerate(clients):
        if client.get("chat_id") == new_client.get("chat_id"):
            clients[idx] = merge_client(client, new_client)
            updated = True
            break
    if not updated:
        clients.append(new_client)
    return clients


def load_preferences(settings: Settings) -> list[dict]:
    ensure_directories(settings)
    raw = read_json(settings.preferences_path, default=[])
    if not isinstance(raw, list):
        raw = []
    normalized = [normalize_client(item) for item in raw if isinstance(item, dict)]
    return normalized


def save_preferences(settings: Settings, clients: list[dict]) -> None:
    normalized = [normalize_client(client) for client in clients]
    write_json(settings.preferences_path, normalized)


def load_seen_history(settings: Settings) -> dict[str, set[str]]:
    ensure_directories(settings)
    raw = read_json(settings.history_path, default={})
    if not isinstance(raw, dict):
        return {}
    return {str(key): set(value) for key, value in raw.items() if isinstance(value, list)}


def save_seen_history(settings: Settings, seen_history: dict[str, set[str]]) -> None:
    serializable = {key: list(value) for key, value in seen_history.items()}
    write_json(settings.history_path, serializable)


def create_client_from_request(chat_id: str, name: str, request: dict, locale: str | None = None) -> dict:
    search_term = request.get("product", "")
    price_max = request.get("max_price", 0)
    target_city = request.get("city", "")
    persona = request.get("persona", "SNIPER")

    raw = {
        "chat_id": str(chat_id),
        "name": name,
        "active": True,
        "search_term": search_term,
        "price_min": 0,
        "price_max": price_max,
        "target_city": target_city,
        "strict_city": target_city,
        "persona": persona,
        "negative_keywords": [],
        "sources": {},
        "locale": locale or "",
    }
    return normalize_client(raw)
