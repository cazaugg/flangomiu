from functools import wraps

from flask import Blueprint, g, jsonify, request, session

from ..extensions import db
from ..models import User

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "authentication required"}), 401
        g.user = user
        return fn(*args, **kwargs)

    return wrapper


def write_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "authentication required"}), 401
        if not user.write_access:
            return jsonify({"error": "write access required"}), 403
        g.user = user
        return fn(*args, **kwargs)

    return wrapper


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401
    session["user_id"] = user.id
    return jsonify({"user": user.to_dict()})


@bp.post("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})


@bp.get("/me")
def me():
    return jsonify({"user": current_user().to_dict() if current_user() else None})
