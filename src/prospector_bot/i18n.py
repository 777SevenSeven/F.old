"""
================================================================================
CORE MODULE: INTERNATIONALIZATION (I18N) & LOCALIZATION
================================================================================
FUNCTION:
Manages multi-language support (English, Spanish, French, German, Italian, 
Portuguese) and context-aware messaging for the global user base.

[PRODUCT STRATEGY & MARKET VALIDATION - ANDRE (PM)]
Go-to-Market (Q1): The legacy prototype was validated exclusively in the 
Brazilian market (PT-BR). 
Scaling Decision (Q2): To increase Total Addressable Market (TAM), the system 
was refactored into this dynamic i18n architecture. Hardcoded strings were 
eliminated, allowing immediate deployment across North America and Europe with 
zero changes to the AI Core.

[LEGAL & COMPLIANCE - IASMIN]
Cultural Formatting: Ensures currency symbols, price formatting, and UI/UX flows 
respect regional data presentation laws.
================================================================================
"""
from __future__ import annotations

from typing import Mapping

SUPPORTED_LOCALES = {"en", "es", "fr", "de", "it", "pt-BR"}
_ALIASES = {
    "en": "en",
    "en-us": "en",
    "en_us": "en",
    "es": "es",
    "es-es": "es",
    "es_es": "es",
    "fr": "fr",
    "fr-fr": "fr",
    "fr_fr": "fr",
    "de": "de",
    "de-de": "de",
    "de_de": "de",
    "it": "it",
    "it-it": "it",
    "it_it": "it",
    "pt": "pt-BR",
    "pt-br": "pt-BR",
    "pt_br": "pt-BR",
}

_LOCALE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt-BR": "Portuguese (Brazil)",
}

