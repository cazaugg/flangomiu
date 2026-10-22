from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Event
from .auth import write_required
from .events import apply_payload

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _tasks():
    return (
        Event.query.filter_by(kind="task")
        .order_by(Event.stop_date_time.is_(None), Event.stop_date_time)
        .all()
    )


@bp.get("")
def list_tasks():
    status = request.args.get("status", "all")
    items = [t.to_dict() for t in _tasks()]
    if status == "open":
        items = [t for t in items if not t["is_done"]]
    elif status == "done":
        items = [t for t in items if t["is_done"]]
    return jsonify({"items": items})


@bp.post("")
@write_required
def create_task():
    data = request.get_json(silent=True) or {}
    if not (data.get("title") or "").strip():
        return jsonify({"error": "title is required"}), 400
    task = Event(kind="task")
    apply_payload(task, data)
    task.kind = "task"
    db.session.add(task)
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 201


@bp.put("/<int:task_id>")
@write_required
def update_task(task_id):
    task = db.session.get(Event, task_id)
    if not task or task.kind != "task":
        return jsonify({"error": "not found"}), 404
    apply_payload(task, request.get_json(silent=True) or {})
    task.kind = "task"
    db.session.commit()
    return jsonify({"task": task.to_dict()})


@bp.delete("/<int:task_id>")
@write_required
def delete_task(task_id):
    task = db.session.get(Event, task_id)
    if not task or task.kind != "task":
        return jsonify({"error": "not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"ok": True})
