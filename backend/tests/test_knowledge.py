def login(client, username="admin"):
    return client.post("/api/auth/login", json={"username": username, "password": "pw"})


def make_subject(client, name="Rezepte"):
    response = client.post("/api/knowledge/subjects", json={"name": name})
    assert response.status_code == 201
    return response.get_json()["subject"]


def test_knowledge_requires_login(client):
    assert client.get("/api/knowledge/subjects").status_code == 401
    assert client.get("/api/knowledge/entries").status_code == 401


def test_viewer_can_read_but_not_write(client):
    login(client, "viewer")
    assert client.get("/api/knowledge/subjects").status_code == 200
    assert client.post("/api/knowledge/subjects", json={"name": "X"}).status_code == 403


def test_subject_and_entry_crud(client):
    login(client)
    subject = make_subject(client)
    assert subject["entry_count"] == 0

    created = client.post(
        "/api/knowledge/entries",
        json={"subject_id": subject["id"], "title": "Apfelkuchen", "content": "# Kuchen"},
    )
    assert created.status_code == 201
    entry = created.get_json()["entry"]
    assert entry["subject"]["name"] == "Rezepte"

    listed = client.get(f"/api/knowledge/entries?subject_id={subject['id']}").get_json()["items"]
    assert [item["title"] for item in listed] == ["Apfelkuchen"]
    assert listed[0]["excerpt"]

    updated = client.put(
        f"/api/knowledge/entries/{entry['id']}", json={"content": "# Neu"}
    ).get_json()["entry"]
    assert updated["content"] == "# Neu"

    detail = client.get(f"/api/knowledge/subjects/{subject['id']}").get_json()["subject"]
    assert detail["entry_count"] == 1
    assert detail["entries"][0]["title"] == "Apfelkuchen"


def test_entry_requires_valid_subject(client):
    login(client)
    assert (
        client.post(
            "/api/knowledge/entries", json={"title": "X", "subject_id": 999}
        ).status_code
        == 400
    )
    assert client.post("/api/knowledge/entries", json={"title": "X"}).status_code == 400
    assert client.post("/api/knowledge/entries", json={"subject_id": 1}).status_code == 400


def test_search_filters_title_and_content(client):
    login(client)
    subject = make_subject(client)
    client.post(
        "/api/knowledge/entries",
        json={"subject_id": subject["id"], "title": "WLAN", "content": "Router und Modem"},
    )
    client.post(
        "/api/knowledge/entries",
        json={"subject_id": subject["id"], "title": "Kuchen", "content": "Mehl und Zucker"},
    )

    by_title = client.get("/api/knowledge/entries?q=wlan").get_json()["items"]
    assert [item["title"] for item in by_title] == ["WLAN"]

    by_content = client.get("/api/knowledge/entries?q=router").get_json()["items"]
    assert [item["title"] for item in by_content] == ["WLAN"]


def test_delete_subject_cascades_entries(client):
    login(client)
    subject = make_subject(client)
    entry = client.post(
        "/api/knowledge/entries",
        json={"subject_id": subject["id"], "title": "Beitrag"},
    ).get_json()["entry"]

    assert client.delete(f"/api/knowledge/subjects/{subject['id']}").status_code == 200
    assert client.get(f"/api/knowledge/entries/{entry['id']}").status_code == 404
    assert client.get("/api/knowledge/subjects").get_json()["items"] == []


def test_unknown_subject_is_404(client):
    login(client)
    assert client.get("/api/knowledge/subjects/999").status_code == 404
