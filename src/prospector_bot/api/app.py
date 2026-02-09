"""REST API for GarimpoBot (FastAPI)."""
from __future__ import annotations

import threading
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..ai_client import AIClient
from ..engine import run_scraper_loop
from ..settings import load_settings
from ..storage import normalize_client, save_preferences, upsert_client


class ParseRequest(BaseModel):
    message: str
    locale: str | None = None


class ClientPayload(BaseModel):
    chat_id: str | None = None
    name: str | None = None
    active: bool | None = None
    search_term: str | None = None
    price_min: float | None = None
    price_max: float | None = None
    target_city: str | None = None
    strict_city: str | None = None
    persona: str | None = None
    negative_keywords: list[str] | None = None
    sources: dict | None = None

    class Config:
        extra = "allow"



class PreferencePayload(BaseModel):
    chat_id: str | None = None
    produto: str | None = None
    cidade_alvo: str | None = None
    preco_min: float | None = None
    preco_max: float | None = None
    palavras_negativas: list[str] | None = None
    facebook_ativo: bool | None = None
    facebook_url: str | None = None
    mercadolivre_ativo: bool | None = None
    mercadolivre_url: str | None = None
    olx_ativo: bool | None = None
    olx_url: str | None = None
    fontes: dict | None = None

    class Config:
        extra = "allow"


MOCK_DATA = {
    "iphone": [
        {
            "title": "iPhone 12 64GB Black",
            "price": "R$ 1.899",
            "marketplace": "FACEBOOK",
            "badge": "Low price",
            "imageUrl": "https://images.unsplash.com/photo-1603899123140-b7b6be6c4585?w=600",
            "link": "https://facebook.com/marketplace/iphone12-64gb-Black",
        },
        {
            "title": "iPhone 12 128GB Green",
            "price": "R$ 2.080",
            "marketplace": "MERCADOLIVRE",
            "badge": "New",
            "imageUrl": "https://images.unsplash.com/photo-1606066906352-0282f9b56bce?w=600",
            "link": "https://www.mercadolivre.com.br/iphone12-128gb-Green",
        },
        {
            "title": "iPhone 12 Pro 128GB",
            "price": "R$ 2.899",
            "marketplace": "FACEBOOK",
            "badge": "Oferta",
            "imageUrl": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600",
            "link": "https://facebook.com/marketplace/iphone12-pro",
        },
        {
            "title": "iPhone 12 256GB White",
            "price": "R$ 2.650",
            "marketplace": "OLX",
            "badge": "Like new",
            "imageUrl": "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=600",
            "link": "https://www.olx.com.br/iphone12-256",
        },
        {
            "title": "iPhone 12 Mini 64GB",
            "price": "R$ 1.550",
            "marketplace": "OLX",
            "badge": "Low price",
            "imageUrl": "https://images.unsplash.com/photo-1529612700005-e35377bf1415?w=600",
            "link": "https://www.olx.com.br/iphone12-mini",
        },
        {
            "title": "iPhone 12 128GB Purple",
            "price": "R$ 2.200",
            "marketplace": "FACEBOOK",
            "badge": "Top deal",
            "imageUrl": "https://images.unsplash.com/photo-1512499617640-c2f999098c01?w=600",
            "link": "https://facebook.com/marketplace/iphone12-Purple",
        },
        {
            "title": "iPhone 12 64GB Blue",
            "price": "R$ 1.750",
            "marketplace": "MERCADOLIVRE",
            "badge": "Low price",
            "imageUrl": "https://images.unsplash.com/photo-1475180098004-ca77a66827be?w=600",
            "link": "https://www.mercadolivre.com.br/iphone12-Blue",
        },
        {
            "title": "iPhone 12 128GB White",
            "price": "R$ 2.150",
            "marketplace": "FACEBOOK",
            "badge": "Sealed",
            "imageUrl": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600",
            "link": "https://facebook.com/marketplace/iphone12-White",
        },
    ],
    "macbook": [
        {
            "title": "MacBook Air M1 256GB",
            "price": "R$ 4.200",
            "marketplace": "OLX",
            "badge": "Like new",
            "imageUrl": "https://images.unsplash.com/photo-1503602642458-232111445657?w=600",
            "link": "https://www.olx.com.br/macbook-air-m1",
        },
        {
            "title": "MacBook Pro 14\"",
            "price": "R$ 9.800",
            "marketplace": "FACEBOOK",
            "badge": "Sealed",
            "imageUrl": "https://images.unsplash.com/photo-1517331156700-3c241d2b4d83?w=600",
            "link": "https://facebook.com/marketplace/macbook-pro-14",
        },
        {
            "title": "MacBook Air M2 512GB",
            "price": "R$ 6.300",
            "marketplace": "MERCADOLIVRE",
            "badge": "Premium",
            "imageUrl": "https://images.unsplash.com/photo-1517445312885-5bc20087f9e2?w=600",
            "link": "https://www.mercadolivre.com.br/macbook-air-m2",
        },
        {
            "title": "MacBook Pro 13\" i5",
            "price": "R$ 3.900",
            "marketplace": "OLX",
            "badge": "Low price",
            "imageUrl": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600",
            "link": "https://www.olx.com.br/macbook-pro-13",
        },
        {
            "title": "MacBook Air 2019",
            "price": "R$ 3.100",
            "marketplace": "FACEBOOK",
            "badge": "Good condition",
            "imageUrl": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600",
            "link": "https://facebook.com/marketplace/macbook-air-2019",
        },
        {
            "title": "MacBook Pro 16\" i9",
            "price": "R$ 8.700",
            "marketplace": "MERCADOLIVRE",
            "badge": "Top deal",
            "imageUrl": "https://images.unsplash.com/photo-1511385348-a52b4a160dc2?w=600",
            "link": "https://www.mercadolivre.com.br/macbook-pro-16",
        },
        {
            "title": "MacBook Air M2 8GB",
            "price": "R$ 5.800",
            "marketplace": "FACEBOOK",
            "badge": "New",
            "imageUrl": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600",
            "link": "https://facebook.com/marketplace/macbook-air-m2",
        },
        {
            "title": "MacBook Pro 15\" Retina",
            "price": "R$ 4.500",
            "marketplace": "OLX",
            "badge": "Like new",
            "imageUrl": "https://images.unsplash.com/photo-1483058712412-4245e9b90334?w=600",
            "link": "https://www.olx.com.br/macbook-pro-15",
        },
    ],
}


