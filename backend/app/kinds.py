"""Event kind definitions shared across the API."""

# Erlebnis kinds (diary, calendar, gallery-capable)
EVENT_KINDS = [
    "event",
    "event_excursion",
    "event_vacation",
    "event_festival",
    "event_project",
    "event_birthday",
]

# Every kind that is persisted as an event row.
STORED_KINDS = EVENT_KINDS + ["appointment", "task"]
