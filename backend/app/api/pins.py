from flask import Blueprint, g, jsonify, request

from ..extensions import db
from ..media import allowed, delete_picture_files, store_picture
from ..models import Pin, Tag
from .auth import write_required

bp = Blueprint("pins", __name__, url_prefix="/api/pins")

TAG_LIMIT = 60


def _payload():
    return request.form if request.form else (request.get_json(silent=True) or {})


def _tag_names(raw) -> list[str]:
    if raw is None:
        return []
    values = raw if isinstance(raw, list) else str(raw).split(",")
    seen = set()
    names = []
    for value in values:
        name = " ".join(str(value).split()).strip()[:TAG_LIMIT].strip()
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        names.append(name)
    return names


def _apply_tags(pin, raw) -> None:
    previous_ids = [tag.id for tag in pin.tags]
    existing = {tag.name.casefold(): tag for tag in Tag.query.all()}
    tags = []
    for name in _tag_names(raw):
        key = name.casefold()
        tag = existing.get(key)
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
            existing[key] = tag
        tags.append(tag)
    pin.tags = tags
    _cleanup_tags(previous_ids)


def _cleanup_tags(tag_ids) -> None:
    if not tag_ids:
        return
    db.session.flush()
    orphans = Tag.query.filter(Tag.id.in_(tag_ids), ~Tag.pins.any()).all()
    for tag in orphans:
        db.session.delete(tag)


def _drop_picture(picture) -> None:
    if not picture:
        return
    delete_picture_files(picture)
    db.session.delete(picture)


def _apply_image(pin, upload_file) -> str | None:
    """Handle upload/replacement/removal. Returns an error message when invalid."""
    remove = str(_payload().get("remove_image") or "").lower() in {"1", "true", "yes"}

    if upload_file and upload_file.filename:
        if not allowed(upload_file.filename):
            return f"unsupported file type: {upload_file.filename}"
        previous = pin.image
        picture = store_picture(upload_file)
        db.session.add(picture)
        pin.image = picture
        db.session.flush()
        _drop_picture(previous)
    elif remove and pin.image:
        previous = pin.image
        pin.image = None
        db.session.flush()
        _drop_picture(previous)

    return None


def _owned_pin(pin_id):
    pin = db.session.get(Pin, pin_id)
    if not pin:
        return None, (jsonify({"error": "not found"}), 404)
    if pin.user_id != g.user.id:
        return None, (jsonify({"error": "only the owner may change this pin"}), 403)
    return pin, None


@bp.get("")
def list_pins():
    pins = Pin.query.order_by(Pin.created_at.desc(), Pin.id.desc()).all()
    return jsonify({"items": [pin.to_dict() for pin in pins]})


@bp.post("")
@write_required
def create_pin():
    data = _payload()
    text = (data.get("text") or "").strip()
    upload_file = request.files.get("file")

    pin = Pin(user_id=g.user.id)
    error = _apply_image(pin, upload_file)
    if error:
        return jsonify({"error": error}), 400
    if not text and not pin.image:
        return jsonify({"error": "text or an image is required"}), 400

    pin.text = text
    pin.author = (data.get("author") or "").strip()[:255]
    _apply_tags(pin, data.get("tags"))
    db.session.add(pin)
    db.session.commit()
    return jsonify({"pin": pin.to_dict()}), 201


@bp.put("/<int:pin_id>")
@write_required
def update_pin(pin_id):
    pin, error = _owned_pin(pin_id)
    if error:
        return error

    data = _payload()
    upload_file = request.files.get("file")
    remove_image = str(data.get("remove_image") or "").lower() in {"1", "true", "yes"}

    text = (data.get("text") or "").strip() if "text" in data else (pin.text or "").strip()
    has_new_file = bool(upload_file and upload_file.filename)
    keeps_image = bool(pin.image_id) and not remove_image
    if not text and not has_new_file and not keeps_image:
        return jsonify({"error": "text or an image is required"}), 400
    if has_new_file and not allowed(upload_file.filename):
        return jsonify({"error": f"unsupported file type: {upload_file.filename}"}), 400

    image_error = _apply_image(pin, upload_file)
    if image_error:
        return jsonify({"error": image_error}), 400

    if "text" in data:
        pin.text = text
    if "author" in data:
        pin.author = (data.get("author") or "").strip()[:255]
    if "tags" in data:
        _apply_tags(pin, data.get("tags"))

    db.session.commit()
    return jsonify({"pin": pin.to_dict()})


@bp.delete("/<int:pin_id>")
@write_required
def delete_pin(pin_id):
    pin, error = _owned_pin(pin_id)
    if error:
        return error

    tag_ids = [tag.id for tag in pin.tags]
    picture = pin.image
    pin.image = None
    db.session.flush()
    _drop_picture(picture)
    db.session.delete(pin)
    _cleanup_tags(tag_ids)
    db.session.commit()
    return jsonify({"ok": True})
