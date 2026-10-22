from flask import Blueprint, jsonify, request

from ..extensions import db
from ..kinds import EVENT_KINDS, STORED_KINDS
from ..media import allowed, delete_picture_files, store_picture
from ..models import Event, Person, Picture, picture_event
from ..parsing import parse_dt
from .auth import write_required

bp = Blueprint("events", __name__, url_prefix="/api/events")


def _resolve_kinds(raw: str):
    if not raw:
        return None
    if raw in ("event", "events"):
        return EVENT_KINDS
    return [kind for kind in raw.split(",") if kind in STORED_KINDS]


def apply_payload(event, data):
    if "title" in data:
        event.title = (data.get("title") or "").strip()
    if "kind" in data and data.get("kind") in STORED_KINDS:
        event.kind = data["kind"]
    for field in ("description", "location"):
        if field in data:
            setattr(event, field, data.get(field) or "")
    if "start" in data:
        event.start_date_time = parse_dt(data.get("start"))
    if "stop" in data:
        event.stop_date_time = parse_dt(data.get("stop"))
    if "all_day" in data:
        event.all_day = bool(data.get("all_day"))
    if "cover_picture_id" in data:
        cover_id = data.get("cover_picture_id")
        event.cover_picture_id = cover_id if cover_id else None
    if "people_ids" in data:
        ids = data.get("people_ids") or []
        event.people = Person.query.filter(Person.id.in_(ids)).all() if ids else []
    if "picture_ids" in data:
        ids = data.get("picture_ids") or []
        event.pictures = Picture.query.filter(Picture.id.in_(ids)).all() if ids else []


def _append_picture(event, picture, position):
    event.pictures.append(picture)
    db.session.flush()
    db.session.execute(
        picture_event.update()
        .where(
            (picture_event.c.event_id == event.id) & (picture_event.c.picture_id == picture.id)
        )
        .values(position=position)
    )


@bp.get("")
def list_events():
    query = Event.query
    kinds = _resolve_kinds(request.args.get("kind"))
    if kinds is not None:
        query = query.filter(Event.kind.in_(kinds))
    start = parse_dt(request.args.get("from"))
    end = parse_dt(request.args.get("to"))
    if start:
        query = query.filter((Event.stop_date_time.is_(None)) | (Event.stop_date_time >= start))
    if end:
        query = query.filter(Event.start_date_time <= end)
    events = query.order_by(Event.start_date_time.is_(None), Event.start_date_time.desc()).all()
    return jsonify({"items": [e.to_dict() for e in events]})


@bp.get("/<int:event_id>")
def get_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "not found"}), 404
    return jsonify({"event": event.to_dict()})


@bp.post("")
@write_required
def create_event():
    data = request.get_json(silent=True) or {}
    if not (data.get("title") or "").strip():
        return jsonify({"error": "title is required"}), 400
    event = Event(kind="event")
    apply_payload(event, data)
    db.session.add(event)
    db.session.commit()
    return jsonify({"event": event.to_dict()}), 201


@bp.put("/<int:event_id>")
@write_required
def update_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "not found"}), 404
    apply_payload(event, request.get_json(silent=True) or {})
    db.session.commit()
    return jsonify({"event": event.to_dict()})


@bp.delete("/<int:event_id>")
@write_required
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"ok": True})


@bp.post("/<int:event_id>/pictures")
@write_required
def upload_event_pictures(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "not found"}), 404

    files = request.files.getlist("files")
    if not files and "file" in request.files:
        files = [request.files["file"]]
    files = [f for f in files if f and f.filename]
    if not files:
        return jsonify({"error": "no files provided"}), 400

    position = len(event.pictures)
    for upload_file in files:
        if not allowed(upload_file.filename):
            return jsonify({"error": f"unsupported file type: {upload_file.filename}"}), 400
        picture = store_picture(upload_file, description=request.form.get("description") or "")
        db.session.add(picture)
        _append_picture(event, picture, position)
        if event.cover_picture_id is None:
            event.cover_picture_id = picture.id
        position += 1

    db.session.commit()
    return jsonify({"event": event.to_dict()}), 201


@bp.delete("/<int:event_id>/pictures/<int:picture_id>")
@write_required
def remove_event_picture(event_id, picture_id):
    event = db.session.get(Event, event_id)
    picture = db.session.get(Picture, picture_id)
    if not event or not picture or picture not in event.pictures:
        return jsonify({"error": "not found"}), 404

    event.pictures.remove(picture)
    if event.cover_picture_id == picture.id:
        event.cover_picture_id = None
    db.session.flush()

    if not picture.events:
        delete_picture_files(picture)
        db.session.delete(picture)

    db.session.commit()
    return jsonify({"event": event.to_dict()})


@bp.put("/<int:event_id>/pictures/order")
@write_required
def reorder_event_pictures(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "not found"}), 404
    ids = (request.get_json(silent=True) or {}).get("picture_ids") or []
    for index, picture_id in enumerate(ids):
        db.session.execute(
            picture_event.update()
            .where(
                (picture_event.c.event_id == event_id)
                & (picture_event.c.picture_id == int(picture_id))
            )
            .values(position=index)
        )
    db.session.commit()
    return jsonify({"event": event.to_dict()})