def create_app(state: dict | None = None, settings=None, ai_client=None, bot=None) -> FastAPI:
    settings = settings or load_settings()
    ai_client = ai_client or AIClient(settings.gemini_api_key)
    state = state or _bootstrap_state(settings)

    app = FastAPI(title="ProspectorBot API")
    app.state.state = state
    app.state.settings = settings
    app.state.ai_client = ai_client
    app.state.bot = bot
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    def _require_api_key(request: Request) -> None:
        if settings.api_key:
            incoming = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
            if incoming != settings.api_key:
                raise HTTPException(status_code=401, detail="invalid api key")

    guard = Depends(_require_api_key)

    @app.get("/health", dependencies=[guard])
    def health() -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = list(state.get("clients", []))
            last_scan = state.get("last_scan_at")
        return {"status": "ok", "clients": len(clients), "last_scan_at": last_scan}

    @app.get("/mock", dependencies=[guard])
    def mock_items() -> dict:
        """Return mock data for demos."""
        return MOCK_DATA

    @app.get("/clients", dependencies=[guard])
    def list_clients() -> list[dict]:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            return list(state.get("clients", []))

    @app.get("/clients/{chat_id}", dependencies=[guard])
    def get_client(chat_id: str) -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            client = _find_client(state.get("clients", []), chat_id)
        if not client:
            raise HTTPException(status_code=404, detail="client not found")
        return client

    @app.post("/clients", dependencies=[guard])
    def upsert_client_endpoint(payload: ClientPayload) -> dict:
        data = _payload_to_dict(payload)
        chat_id = data.get("chat_id")
        if not chat_id:
            raise HTTPException(status_code=400, detail="chat_id is required")

        state = app.state.state
        lock = _get_lock(state)
        with lock:
            existing = _find_client(state.get("clients", []), chat_id)
            merged = _merge_payload(existing, data)
            normalized = normalize_client(merged)
            state["clients"] = upsert_client(state.get("clients", []), normalized)
            save_preferences(app.state.settings, state["clients"])
            return normalized

    @app.put("/clients/{chat_id}", dependencies=[guard])
    def update_client(chat_id: str, payload: ClientPayload) -> dict:
        data = _payload_to_dict(payload)
        data["chat_id"] = chat_id
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            existing = _find_client(state.get("clients", []), chat_id)
            merged = _merge_payload(existing, data)
            normalized = normalize_client(merged)
            state["clients"] = upsert_client(state.get("clients", []), normalized)
            save_preferences(app.state.settings, state["clients"])
            return normalized

    @app.delete("/clients/{chat_id}", dependencies=[guard])
    def delete_client(chat_id: str) -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = [c for c in state.get("clients", []) if str(c.get("chat_id")) != str(chat_id)]
            state["clients"] = clients
            save_preferences(app.state.settings, clients)
        return {"status": "deleted"}

    @app.post("/clients/{chat_id}/pause", dependencies=[guard])
    def pause_client(chat_id: str) -> dict:
        return _set_client_active(app, chat_id, False)

    @app.post("/clients/{chat_id}/resume", dependencies=[guard])
    def resume_client(chat_id: str) -> dict:
        return _set_client_active(app, chat_id, True)

    @app.post("/parse", dependencies=[guard])
    def parse_message(payload: ParseRequest) -> dict:
        reply, data = app.state.ai_client.parse_message(payload.message, payload.locale)
        return {"reply": reply, "payload": data}

    @app.get("/offers", dependencies=[guard])
    def get_offers(chat_id: str | None = None) -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            offers = state.get("last_offers", {})
            if chat_id:
                return {"offers": offers.get(chat_id, [])}
            return {"offers": offers}

    @app.post("/engine/start", dependencies=[guard])
    def engine_start() -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            state["running"] = True
            thread = state.get("engine_thread")
            if thread and getattr(thread, "is_alive", lambda: False)():
                return {"status": "already_running"}
            thread = threading.Thread(
                target=run_scraper_loop,
                args=(app.state.settings, state, app.state.bot),
                daemon=True,
            )
            state["engine_thread"] = thread
            thread.start()
        return {"status": "started"}

    @app.post("/engine/stop", dependencies=[guard])
    def engine_stop() -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            state["running"] = False
        return {"status": "stopping"}

    @app.get("/api/preferences", dependencies=[guard])
    def list_preferences() -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = list(state.get("clients", []))
        data = [_client_to_preference(client) for client in clients]
        return {"success": True, "data": data}

    @app.post("/api/preferences", dependencies=[guard])
    def create_preference(payload: PreferencePayload) -> dict:
        data = _payload_to_dict(payload)
        chat_id = data.get("chat_id") or data.get("chatId")
        if not chat_id:
            raise HTTPException(status_code=400, detail="chat_id is required")

        raw = _preference_payload_to_client(data)
        normalized = normalize_client(raw)

        state = app.state.state
        lock = _get_lock(state)
        with lock:
            state["clients"] = upsert_client(state.get("clients", []), normalized)
            save_preferences(app.state.settings, state["clients"])
        return {"success": True, "data": _client_to_preference(normalized)}

    @app.put("/api/preferences/{index}", dependencies=[guard])
    def update_preference(index: int, payload: PreferencePayload) -> dict:
        data = _payload_to_dict(payload)
        raw = _preference_payload_to_client(data)

        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = list(state.get("clients", []))
            if index < 0 or index >= len(clients):
                raise HTTPException(status_code=404, detail="preference not found")
            existing = clients[index]
            merged = _merge_payload(existing, raw)
            normalized = normalize_client(merged)
            clients[index] = normalized
            state["clients"] = clients
            save_preferences(app.state.settings, clients)
        return {"success": True, "data": _client_to_preference(normalized)}

    @app.delete("/api/preferences/{index}", dependencies=[guard])
    def delete_preference(index: int) -> dict:
        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = list(state.get("clients", []))
            if index < 0 or index >= len(clients):
                raise HTTPException(status_code=404, detail="preference not found")
            clients.pop(index)
            state["clients"] = clients
            save_preferences(app.state.settings, clients)
        return {"success": True}

    @app.post("/api/search", dependencies=[guard])
    def search_items(payload: dict) -> dict:
        preference_index = payload.get("preference_index")
        if preference_index is None:
            raise HTTPException(status_code=400, detail="preference_index is required")

        state = app.state.state
        lock = _get_lock(state)
        with lock:
            clients = list(state.get("clients", []))
        try:
            pref = clients[int(preference_index)]
        except Exception:
            raise HTTPException(status_code=404, detail="preference not found")

        term = str(pref.get("search_term") or "").lower().strip()
        items = _mock_items_for_term(term)
        return {"success": True, "data": {"items": items}}

    @app.post("/api/ai/analyze", dependencies=[guard])
    def analyze_product(payload: dict) -> dict:
        product = payload.get("produto") or payload.get("product") or "Unknown product"
        price = payload.get("preco") or payload.get("price") or payload.get("preco_max") or "N/A"
        analysis = (
            f"Quick take: {product} at {price} looks competitive for most local markets. "
            "For best results, compare recent listings and verify condition before purchase."
        )
        return {"success": True, "data": {"analysis": analysis}}

    @app.post("/api/ai/suggest-search", dependencies=[guard])
    def suggest_search(payload: dict) -> dict:
        product = payload.get("produto") or payload.get("product") or ""
        city = payload.get("cidade") or payload.get("city") or ""
        suggestions = _build_suggestions(product, city)
        return {"success": True, "data": {"suggestions": suggestions}}


    return app


