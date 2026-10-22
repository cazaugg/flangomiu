from datetime import date, datetime

from flask import Blueprint, jsonify, request

from ..birthdays import ensure_birthday_events
from ..kinds import EVENT_KINDS
from ..models import Event, Person

bp = Blueprint("calendar", __name__, url_prefix="/api/calendar")

CALENDAR_KINDS = ["appointment"] + EVENT_KINDS


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


@bp.get("")
def calendar():
    start = parse_date(request.args.get("start"))
    end = parse_date(request.args.get("end"))
    if not start or not end:
        return jsonify({"error": "start and end dates are required"}), 400

    for year in range(start.year, end.year + 1):
        ensure_birthday_events(year)

    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())

    events = (
        Event.query.filter(Event.kind.in_(CALENDAR_KINDS))
        .filter((Event.stop_date_time.is_(None)) | (Event.stop_date_time >= start_dt))
        .filter(Event.start_date_time <= end_dt)
        .all()
    )
    items = [e.to_dict() for e in events]
    items.sort(key=lambda item: item["start"] or "")
    return jsonify({"items": items})
