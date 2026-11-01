import os

from flask import Flask, abort, jsonify, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import cors, db

IMMUTABLE = "public, max-age=31536000, immutable"
NO_CACHE = "no-cache"


def _register_frontend(app: Flask) -> None:
    """Serve the built Vue app (including PWA files) when a dist folder exists."""
    dist = app.config.get("FRONTEND_DIST") or ""
    if not os.path.isfile(os.path.join(dist, "index.html")):
        return

    def _send(filename: str, cache_control: str):
        response = send_from_directory(dist, filename)
        response.headers["Cache-Control"] = cache_control
        return response

    def _index():
        # The app shell and the service worker must never be cached hard,
        # otherwise a new deployment would not reach installed PWAs.
        return _send("index.html", NO_CACHE)

    @app.get("/")
    def frontend_index():
        return _index()

    @app.get("/<path:filename>")
    def frontend_asset(filename: str):
        if filename == "api" or filename.startswith("api/"):
            abort(404)
        if os.path.isfile(os.path.join(dist, filename)):
            cache = IMMUTABLE if filename.startswith("assets/") else NO_CACHE
            return _send(filename, cache)
        # Vue Router uses history mode: unknown paths render the app shell.
        return _index()


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    if app.config.get("TRUST_PROXY"):
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1
        )

    os.makedirs(app.config["DATA_DIR"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    cors_origins = app.config.get("CORS_ORIGINS") or []
    if cors_origins:
        cors.init_app(
            app,
            resources={r"/api/*": {"origins": cors_origins}},
            supports_credentials=True,
        )

    from .api import BLUEPRINTS

    for bp in BLUEPRINTS:
        app.register_blueprint(bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    _register_frontend(app)

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    return app
