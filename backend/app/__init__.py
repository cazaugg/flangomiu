import os

from flask import Flask, jsonify

from .config import Config
from .extensions import cors, db


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
    )

    from .api import BLUEPRINTS

    for bp in BLUEPRINTS:
        app.register_blueprint(bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    return app
