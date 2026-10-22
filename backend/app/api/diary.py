from datetime import datetime

from flask import Blueprint, jsonify, request

from ..birthdays import ensure_birthday_events
from ..kinds import EVENT_KINDS
from ..models import Event

bp = Blueprint("diary", __name__, url_prefix="/api/diary")


@bp.get("")
def diary():
    try:
        year = int(request.args.get("year") or datetime.now().year)
    except ValueError:
        return jsonify({"error": "year must be a number"}), 400

    ensure_birthday_events(year)

    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31, 23, 59, 59)
    events = (
        Event.query.filter(Event.kind.in_(EVENT_KINDS))
        .filter(Event.start_date_time.isnot(None))
        .filter((Event.stop_date_time.is_(None)) | (Event.stop_date_time >= start))
        .filter(Event.start_date_time <= end)
        .order_by(Event.start_date_time.desc())
        .all()
    )
    return jsonify({"year": year, "items": [e.to_dict() for e in events]})


@bp.get("/years")
def years():
    current = datetime.now().year
    ensure_birthday_events(current)

    events = (
        Event.query.filter(Event.kind.in_(EVENT_KINDS))
        .filter(Event.start_date_time.isnot(None))
        .order_by(Event.start_date_time.desc())
        .all()
    )

    grouped: dict[int, dict] = {}
    for event in events:
        year = event.start_date_time.year
        entry = grouped.setdefault(year, {"year": year, "count": 0, "cover": None})
        entry["count"] += 1
        if entry["cover"] is None and event.cover:
            entry["cover"] = event.cover.to_dict()

    if current not in grouped:
        grouped[current] = {"year": current, "count": 0, "cover": None}

    ordered = sorted(grouped.values(), key=lambda item: item["year"], reverse=True)
    return jsonify({"items": ordered})
