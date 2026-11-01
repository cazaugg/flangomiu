"""Create the initial users from environment variables, without demo data.

This is safe to run on every container start: existing users are never
modified, nothing is dropped, and nothing runs unless a password is provided.

Usage:
    ADMIN_USERNAME=admin ADMIN_PASSWORD=... python -m app.bootstrap

Optional read-only account:
    GUEST_USERNAME=gast GUEST_PASSWORD=...
"""

import os
import sys

from . import create_app
from .extensions import db
from .models import User

MIN_PASSWORD_LENGTH = 8


def _env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def _ensure_user(username: str, password: str, write_access: bool) -> bool:
    """Create the user when missing. Returns True when a user was created."""
    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        print(f"bootstrap: user '{username}' already exists, left unchanged")
        return False

    if len(password) < MIN_PASSWORD_LENGTH:
        raise SystemExit(
            f"bootstrap: password for '{username}' must be at least "
            f"{MIN_PASSWORD_LENGTH} characters"
        )

    user = User(username=username, write_access=write_access)
    user.set_password(password)
    db.session.add(user)
    print(
        f"bootstrap: created user '{username}' "
        f"({'write' if write_access else 'read-only'} access)"
    )
    return True


def bootstrap() -> int:
    admin_username = _env("ADMIN_USERNAME") or "admin"
    admin_password = _env("ADMIN_PASSWORD")
    guest_username = _env("GUEST_USERNAME")
    guest_password = _env("GUEST_PASSWORD")

    if not admin_password and not guest_password:
        print("bootstrap: no ADMIN_PASSWORD/GUEST_PASSWORD set, nothing to do")
        return 0

    app = create_app()
    with app.app_context():
        db.create_all()
        created = False
        if admin_password:
            created |= _ensure_user(admin_username, admin_password, write_access=True)
        else:
            print("bootstrap: ADMIN_PASSWORD not set, no admin account created")
        if guest_password:
            created |= _ensure_user(
                guest_username or "gast", guest_password, write_access=False
            )
        if created:
            db.session.commit()
    return 0


if __name__ == "__main__":
    sys.exit(bootstrap())
