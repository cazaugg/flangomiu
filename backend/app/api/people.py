from datetime import date, datetime

from flask import Blueprint, jsonify, request

from ..birthdays import ensure_birthday_events
from ..extensions import db
from ..models import Person
from .auth import write_required

bp = Blueprint("people", __name__, url_prefix="/api/people")


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def apply_payload(person, data):
    if "name" in data:
        person.name = (data.get("name") or "").strip()
    if "description" in data:
        person.description = data.get("description") or ""
    if "birthday" in data:
        person.birthday = parse_date(data.get("birthday"))
    if "picture_id" in data:
        person.picture_id = data.get("picture_id")


@bp.get("")
def list_people():
    people = Person.query.order_by(Person.name).all()
    return jsonify({"items": [p.to_dict() for p in people]})


@bp.get("/<int:person_id>")
def get_person(person_id):
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({"error": "not found"}), 404
    data = person.to_dict()
    data["events"] = [e.to_dict() for e in person.events]
    return jsonify({"person": data})


@bp.post("")
@write_required
def create_person():
    data = request.get_json(silent=True) or {}
    if not (data.get("name") or "").strip():
        return jsonify({"error": "name is required"}), 400
    person = Person()
    apply_payload(person, data)
    db.session.add(person)
    db.session.commit()

    if person.birthday:
        ensure_birthday_events(datetime.now().year, person=person)

    return jsonify({"person": person.to_dict()}), 201


@bp.put("/<int:person_id>")
@write_required
def update_person(person_id):
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({"error": "not found"}), 404
    apply_payload(person, request.get_json(silent=True) or {})
    db.session.commit()
    return jsonify({"person": person.to_dict()})


@bp.delete("/<int:person_id>")
@write_required
def delete_person(person_id):
    person = db.session.get(Person, person_id)
    if not person:
        return jsonify({"error": "not found"}), 404
    for event in list(person.events):
        if event.kind == "event_birthday":
            db.session.delete(event)
    db.session.delete(person)
    db.session.commit()
    return jsonify({"ok": True})