_MESSAGES: dict[str, Mapping[str, str]] = {
    "en": {
        "paused": "Paused. Type 'resume' or /menu to continue.",
        "resumed": "Resumed. I will keep searching.",
        "status": "Searching for {search_term} in {target_city}.",
        "config_confirmed": (
            "Configuration confirmed.\n\n"
            "Mode: {persona}\n"
            "Search: {search_term}\n"
            "City: {target_city}\n"
            "Max price: {price_max}\n\n"
            "I am searching now and will notify you when I find matches."
        ),
        "ai_ready": "Great. I will start searching now.",
        "ai_missing_fields": "I need the product, max price, and city.",
        "ai_fallback_starting": "Got it. I am starting the search.",
        "ai_fallback_prompt": (
            "Tell me the product, the maximum price, and the city. "
            "Example: 'PlayStation 5 up to 2500 in Sao Paulo'."
        ),
        "offer_default_title": "Listing",
        "offer_found": "FOUND:",
        "offer_source": "Source: {source}",
        "offer_title": "Title: {title}",
        "offer_price": "Price: {price}",
        "offer_info": "Info: {extra}",
        "offer_link": "Link: {link}",
        "lang_prompt": (
            "Language settings:\n"
            "Use /lang <code> to switch.\n"
            "Available: {locales}"
        ),
        "lang_updated": "Language updated to {locale}.",
        "lang_unknown": "Unknown language. Available: {locales}",
    },
    "es": {
        "paused": "Pausado. Escribe 'resume' o /menu para continuar.",
        "resumed": "Reanudado. Seguire buscando.",
        "status": "Buscando {search_term} en {target_city}.",
        "config_confirmed": (
            "Configuracion confirmada.\n\n"
            "Modo: {persona}\n"
            "Busqueda: {search_term}\n"
            "Ciudad: {target_city}\n"
            "Precio maximo: {price_max}\n\n"
            "Estoy buscando ahora y avisare cuando encuentre resultados."
        ),
        "ai_ready": "Genial. Empezare a buscar ahora.",
        "ai_missing_fields": "Necesito el producto, el precio maximo y la ciudad.",
        "ai_fallback_starting": "Entendido. Empezare la busqueda.",
        "ai_fallback_prompt": (
            "Dime el producto, el precio maximo y la ciudad. "
            "Ejemplo: 'PlayStation 5 hasta 2500 en Sao Paulo'."
        ),
        "offer_default_title": "Anuncio",
        "offer_found": "ENCONTRADO:",
        "offer_source": "Fuente: {source}",
        "offer_title": "Titulo: {title}",
        "offer_price": "Precio: {price}",
        "offer_info": "Info: {extra}",
        "offer_link": "Enlace: {link}",
        "lang_prompt": (
            "Configuracion de idioma:\n"
            "Usa /lang <code> para cambiar.\n"
            "Disponibles: {locales}"
        ),
        "lang_updated": "Idioma actualizado a {locale}.",
        "lang_unknown": "Idioma desconocido. Disponibles: {locales}",
    },
    "fr": {
        "paused": "En pause. Tapez 'resume' ou /menu pour continuer.",
        "resumed": "Reprise. Je continue la recherche.",
        "status": "Recherche de {search_term} a {target_city}.",
        "config_confirmed": (
            "Configuration confirmee.\n\n"
            "Mode : {persona}\n"
            "Recherche : {search_term}\n"
            "Ville : {target_city}\n"
            "Prix max : {price_max}\n\n"
            "Je cherche maintenant et vous alerterai en cas de resultat."
        ),
        "ai_ready": "Parfait. Je demarre la recherche.",
        "ai_missing_fields": "J'ai besoin du produit, du prix max et de la ville.",
        "ai_fallback_starting": "Compris. Je lance la recherche.",
        "ai_fallback_prompt": (
            "Indiquez le produit, le prix max et la ville. "
            "Exemple : 'PlayStation 5 jusqu'a 2500 a Sao Paulo'."
        ),
        "offer_default_title": "Annonce",
        "offer_found": "TROUVE :",
        "offer_source": "Source : {source}",
        "offer_title": "Titre : {title}",
        "offer_price": "Prix : {price}",
        "offer_info": "Info : {extra}",
        "offer_link": "Lien : {link}",
        "lang_prompt": (
            "Parametres de langue :\n"
            "Utilisez /lang <code> pour changer.\n"
            "Disponibles : {locales}"
        ),
        "lang_updated": "Langue mise a jour : {locale}.",
        "lang_unknown": "Langue inconnue. Disponibles : {locales}",
    },
    "de": {
        "paused": "Pausiert. Tippe 'resume' oder /menu, um fortzufahren.",
        "resumed": "Fortgesetzt. Ich suche weiter.",
        "status": "Suche nach {search_term} in {target_city}.",
        "config_confirmed": (
            "Konfiguration bestaetigt.\n\n"
            "Modus: {persona}\n"
            "Suche: {search_term}\n"
            "Stadt: {target_city}\n"
            "Max. Preis: {price_max}\n\n"
            "Ich suche jetzt und melde mich bei Treffern."
        ),
        "ai_ready": "Super. Ich starte die Suche.",
        "ai_missing_fields": "Ich brauche Produkt, Hoechstpreis und Stadt.",
        "ai_fallback_starting": "Alles klar. Ich starte die Suche.",
        "ai_fallback_prompt": (
            "Nenne Produkt, Hoechstpreis und Stadt. "
            "Beispiel: 'PlayStation 5 bis 2500 in Sao Paulo'."
        ),
        "offer_default_title": "Anzeige",
        "offer_found": "GEFUNDEN:",
        "offer_source": "Quelle: {source}",
        "offer_title": "Titel: {title}",
        "offer_price": "Preis: {price}",
        "offer_info": "Info: {extra}",
        "offer_link": "Link: {link}",
        "lang_prompt": (
            "Spracheinstellungen:\n"
            "Nutze /lang <code> zum Wechseln.\n"
            "Verfuegbar: {locales}"
        ),
        "lang_updated": "Sprache geaendert auf {locale}.",
        "lang_unknown": "Unbekannte Sprache. Verfuegbar: {locales}",
    },
    "it": {
        "paused": "In pausa. Digita 'resume' o /menu per continuare.",
        "resumed": "Ripreso. Continuero a cercare.",
        "status": "Cerco {search_term} a {target_city}.",
        "config_confirmed": (
            "Configurazione confermata.\n\n"
            "Modalita: {persona}\n"
            "Ricerca: {search_term}\n"
            "Citta: {target_city}\n"
            "Prezzo massimo: {price_max}\n\n"
            "Sto cercando e ti avvisero quando trovo risultati."
        ),
        "ai_ready": "Perfetto. Avvio la ricerca.",
        "ai_missing_fields": "Mi servono prodotto, prezzo massimo e citta.",
        "ai_fallback_starting": "Ok. Avvio la ricerca.",
        "ai_fallback_prompt": (
            "Dimmi prodotto, prezzo massimo e citta. "
            "Esempio: 'PlayStation 5 fino a 2500 a Sao Paulo'."
        ),
        "offer_default_title": "Annuncio",
        "offer_found": "TROVATO:",
        "offer_source": "Fonte: {source}",
        "offer_title": "Titolo: {title}",
        "offer_price": "Prezzo: {price}",
        "offer_info": "Info: {extra}",
        "offer_link": "Link: {link}",
        "lang_prompt": (
            "Impostazioni lingua:\n"
            "Usa /lang <code> per cambiare.\n"
            "Disponibili: {locales}"
        ),
        "lang_updated": "Lingua aggiornata a {locale}.",
        "lang_unknown": "Lingua sconosciuta. Disponibili: {locales}",
    },
    "pt-BR": {
        "paused": "Pausado. Digite 'resume' ou /menu para continuar.",
        "resumed": "Retomado. Vou continuar buscando.",
        "status": "Procurando por {search_term} em {target_city}.",
        "config_confirmed": (
            "Configuracao confirmada.\n\n"
            "Modo: {persona}\n"
            "Busca: {search_term}\n"
            "Cidade: {target_city}\n"
            "Preco maximo: {price_max}\n\n"
            "Estou buscando agora e avisarei quando encontrar resultados."
        ),
        "ai_ready": "Otimo. Vou comecar a buscar agora.",
        "ai_missing_fields": "Preciso do produto, do preco maximo e da cidade.",
        "ai_fallback_starting": "Entendido. Vou iniciar a busca.",
        "ai_fallback_prompt": (
            "Me diga o produto, o preco maximo e a cidade. "
            "Exemplo: 'PlayStation 5 ate 2500 em Sao Paulo'."
        ),
        "offer_default_title": "Anuncio",
        "offer_found": "ENCONTRADO:",
        "offer_source": "Fonte: {source}",
        "offer_title": "Titulo: {title}",
        "offer_price": "Preco: {price}",
        "offer_info": "Info: {extra}",
        "offer_link": "Link: {link}",
        "lang_prompt": (
            "Configuracoes de idioma:\n"
            "Use /lang <code> para trocar.\n"
            "Disponiveis: {locales}"
        ),
        "lang_updated": "Idioma atualizado para {locale}.",
        "lang_unknown": "Idioma desconhecido. Disponiveis: {locales}",
    },
}


