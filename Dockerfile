# syntax=docker/dockerfile:1

# --- Frontend build -----------------------------------------------------------
FROM node:26.13.0-alpine AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- Backend runtime ----------------------------------------------------------
FROM python:3.15.2-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=0 \
    DATA_DIR=/data/flagomiu \
    TZ=Europe/Zurich \
    APP_ENV=production

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends passwd tzdata; \
    rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 10001 app; \
    useradd --uid 10001 --gid 10001 --home-dir /app --shell /usr/sbin/nologin app; \
    mkdir -p /app/backend /app/frontend /data/flagomiu/uploads; \
    chown -R 10001:10001 /app /data

WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --python /usr/local/bin/python3

COPY backend/ ./
COPY --from=frontend /build/dist /app/frontend/dist
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod 0755 /usr/local/bin/entrypoint.sh \
    && chown -R 10001:10001 /app

ENV PATH="/opt/venv/bin:$PATH" \
    HOME=/app

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4)"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["gunicorn", "--workers", "2", "--worker-class", "gthread", "--threads", "4", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
