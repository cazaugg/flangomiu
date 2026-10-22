import pytest

from app import create_app
from app.config import Config
from app.extensions import db
from app.models import User


@pytest.fixture
def app(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path / 'test.db'}"
        UPLOAD_FOLDER = str(tmp_path / "uploads")

    application = create_app(TestConfig)
    with application.app_context():
        admin = User(username="admin", write_access=True)
        admin.set_password("pw")
        viewer = User(username="viewer", write_access=False)
        viewer.set_password("pw")
        editor = User(username="editor", write_access=True)
        editor.set_password("pw")
        db.session.add_all([admin, viewer, editor])
        db.session.commit()
        yield application
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()
