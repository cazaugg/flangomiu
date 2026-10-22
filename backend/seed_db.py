from app import create_app
from app.extensions import db
from app.seed import seed

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    seed()