def _bootstrap_state(settings) -> dict:
    from ..storage import load_preferences

    return {
        "clients": load_preferences(settings),
        "running": True,
        "lock": threading.Lock(),
        "last_offers": {},
        "pending_locales": {},
    }


def _payload_to_dict(payload: BaseModel) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump(exclude_unset=True)
    return payload.dict(exclude_unset=True)


def _merge_payload(existing: dict | None, update: dict) -> dict:
    merged = dict(existing) if existing else {}
    for key, value in update.items():
        if value is not None:
            merged[key] = value
    return merged


def _find_client(clients: list[dict], chat_id: str) -> dict | None:
    for client in clients:
        if str(client.get("chat_id")) == str(chat_id):
            return client
    return None


def _get_lock(state: dict) -> threading.Lock:
    lock = state.get("lock")
    if not hasattr(lock, "acquire"):
        lock = threading.Lock()
        state["lock"] = lock
    return lock


def _set_client_active(app: FastAPI, chat_id: str, active: bool) -> dict:
    state = app.state.state
    lock = _get_lock(state)
    with lock:
        client = _find_client(state.get("clients", []), chat_id)
        if not client:
            raise HTTPException(status_code=404, detail="client not found")
        client["active"] = active
        save_preferences(app.state.settings, state["clients"])
    return {"status": "ok", "active": active}

