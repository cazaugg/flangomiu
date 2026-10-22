from datetime import date, datetime, time

from .extensions import db
from .models import Event, Person


def ensure_birthday_events(year: int, person: Person | None = None) -> int:
    """Idempotently create real `event_birthday` events for a year.

    Birthdays come from `people.birthday`; each year a real event is created so
    it can carry a description and photos. Returns the number created.
    """
    people = [person] if person is not None else Person.query.filter(Person.birthday.isnot(None)).all()
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31, 23, 59, 59)
    created = 0

    for entry in people:
        birthday = entry.birthday
        if not birthday or birthday.year > year:
            continue

        exists = (
            Event.query.filter(
                Event.kind == "event_birthday",
                Event.start_date_time >= start,
                Event.start_date_time <= end,
                Event.people.any(Person.id == entry.id),
            ).first()
        )
        if exists:
            continue

        try:
            occurrence = date(year, birthday.month, birthday.day)
        except ValueError:
            occurrence = date(year, birthday.month, 28)

        age = year - birthday.year
        event = Event(
            title=f"Geburtstag von {entry.name}",
            kind="event_birthday",
            description=f"{entry.name} wird {age} Jahre alt.",
            all_day=True,
            start_date_time=datetime.combine(occurrence, time.min),
            stop_date_time=datetime.combine(occurrence, time(23, 59)),
            people=[entry],
        )
        db.session.add(event)
        created += 1

    if created:
        db.session.commit()
    return created
