"""Search URL builders."""
from __future__ import annotations

from urllib.parse import parse_qs, quote_plus, urlencode, urlparse, urlunparse

from .text import to_slug


def build_craigslist_url(
    search_term: str,
    price_min: float,
    price_max: float,
    city: str | None = None,
    base_url: str | None = None,
) -> str:
    params = {
        "query": search_term or "",
        "min_price": int(price_min) if price_min else 0,
        "max_price": int(price_max) if price_max else 999999,
        "format": "rss",
    }
    if base_url:
        parsed = urlparse(base_url)
        if parsed.scheme and parsed.netloc:
            base = urlunparse(parsed._replace(query="", fragment=""))
            return f"{base}?{urlencode(params)}"

    slug = to_slug(city or "") or "geo"
    base = f"https://{slug}.craigslist.org/search/sss"
    return f"{base}?{urlencode(params)}"


def build_ebay_url(search_term: str, price_min: float, price_max: float) -> str:
    params = {
        "_nkw": search_term or "",
        "_udlo": int(price_min) if price_min else "",
        "_udhi": int(price_max) if price_max else "",
    }
    return f"https://www.ebay.com/sch/i.html?{urlencode(params)}"


def build_olx_url(
    search_term: str,
    price_min: float,
    price_max: float,
    city: str | None = None,
    base_url: str | None = None,
) -> str:
    base = base_url or "https://www.olx.com.br/brasil"
    parsed = urlparse(base)
    if not parsed.scheme or not parsed.netloc:
        parsed = urlparse("https://www.olx.com.br/brasil")

    query = parse_qs(parsed.query)
    query["q"] = [search_term or ""]
    query["ps"] = [str(int(price_min))] if price_min else ["0"]
    query["pe"] = [str(int(price_max))] if price_max else ["999999"]
    query.setdefault("sf", ["1"])

    return urlunparse(parsed._replace(query=urlencode(query, doseq=True), fragment=""))


def build_facebook_url(
    search_term: str,
    price_min: float,
    price_max: float,
    city: str | None = None,
    base_url: str | None = None,
) -> str:
    base = base_url or "https://www.facebook.com/marketplace/search"
    parsed = urlparse(base)
    if not parsed.scheme or not parsed.netloc:
        parsed = urlparse("https://www.facebook.com/marketplace/search")

    query = parse_qs(parsed.query)
    query["query"] = [search_term or ""]

    if price_min and price_min > 0:
        query["minPrice"] = [str(int(price_min))]
    else:
        query.pop("minPrice", None)

    if price_max and price_max > 0:
        query["maxPrice"] = [str(int(price_max))]
    else:
        query.pop("maxPrice", None)

    query.setdefault("sortBy", ["creation_time_descend"])
    query.setdefault("exact", ["false"])

    return urlunparse(parsed._replace(query=urlencode(query, doseq=True), fragment=""))


def build_mercado_livre_url(
    search_term: str,
    price_min: float,
    price_max: float,
    city: str | None = None,
    base_url: str | None = None,
) -> str:
    base = base_url or "https://lista.mercadolivre.com.br/"
    parsed = urlparse(base)
    if not parsed.scheme or not parsed.netloc:
        parsed = urlparse("https://lista.mercadolivre.com.br/")

    min_price = int(price_min) if price_min and price_min > 0 else 0
    max_price = int(price_max) if price_max and price_max > 0 else 999999

    term = quote_plus(search_term or "")
    search_segment = f"{term}_PriceRange_{min_price}BRL-{max_price}BRL_NoIndex_True"

    prefix = parsed.path.strip("/")
    if prefix:
        parts = prefix.split("/")
        if "_PriceRange_" in parts[-1]:
            parts = parts[:-1]
        prefix = "/".join(parts)
    new_path = f"/{search_segment}" if not prefix else f"/{prefix}/{search_segment}"

    return urlunparse(parsed._replace(path=new_path, query="", fragment=""))