def _client_to_preference(client: dict) -> dict:
    sources = client.get("sources", {}) if isinstance(client, dict) else {}

    def _source_payload(key: str) -> dict:
        cfg = sources.get(key) or {}
        return {
            "ativo": bool(cfg.get("active", True)),
            "url": cfg.get("url", ""),
        }

    return {
        "chat_id": client.get("chat_id", ""),
        "produto": client.get("search_term", ""),
        "cidade_alvo": client.get("target_city", ""),
        "preco_min": client.get("price_min", 0),
        "preco_max": client.get("price_max", 0),
        "palavras_negativas": client.get("negative_keywords", []),
        "fontes": {
            "facebook": _source_payload("facebook"),
            "mercadolivre": _source_payload("mercado_livre"),
            "olx": _source_payload("olx"),
        },
    }


def _preference_payload_to_client(data: dict) -> dict:
    sources = {}
    fontes = data.get("fontes") or {}

    def _merge_source(key: str, ativo_key: str, url_key: str, alias: str) -> None:
        cfg = fontes.get(alias) or {}
        active = data.get(ativo_key)
        url = data.get(url_key)
        if active is None:
            active = cfg.get("ativo")
        if url is None:
            url = cfg.get("url")
        if active is not None or url is not None:
            sources[key] = {"active": bool(active) if active is not None else True, "url": url or ""}

    _merge_source("facebook", "facebook_ativo", "facebook_url", "facebook")
    _merge_source("mercado_livre", "mercadolivre_ativo", "mercadolivre_url", "mercadolivre")
    _merge_source("olx", "olx_ativo", "olx_url", "olx")

    return {
        "chat_id": data.get("chat_id") or data.get("chatId") or "",
        "search_term": data.get("produto") or data.get("product") or "",
        "target_city": data.get("cidade_alvo") or data.get("city") or "",
        "price_min": data.get("preco_min") or data.get("price_min") or 0,
        "price_max": data.get("preco_max") or data.get("price_max") or 0,
        "negative_keywords": data.get("palavras_negativas") or data.get("negative_keywords") or [],
        "sources": sources,
    }


def _mock_items_for_term(term: str) -> list[dict]:
    term_key = "iphone" if "iphone" in term else "macbook" if "macbook" in term else None
    items = MOCK_DATA.get(term_key, []) if term_key else list(MOCK_DATA.get("iphone", []))
    mapped = []
    for idx, item in enumerate(items, start=1):
        mapped.append(
            {
                "origem": item.get("marketplace", "MARKET"),
                "cor": "blue",
                "id": str(idx),
                "titulo": item.get("title", ""),
                "preco_texto": item.get("price", ""),
                "link": item.get("link", ""),
                "info_extra": item.get("badge", ""),
                "imagem_url": item.get("imageUrl", ""),
            }
        )
    return mapped


def _build_suggestions(product: str, city: str) -> str:
    product = str(product or "").strip()
    city = str(city or "").strip()
    parts = []
    if product:
        query = product.replace(" ", "+")
        if city:
            parts.append(f"Facebook Marketplace: https://www.facebook.com/marketplace/{city}/search?query={query}")
        parts.append(f"Mercado Livre: https://lista.mercadolivre.com.br/{query}")
        parts.append(f"OLX: https://www.olx.com.br/brasil?q={query}")
    else:
        parts.append("Provide a product name to generate marketplace URLs.")
    return "\n".join(parts)






