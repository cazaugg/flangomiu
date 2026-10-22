import io

from app.models import User


def login(client, username="admin"):
    return client.post("/api/auth/login", json={"username": username, "password": "pw"})


def png_bytes(color="#EE6C5A"):
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (24, 24), color).save(buffer, "PNG")
    buffer.seek(0)
    return buffer


def test_health(client):
    assert client.get("/api/health").status_code == 200


def test_write_requires_auth(client):
    assert client.post("/api/events", json={"title": "X"}).status_code == 401


def test_viewer_cannot_write(client):
    login(client, "viewer")
    assert client.post("/api/events", json={"title": "X"}).status_code == 403


def test_create_and_list_event(client):
    login(client)
    response = client.post("/api/events", json={"title": "Zoo", "kind": "event_excursion"})
    assert response.status_code == 201
    assert response.get_json()["event"]["kind"] == "event_excursion"
    items = client.get("/api/events?kind=events").get_json()["items"]
    assert [item["title"] for item in items] == ["Zoo"]


def test_task_completion_is_derived_from_time(client):
    login(client)
    client.post("/api/tasks", json={"title": "Alt", "stop": "2000-01-01T00:00:00"})
    client.post("/api/tasks", json={"title": "Neu", "stop": "2999-01-01T00:00:00"})
    items = client.get("/api/tasks?status=all").get_json()["items"]
    by_title = {item["title"]: item for item in items}
    assert by_title["Alt"]["is_done"] is True
    assert by_title["Neu"]["is_done"] is False

    open_items = client.get("/api/tasks?status=open").get_json()["items"]
    assert [item["title"] for item in open_items] == ["Neu"]


def test_diary_generates_real_birthday_events(client):
    login(client)
    client.post("/api/people", json={"name": "Mia", "birthday": "2015-06-21"})
    items = client.get("/api/diary?year=2026").get_json()["items"]
    birthdays = [item for item in items if item["kind"] == "event_birthday"]
    assert len(birthdays) == 1
    assert birthdays[0]["title"] == "Geburtstag von Mia"
    assert birthdays[0]["start"][:10] == "2026-06-21"

    # Idempotent: a second call creates nothing new.
    again = client.get("/api/diary?year=2026").get_json()["items"]
    assert len([i for i in again if i["kind"] == "event_birthday"]) == 1


def test_diary_years_reports_covers(client):
    login(client)
    event = client.post(
        "/api/events",
        json={"title": "Ferien", "kind": "event_vacation", "start": "2025-07-12T00:00:00"},
    ).get_json()["event"]
    client.post(
        f"/api/events/{event['id']}/pictures",
        data={"files": [(png_bytes(), "strand.png")]},
        content_type="multipart/form-data",
    )
    years = client.get("/api/diary/years").get_json()["items"]
    assert any(entry["cover"] for entry in years)


def test_event_images_upload_caption_reorder_delete(client):
    login(client)
    event = client.post("/api/events", json={"title": "Zoo"}).get_json()["event"]

    uploaded = client.post(
        f"/api/events/{event['id']}/pictures",
        data={"files": [(png_bytes(), "a.png"), (png_bytes("#6E9B6B"), "b.png")]},
        content_type="multipart/form-data",
    )
    assert uploaded.status_code == 201
    pictures = uploaded.get_json()["event"]["pictures"]
    assert len(pictures) == 2

    first_id = pictures[0]["id"]
    caption = client.patch(f"/api/pictures/{first_id}", json={"description": "Am Eingang"})
    assert caption.get_json()["picture"]["description"] == "Am Eingang"

    client.put(
        f"/api/events/{event['id']}/pictures/order",
        json={"picture_ids": [pictures[1]["id"], first_id]},
    )
    reordered = client.get(f"/api/events/{event['id']}").get_json()["event"]["pictures"]
    assert [p["id"] for p in reordered] == [pictures[1]["id"], first_id]

    client.delete(f"/api/events/{event['id']}/pictures/{first_id}")
    remaining = client.get(f"/api/events/{event['id']}").get_json()["event"]["pictures"]
    assert [p["id"] for p in remaining] == [pictures[1]["id"]]


