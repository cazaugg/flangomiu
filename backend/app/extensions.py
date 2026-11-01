import sqlite3

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
cors = CORS()


@event.listens_for(Engine, "connect")
def _configure_sqlite(dbapi_connection, connection_record):
    """Use WAL and wait on locks, so several gunicorn workers can share SQLite."""
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()
