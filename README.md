# Flagomiu

Familentagebuch und Planung. Frontend auf Deutsch

Features

- Tagebuch: Rückblick auf vergangene Jahre mit Bildern und Beschreibungen
- Wissen: Bereiche mit Markdown-Beiträgen (Rezepte, Administration, Heimnetz)
- Pinwand: Notizen, Zitate und lustige Bilder mit Tags, Suche und Filtern
- Erlebnisse: Ausflüge, Ferien, Feste und Familienprojekte
- Bilder: Fotos mit Beschreibung, Titelbild und Sortierung pro Erlebnis
- Personen: Freunde und Familie, Geburtstage und Jubiläen
- Kalender: Termine, Feste und Ausflüge, primär zur Planung
- Aufgaben: Pflichten und Notwendiges

## Database

Database and code (frontend and backend) in english

- users: pople_id, write_access (bool)
- events: title, kind, description, start_date_time, stop_date_time, cover_picture_id
- pictures: name, path, thumb_path, description
- picture_event: join (+ position für die Reihenfolge)
- people_event: join
- people: name, description, picture, birthday
- pins: user_id, author, text, image_id
- tag: name
- pin_tag: join
- subject: name, description, position
- knowledge: subject_id, title, content (Markdown)

### Event kinds

- event — Erlebnis (allgemein)
- event_excursion — Ausflug
- event_vacation — Ferien
- event_festival — Fest
- event_project — Familienprojekt
- event_birthday — Geburtstag (pro Person und Jahr automatisch angelegt)
- appointment — Termin
- task — Aufgabe (erledigt, sobald die Zeit vorbei ist)

## Backend

- /api/events
- /api/people
- /api/calendar
- /api/tasks
- /api/pins
- /api/knowledge

## Techstack

- SQlite
- Flask
- Vue

Frontend mobile (PWA) and Desktop

## Design

Use flamingo color palette in light red. Avoid makting it too pink/girliy, use more earthy red tones to contrast the light red.

Keep the ux simple and modern. Make the design artistic and beatiful.

## Entwicklung

Aus dem Repo-Root stehen Kurzbefehle bereit (npm leitet sie ins `frontend/` bzw.
`backend/` weiter):

```bash
npm run backend    # Flask-API auf http://localhost:5000
npm run dev        # Vite-Dev-Server auf http://localhost:5173
npm run seed       # Datenbank zurücksetzen und Demo-Daten anlegen
npm run build      # Produktions-Build des Frontends
npm run typecheck  # TypeScript prüfen
npm run test       # Backend-Tests (uv run pytest)
```

Voraussetzung für die Backend-Befehle: [uv](https://docs.astral.sh/uv/) ist
installiert (`pacman -S uv`); die virtuelle Umgebung wird automatisch verwaltet.

Backend und Frontend laufen als zwei Prozesse — also `npm run backend` in einem
Terminal und `npm run dev` in einem zweiten starten.

### Backend (Flask + SQLite)

Abhängigkeiten und virtuelle Umgebung werden mit [uv](https://docs.astral.sh/uv/)
verwaltet (`backend/pyproject.toml` + `backend/uv.lock`):

```bash
cd backend
uv sync                         # .venv anlegen/aktualisieren (inkl. Dev-Abhängigkeiten)
uv run python seed_db.py        # Demo-Daten und Benutzer anlegen
uv run python run.py            # http://localhost:5000
```

Demo-Benutzer: `admin` / `flamingo` (Schreibzugriff) und `gast` / `flamingo` (nur Lesen).

Nach Änderungen an den Abhängigkeiten `uv add <paket>` bzw. `uv add --dev <paket>`
verwenden (statt `pip install`); `uv sync` aktualisiert danach die Umgebung.

Tests:

```bash
cd backend
uv run pytest
```

### Frontend (Vue 3 + Vite + Tailwind)

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173, /api wird auf :5000 geproxied
```

Alternativ aus dem Repo-Root: `npm run dev` (setzt `frontend/node_modules` voraus,
also einmalig `npm install --prefix frontend`).

Weitere Skripte: `npm run build`, `npm run typecheck`, `npm run preview`.

## Projektstruktur

```
backend/    Flask-API, SQLAlchemy-Modelle, Tests
frontend/   Vue 3 + TypeScript + Pinia + Tailwind (PWA)
```

## UI-Komponenten

Wiederverwendbare Bausteine liegen in `frontend/src/components/ui/` und werden in
allen Ansichten verwendet, damit das Design konsistent bleibt:

- `BaseButton`, `BaseIconButton` — Aktionen und Varianten
- `BaseCard`, `BasePageHeader`, `BaseEmptyState` — Layout-Bausteine
- `BaseInput`, `BaseTextarea`, `BaseSelect`, `BaseField` — Formularfelder
- `BaseModal`, `BaseChip`, `SegmentedControl` — Dialoge und Filter
- `BaseBadge`, `KindBadge`, `BaseAvatar`, `BaseSpinner`, `ToastHost` — Feedback
- `ImageUploader`, `PictureGallery`, `ImageLightbox` — Bilder mit Beschreibung und Reihenfolge
- `MarkdownView`, `MarkdownEditor` — Markdown-Darstellung und -Editor (mit Bild-Upload)

Design-Tokens (Flamingo-Palette, Schriften) stehen in `frontend/src/style.css`.