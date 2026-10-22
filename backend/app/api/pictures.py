from flask import Blueprint, abort, current_app, jsonify, request, send_from_directory

from ..extensions import db
from ..media import allowed, delete_picture_files, store_picture
from ..models import Picture
from .auth import write_required

bp = Blueprint("pictures", __name__, url_prefix="/api/pictures")


@bp.get("")
def list_pictures():
    pictures = Picture.query.order_by(Picture.id.desc()).all()
    return jsonify({"items": [p.to_dict() for p in pictures]})


def _send(relative_path):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], relative_path)


@bp.get("/<int:picture_id>/file")
def file(picture_id):
    picture = db.session.get(Picture, picture_id)
    if not picture:
        abort(404)
    return _send(picture.path)


@bp.get("/<int:picture_id>/thumb")
def thumb(picture_id):
    picture = db.session.get(Picture, picture_id)
    if not picture:
        abort(404)
    return _send(picture.thumb_path or picture.path)


@bp.post("")
@write_required
def upload():
    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400
    upload_file = request.files["file"]
    if not upload_file.filename or not allowed(upload_file.filename):
        return jsonify({"error": "unsupported file type"}), 400
    picture = store_picture(
        upload_file,
        name=request.form.get("name"),
        description=request.form.get("description") or "",
    )
    db.session.add(picture)
    db.session.commit()
    return jsonify({"picture": picture.to_dict()}), 201


@bp.patch("/<int:picture_id>")
@write_required
def update_picture(picture_id):
    picture = db.session.get(Picture, picture_id)
    if not picture:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True) or {}
    if "name" in data:
        picture.name = (data.get("name") or "").strip() or picture.name
    if "description" in data:
        picture.description = data.get("description") or ""
    db.session.commit()
    return jsonify({"picture": picture.to_dict()})


@bp.delete("/<int:picture_id>")
@write_required
def delete_picture(picture_id):
    picture = db.session.get(Picture, picture_id)
    if not picture:
        return jsonify({"error": "not found"}), 404
    delete_picture_files(picture)
    db.session.delete(picture)
    db.session.commit()
    return jsonify({"ok": True})