def normalize_locale(locale: str | None, default: str = "en") -> str:
    if not locale:
        return default if default in SUPPORTED_LOCALES else "en"
    raw = str(locale).strip().replace("_", "-")
    lowered = raw.lower()
    if lowered in _ALIASES:
        return _ALIASES[lowered]
    if "-" in raw:
        base = raw.split("-", 1)[0].lower()
        if base in _ALIASES:
            return _ALIASES[base]
    if raw in SUPPORTED_LOCALES:
        return raw
    if lowered in SUPPORTED_LOCALES:
        return lowered
    return default if default in SUPPORTED_LOCALES else "en"


def select_locale(preferred: str | None, language_code: str | None, default: str = "en") -> str:
    if preferred:
        return normalize_locale(preferred, default)
    if language_code:
        return normalize_locale(language_code, default)
    return normalize_locale(default, "en")


def resolve_locale(requested: str | None) -> str | None:
    if not requested:
        return None
    raw = str(requested).strip()
    lowered = raw.lower().replace("_", "-")
    if lowered in _ALIASES:
        return _ALIASES[lowered]
    if raw in SUPPORTED_LOCALES:
        return raw
    if lowered in SUPPORTED_LOCALES:
        return lowered
    return None


def language_name(locale: str | None) -> str | None:
    normalized = normalize_locale(locale, "en")
    return _LOCALE_NAMES.get(normalized)


def t(locale: str | None, key: str, **kwargs) -> str:
    normalized = normalize_locale(locale, "en")
    messages = _MESSAGES.get(normalized) or _MESSAGES["en"]
    template = messages.get(key) or _MESSAGES["en"].get(key) or key
    try:
        return template.format(**kwargs)
    except Exception:
        return template
