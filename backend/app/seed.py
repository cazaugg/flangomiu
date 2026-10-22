import os
from datetime import date, datetime, timedelta

from flask import current_app

from .extensions import db
from .media import make_thumbnail
from .models import Event, Knowledge, Person, Picture, Pin, Subject, Tag, User, picture_event


def _make_picture(key, color, name, caption):
    """Create a placeholder photo with a thumbnail for the demo diary."""
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    filename = f"seed_{key}.jpg"
    thumb = f"seed_{key}_thumb.jpg"
    path = os.path.join(folder, filename)

    try:
        from PIL import Image, ImageDraw

        image = Image.new("RGB", (1280, 850), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle([36, 36, 1244, 814], outline=(255, 255, 255), width=8)
        draw.text((80, 80), name, fill=(255, 255, 255))
        image.save(path, "JPEG", quality=88)
        make_thumbnail(path, os.path.join(folder, thumb))
    except ImportError:
        pass

    return Picture(name=name, path=filename, thumb_path=thumb, description=caption)


def _attach(event, pictures):
    event.pictures = pictures
    if pictures and event.cover_picture_id is None:
        event.cover_picture_id = pictures[0].id


def _set_positions(event, pictures):
    db.session.flush()
    for index, picture in enumerate(pictures):
        db.session.execute(
            picture_event.update()
            .where(
                (picture_event.c.event_id == event.id)
                & (picture_event.c.picture_id == picture.id)
            )
            .values(position=index)
        )


def seed():
    if User.query.first():
        print("Database already seeded.")
        return

    admin = User(username="admin", write_access=True)
    admin.set_password("flamingo")
    viewer = User(username="gast", write_access=False)
    viewer.set_password("flamingo")
    db.session.add_all([admin, viewer])

    anna = Person(name="Anna", description="Mutter", birthday=date(1985, 4, 12))
    lukas = Person(name="Lukas", description="Vater", birthday=date(1983, 9, 3))
    mia = Person(name="Mia", description="Tochter", birthday=date(2015, 6, 21))
    noah = Person(name="Noah", description="Sohn", birthday=date(2018, 2, 14))
    omi = Person(name="Oma Rosa", description="Grossmutter", birthday=date(1952, 11, 8))
    db.session.add_all([anna, lukas, mia, noah, omi])
    db.session.commit()

    # --- Demo photos -------------------------------------------------------
    ligurien = [
        _make_picture("ligurien1", "#E28A4C", "Strand", "Erster Tag am Meer"),
        _make_picture("ligurien2", "#6E9B6B", "Wanderung", "Durch die Olivenhaine gewandert"),
        _make_picture("ligurien3", "#EE6C5A", "Abendrot", "Sonnenuntergang über dem Meer"),
        _make_picture("ligurien4", "#7C8A5A", "Abendessen", "Gelato am Dorfplatz"),
    ]
    weihnachten = [
        _make_picture("weihnacht1", "#C0556A", "Christbaum", "Der Baum bei Oma"),
        _make_picture("weihnacht2", "#8A6A4F", "Bescherung", "Bescherung am Heiligabend"),
    ]
    umzug = [
        _make_picture("umzug1", "#B5643E", "Leere Zimmer", "Leere Zimmer vor dem Umzug"),
        _make_picture("umzug2", "#D98A5F", "Kartons", "Kisten stapeln sich im Gang"),
    ]
    db.session.add_all(ligurien + weihnachten + umzug)
    db.session.commit()

    # --- Past years (diary) ------------------------------------------------
    umzug_event = Event(
        title="Umzug in die neue Wohnung",
        kind="event_project",
        description="Von der Altstadtwohnung ins Haus am Hang.",
        location="Zürich",
        start_date_time=datetime(2024, 3, 9, 8),
        stop_date_time=datetime(2024, 3, 10, 18),
        people=[anna, lukas],
    )
    _attach(umzug_event, umzug)

    mia_fest = Event(
        title="Mias Geburtstagsfest",
        kind="event_festival",
        description="Kindergeburtstag mit Schatzsuche im Garten.",
        location="Zuhause",
        start_date_time=datetime(2024, 6, 21, 14),
        stop_date_time=datetime(2024, 6, 21, 18),
        people=[mia, anna],
    )

    ferien = Event(
        title="Sommerferien in Ligurien",
        kind="event_vacation",
        description="Zwei Wochen Camping, Strand und viel Gelato.",
        location="Ligurien, Italien",
        all_day=True,
        start_date_time=datetime(2025, 7, 12),
        stop_date_time=datetime(2025, 7, 26),
        people=[anna, lukas, mia, noah],
    )
    _attach(ferien, ligurien)

    weihnacht = Event(
        title="Weihnachtsfest bei Oma",
        kind="event_festival",
        description="Festliches Essen und Bescherung im Kreise der Familie.",
        location="Bei Oma Rosa",
        start_date_time=datetime(2025, 12, 24, 16),
        stop_date_time=datetime(2025, 12, 24, 22),
        people=[anna, lukas, mia, noah, omi],
    )
    _attach(weihnacht, weihnachten)

    # --- Current year (planning) ------------------------------------------
    now = datetime.now()
    zoo = Event(
        title="Ausflug in den Zoo",
        kind="event_excursion",
        description="Ganzer Tag mit Picknick und Tierfütterung.",
        location="Zoo Zürich",
        start_date_time=now + timedelta(days=3, hours=9),
        stop_date_time=now + timedelta(days=3, hours=17),
        people=[mia, noah, anna],
    )
    garten = Event(
        title="Familienprojekt: Garten umgestalten",
        kind="event_project",
        description="Beete neu anlegen und eine Kräuterspirale bauen.",
        location="Zuhause",
        start_date_time=now + timedelta(days=10, hours=10),
        stop_date_time=now + timedelta(days=10, hours=16),
        people=[lukas],
    )
    appointments = [
        Event(
            title="Zahnarzt Mia",
            kind="appointment",
            location="Praxis Dr. Berg",
            start_date_time=now + timedelta(days=5, hours=14),
            stop_date_time=now + timedelta(days=5, hours=15),
            people=[mia],
        ),
        Event(
            title="Elternabend Schule",
            kind="appointment",
            location="Schulhaus Nord",
            start_date_time=now + timedelta(days=12, hours=19),
            stop_date_time=now + timedelta(days=12, hours=21),
            people=[anna, lukas],
        ),
    ]
    tasks = [
        Event(
            title="Müll rausbringen",
            kind="task",
            start_date_time=now - timedelta(days=1, hours=2),
            stop_date_time=now - timedelta(days=1, hours=1),
        ),
        Event(
            title="Reifen wechseln",
            kind="task",
            description="Winterreifen aufziehen lassen.",
            start_date_time=now + timedelta(days=6, hours=8),
            stop_date_time=now + timedelta(days=6, hours=10),
            people=[lukas],
        ),
        Event(
            title="Geburtstagsgeschenk für Oma besorgen",
            kind="task",
            start_date_time=now + timedelta(days=2),
            stop_date_time=now + timedelta(days=2, hours=18),
            people=[anna],
        ),
    ]

    db.session.add_all([umzug_event, mia_fest, ferien, weihnacht, zoo, garten, *appointments, *tasks])
    db.session.commit()

    for event, pictures in ((umzug_event, umzug), (ferien, ligurien), (weihnacht, weihnachten)):
        _set_positions(event, pictures)
    db.session.commit()

    # --- Pinboard ----------------------------------------------------------
    pin_photo = _make_picture("pin_kaffee", "#D98A5F", "Kaffeepause", "Der lustigste Moment des Tages")
    db.session.add(pin_photo)
    db.session.flush()

    tag_names = ["Zitat", "Familie", "Erinnerung", "Mia", "Alltag", "lustig"]
    tag_map = {name: Tag(name=name) for name in tag_names}
    db.session.add_all(tag_map.values())
    db.session.flush()

    db.session.add_all(
        [
            Pin(
                user_id=admin.id,
                author="Lukas",
                text="Wo wir sind, ist vorne.",
                tags=[tag_map["Zitat"], tag_map["Familie"]],
            ),
            Pin(
                user_id=admin.id,
                text="Mia fährt seit heute ohne Stützräder durch den Hof!",
                tags=[tag_map["Erinnerung"], tag_map["Mia"]],
            ),
            Pin(
                user_id=admin.id,
                text="Kaffee, Kuchen und kein Termin.",
                image_id=pin_photo.id,
                tags=[tag_map["Alltag"], tag_map["lustig"]],
            ),
        ]
    )
    db.session.commit()

    # --- Knowledge ---------------------------------------------------------
    recipes = Subject(name="Rezepte", description="Was bei uns auf den Tisch kommt.", position=1)
    administration = Subject(
        name="Administration", description="Versicherungen, Verträge und Papierkram.", position=2
    )
    network = Subject(name="Heimnetz", description="Router, Geräte und Zugänge.", position=3)
    db.session.add_all([recipes, administration, network])
    db.session.flush()

    db.session.add_all(
        [
            Knowledge(
                subject_id=recipes.id,
                title="Omas Apfelkuchen",
                content="""# Omas Apfelkuchen

Ein Blechkuchen, wie ihn Oma Rosa backt.

## Zutaten

- 500 g Äpfel
- 250 g Mehl
- 125 g Butter
- 100 g Zucker
- 2 Eier
- 1 Päckchen Backpulver
- Zimt nach Geschmack

## Zubereitung

1. Äpfel schälen und in Spalten schneiden.
2. Butter, Zucker und Eier cremig rühren.
3. Mehl mit Backpulver mischen und unterheben.
4. Teig in eine gefettete Form geben, Äpfel darauf verteilen.
5. Bei 180 °C etwa 40 Minuten backen.

> Am besten lauwarm mit einem Klecks Sahne.
""",
            ),
            Knowledge(
                subject_id=recipes.id,
                title="Schnelle Tomatensauce",
                content="""## Zutaten

- 1 Dose Pelati
- 1 Knoblauchzehe
- Olivenöl
- Basilikum

## Zubereitung

Knoblauch in Olivenöl andünsten, Pelati dazugeben und 20 Minuten köcheln lassen.
Mit Basilikum, Salz und Pfeffer abschmecken.
""",
            ),
            Knowledge(
                subject_id=network.id,
                title="WLAN und Router",
                content="""# Heimnetz

## Router

- Modell: *Fritz!Box*
- Adresse: `192.168.178.1`
- WLAN: **Familie-5G**

## Geräte

| Gerät | IP | Notiz |
| --- | --- | --- |
| NAS | 192.168.178.20 | Fotos und Backups |
| Drucker | 192.168.178.30 | Obergeschoss |

## Backups

Das NAS sichert die Fotos jeden Sonntag auf die externe Platte.
""",
            ),
            Knowledge(
                subject_id=administration.id,
                title="Wichtige Dokumente",
                content="""# Wichtige Dokumente

- Versicherungen: Ordner im Schrank, rechte Seite
- Steuerunterlagen: digital im NAS unter `/admin/steuern`
- Passkopien: verschlüsselt im Passwortmanager

**Hinweis:** Bei Adressänderungen alle Verträge aktualisieren.
""",
            ),
        ]
    )
    db.session.commit()

    # Real birthday events for the current year.
    from .birthdays import ensure_birthday_events

    ensure_birthday_events(now.year)

    print("Seeded demo data. Login: admin / flamingo (write) or gast / flamingo (read).")
