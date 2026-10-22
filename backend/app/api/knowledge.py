from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from ..extensions import db
from ..models import Knowledge, Subject
from .auth import login_required, write_required

bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")


def _subject_payload(subject, data):
    if "name" in data:
        subject.name = (data.get("name") or "").strip()
    if "description" in data:
        subject.description = data.get("description") or ""
    if "position" in data:
        try:
            subject.position = int(data.get("position") or 0)
        except (TypeError, ValueError):
            subject.position = 0


# --- Subjects --------------------------------------------------------------


@bp.get("/subjects")
@login_required
def list_subjects():
    subjects = Subject.query.order_by(Subject.position, Subject.name).all()
    return jsonify({"items": [subject.to_dict() for subject in subjects]})


@bp.post("/subjects")
@write_required
def create_subject():
    data = request.get_json(silent=True) or {}
    if not (data.get("name") or "").strip():
        return jsonify({"error": "name is required"}), 400
    subject = Subject()
    _subject_payload(subject, data)
    db.session.add(subject)
    db.session.commit()
    return jsonify({"subject": subject.to_dict()}), 201


@bp.get("/subjects/<int:subject_id>")
@login_required
def get_subject(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "not found"}), 404
    return jsonify({"subject": subject.to_dict(with_entries=True)})


@bp.put("/subjects/<int:subject_id>")
@write_required
def update_subject(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True) or {}
    if "name" in data and not (data.get("name") or "").strip():
        return jsonify({"error": "name is required"}), 400
    _subject_payload(subject, data)
    db.session.commit()
    return jsonify({"subject": subject.to_dict()})


@bp.delete("/subjects/<int:subject_id>")
@write_required
def delete_subject(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "not found"}), 404
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"ok": True})


# --- Entries ---------------------------------------------------------------


@bp.get("/entries")
@login_required
def list_entries():
    query = Knowledge.query

    subject_id = request.args.get("subject_id")
    if subject_id:
        try:
            query = query.filter(Knowledge.subject_id == int(subject_id))
        except ValueError:
            return jsonify({"error": "subject_id must be a number"}), 400

    term = (request.args.get("q") or "").strip()
    if term:
        like = f"%{term}%"
        query = query.filter(
            or_(Knowledge.title.ilike(like), Knowledge.content.ilike(like))
        )

    entries = query.order_by(Knowledge.updated_at.desc(), Knowledge.id.desc()).all()
    return jsonify({"items": [entry.to_dict(summary=True) for entry in entries]})


@bp.get("/entries/<int:entry_id>")
@login_required
def get_entry(entry_id):
    entry = db.session.get(Knowledge, entry_id)
    if not entry:
        return jsonify({"error": "not found"}), 404
    return jsonify({"entry": entry.to_dict()})


def _apply_entry_payload(entry, data):
    if "title" in data:
        entry.title = (data.get("title") or "").strip()
    if "content" in data:
        entry.content = data.get("content") or ""
    if "subject_id" in data:
        entry.subject_id = data.get("subject_id")


@bp.post("/entries")
@write_required
def create_entry():
    data = request.get_json(silent=True) or {}
    if not (data.get("title") or "").strip():
        return jsonify({"error": "title is required"}), 400
    try:
        subject_id = int(data.get("subject_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "subject_id is required"}), 400
    if not db.session.get(Subject, subject_id):
        return jsonify({"error": "unknown subject"}), 400

    entry = Knowledge(subject_id=subject_id)
    _apply_entry_payload(entry, data)
    db.session.add(entry)
    db.session.commit()
    return jsonify({"entry": entry.to_dict()}), 201


@bp.put("/entries/<int:entry_id>")
@write_required
def update_entry(entry_id):
    entry = db.session.get(Knowledge, entry_id)
    if not entry:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True) or {}
    if "title" in data and not (data.get("title") or "").strip():
        return jsonify({"error": "title is required"}), 400
    if "subject_id" in data:
        try:
            subject_id = int(data.get("subject_id"))
        except (TypeError, ValueError):
            return jsonify({"error": "subject_id is required"}), 400
        if not db.session.get(Subject, subject_id):
            return jsonify({"error": "unknown subject"}), 400
    _apply_entry_payload(entry, data)
    db.session.commit()
    return jsonify({"entry": entry.to_dict()})


@bp.delete("/entries/<int:entry_id>")
@write_required
def delete_entry(entry_id):
    entry = db.session.get(Knowledge, entry_id)
    if not entry:
        return jsonify({"error": "not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"ok": True})