def test_delete_person_removes_birthday_events(client):
    login(client)
    person = client.post("/api/people", json={"name": "Anna", "birthday": "1990-01-05"}).get_json()["person"]
    assert client.get("/api/diary?year=2026").get_json()["items"]
    client.delete(f"/api/people/{person['id']}")
    remaining = [i for i in client.get("/api/diary?year=2026").get_json()["items"] if i["kind"] == "event_birthday"]
    assert remaining == []


def test_pin_requires_text_or_image(client):
    login(client)
    response = client.post(
        "/api/pins",
        data={"author": "Nur ein Name"},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_pin_tags_ownership_and_permissions(app, client):
    login(client)
    created = client.post(
        "/api/pins",
        data={"text": "Wo wir sind, ist vorne.", "author": "Lukas", "tags": "Zitat, Familie, zitat"},
        content_type="multipart/form-data",
    )
    assert created.status_code == 201
    pin = created.get_json()["pin"]
    assert pin["user"]["username"] == "admin"
    assert [tag["name"] for tag in pin["tags"]] == ["Familie", "Zitat"]

    login(client, "editor")
    other = client.post(
        "/api/pins",
        data={"text": "Auch ein Zitat", "tags": "familie"},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    assert [tag["name"] for tag in other["tags"]] == ["Familie"]
    assert client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "Fremd"},
        content_type="multipart/form-data",
    ).status_code == 403
    assert client.delete(f"/api/pins/{pin['id']}").status_code == 403

    login(client, "viewer")
    assert client.get("/api/pins").status_code == 200
    assert (
        client.post(
            "/api/pins",
            data={"text": "Nur Lesen"},
            content_type="multipart/form-data",
        ).status_code
        == 403
    )

    login(client)
    updated = client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "Wo wir sind, ist vorne!", "tags": "Erinnerung"},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    assert updated["text"] == "Wo wir sind, ist vorne!"
    assert [tag["name"] for tag in updated["tags"]] == ["Erinnerung"]

    with app.app_context():
        from app.models import Tag

        assert Tag.query.filter_by(name="Zitat").first() is None
        assert Tag.query.filter_by(name="Familie").first() is not None


def test_pin_image_upload_replace_remove_and_delete(app, client):
    login(client)
    pin = client.post(
        "/api/pins",
        data={"text": "Bild-Pin", "file": (png_bytes(), "pin.png")},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    assert pin["image"] is not None
    picture_id = pin["image"]["id"]
    assert client.get(f"/api/pictures/{picture_id}/file").status_code == 200

    # An invalid update must not remove the existing image file.
    invalid = client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "", "remove_image": "1"},
        content_type="multipart/form-data",
    )
    assert invalid.status_code == 400
    assert client.get(f"/api/pictures/{picture_id}/file").status_code == 200

    replacement = client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "Neues Bild", "file": (png_bytes("#6E9B6B"), "neu.png")},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    assert replacement["image"]["id"] != picture_id
    assert client.get(f"/api/pictures/{picture_id}/file").status_code == 404
    new_picture_id = replacement["image"]["id"]

    removed = client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "Ohne Bild", "remove_image": "1"},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    assert removed["image"] is None
    assert client.get(f"/api/pictures/{new_picture_id}/file").status_code == 404

    with_image = client.put(
        f"/api/pins/{pin['id']}",
        data={"text": "Wieder mit Bild", "file": (png_bytes(), "zurueck.png")},
        content_type="multipart/form-data",
    ).get_json()["pin"]
    last_picture_id = with_image["image"]["id"]
    assert client.delete(f"/api/pins/{pin['id']}").status_code == 200
    assert client.get(f"/api/pictures/{last_picture_id}/file").status_code == 404
    assert client.get("/api/pins").get_json()["items"] == []


def test_people_crud(client):
    login(client)
    created = client.post("/api/people", json={"name": "Anna"}).get_json()["person"]
    client.put(f"/api/people/{created['id']}", json={"name": "Anna M."})
    items = client.get("/api/people").get_json()["items"]
    assert items[0]["name"] == "Anna M."
    assert client.delete(f"/api/people/{created['id']}").status_code == 200
    assert client.get("/api/people").get_json()["items"] == []
