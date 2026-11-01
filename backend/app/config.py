import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)

# All persistent state (SQLite database and uploaded pictures) lives in one
# directory so a single volume/bind mount is enough to back everything up.
DATA_DIR = os.path.abspath(
    os.environ.get("DATA_DIR") or os.path.join(BASE_DIR, "instance")
)
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

# Built frontend (served by Flask in production). Absent during development.
FRONTEND_DIST = os.path.abspath(
    os.environ.get("FRONTEND_DIST") or os.path.join(REPO_DIR, "frontend", "dist")
)

APP_ENV = (os.environ.get("APP_ENV") or "development").strip().lower()
IS_PRODUCTION = APP_ENV in {"production", "prod"}


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _secret_key() -> str:
    value = (os.environ.get("SECRET_KEY") or "").strip()
    if value:
        return value
    if IS_PRODUCTION:
        raise RuntimeError(
            "SECRET_KEY must be set when APP_ENV=production. "
            "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
        )
    return "dev-secret-change-me"


class Config:
    APP_ENV = APP_ENV
    IS_PRODUCTION = IS_PRODUCTION

    SECRET_KEY = _secret_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(DATA_DIR, "flagomiu.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATA_DIR = DATA_DIR
    UPLOAD_FOLDER = UPLOAD_DIR
    FRONTEND_DIST = FRONTEND_DIST

    # Same-origin deployment needs no CORS at all; only enable it when the
    # origins are configured explicitly (comma separated).
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get(
            "CORS_ORIGINS", "" if IS_PRODUCTION else "*"
        ).split(",")
        if origin.strip()
    ]

    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", "32")) * 1024 * 1024

    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", IS_PRODUCTION)
    PREFERRED_URL_SCHEME = "https" if IS_PRODUCTION else "http"

    # Trust one reverse proxy hop (Coolify/Traefik) for scheme and client IP.
    TRUST_PROXY = env_bool("TRUST_PROXY", IS_PRODUCTION)

    JSON_SORT_KEYS = False
