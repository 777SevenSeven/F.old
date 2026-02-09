"""Runtime settings and paths."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import sys


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"").strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        return


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class Settings:
    base_dir: Path
    data_dir: Path
    session_dir: Path
    history_path: Path
    preferences_path: Path
    telegram_token: str
    gemini_api_key: str
    interval_minutes: float
    headless: bool
    browser_channel: str | None
    force_login: bool
    api_host: str
    api_port: int
    api_key: str
    ebay_app_id: str
    ebay_global_id: str
    ebay_currency: str
    default_locale: str


def load_settings() -> Settings:
    base_dir = _get_base_dir()
    _load_env_file(base_dir / ".env")

    data_dir = Path(os.getenv("DATA_DIR") or base_dir / "data")
    session_dir = Path(os.getenv("SESSION_DIR") or data_dir / "browser_session")
    history_path = Path(os.getenv("SEEN_HISTORY_PATH") or data_dir / "seen_history.json")
    preferences_path = Path(os.getenv("USER_PREFERENCES_PATH") or data_dir / "user_preferences.json")

    telegram_token = os.getenv("TELEGRAM_TOKEN") or ""
    gemini_api_key = os.getenv("GEMINI_API_KEY") or ""

    interval_raw = (
        os.getenv("SCAN_INTERVAL_MINUTES")
        or os.getenv("INTERVAL_MINUTES")
        or os.getenv("INTERVALO_MINUTOS")
        or "5"
    )
    try:
        interval_minutes = float(interval_raw)
    except Exception:
        interval_minutes = 5.0

    headless = _to_bool(os.getenv("HEADLESS"), default=False)
    force_login = _to_bool(os.getenv("FORCE_LOGIN"), default=False)
    browser_channel = os.getenv("BROWSER_CHANNEL") or "chrome"
    api_host = os.getenv("API_HOST") or "0.0.0.0"
    api_port_raw = os.getenv("API_PORT") or "8000"
    try:
        api_port = int(api_port_raw)
    except Exception:
        api_port = 8000
    api_key = os.getenv("API_KEY") or ""
    ebay_app_id = os.getenv("EBAY_APP_ID") or ""
    ebay_global_id = os.getenv("EBAY_GLOBAL_ID") or "EBAY-US"
    ebay_currency = os.getenv("EBAY_CURRENCY") or "USD"
    default_locale = os.getenv("DEFAULT_LOCALE") or os.getenv("BOT_LOCALE") or "en"

    return Settings(
        base_dir=base_dir,
        data_dir=data_dir,
        session_dir=session_dir,
        history_path=history_path,
        preferences_path=preferences_path,
        telegram_token=telegram_token,
        gemini_api_key=gemini_api_key,
        interval_minutes=interval_minutes,
        headless=headless,
        browser_channel=browser_channel,
        force_login=force_login,
        api_host=api_host,
        api_port=api_port,
        api_key=api_key,
        ebay_app_id=ebay_app_id,
        ebay_global_id=ebay_global_id,
        ebay_currency=ebay_currency,
        default_locale=default_locale,
    )

