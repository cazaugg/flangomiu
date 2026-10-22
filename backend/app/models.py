import re
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db

picture_event = db.Table(
    "picture_event",
    db.Column("picture_id", db.Integer, db.ForeignKey("picture.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
    db.Column("position", db.Integer, default=0),
)

people_event = db.Table(
    "people_event",
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
)

pin_tag = db.Table(
    "pin_tag",
    db.Column("pin_id", db.Integer, db.ForeignKey("pin.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    thumb_path = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description or "",
            "url": f"/api/pictures/{self.id}/file",
            "thumb": f"/api/pictures/{self.id}/thumb",
        }


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    birthday = db.Column(db.Date, nullable=True)
    picture_id = db.Column(db.Integer, db.ForeignKey("picture.id"), nullable=True)
    picture = db.relationship("Picture", foreign_keys=[picture_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description or "",
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "picture": self.picture.to_dict() if self.picture else None,
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    kind = db.Column(db.String(32), nullable=False, default="event")
    description = db.Column(db.Text, default="")
    location = db.Column(db.String(255), default="")
    start_date_time = db.Column(db.DateTime, nullable=True)
    stop_date_time = db.Column(db.DateTime, nullable=True)
    all_day = db.Column(db.Boolean, default=False)
    cover_picture_id = db.Column(db.Integer, db.ForeignKey("picture.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    cover = db.relationship("Picture", foreign_keys=[cover_picture_id])
    people = db.relationship("Person", secondary=people_event, backref="events")
    pictures = db.relationship(
        "Picture",
        secondary=picture_event,
        backref="events",
        order_by=picture_event.c.position,
    )

    @property
    def is_done(self):
        ref = self.stop_date_time or self.start_date_time
        return bool(ref and ref < datetime.now())

    def to_dict(self):
        pictures = [pic.to_dict() for pic in self.pictures]
        return {
            "id": self.id,
            "title": self.title,
            "kind": self.kind,
            "description": self.description or "",
            "location": self.location or "",
            "start": self.start_date_time.isoformat() if self.start_date_time else None,
            "stop": self.stop_date_time.isoformat() if self.stop_date_time else None,
            "all_day": bool(self.all_day),
            "is_done": self.is_done,
            "cover": self.cover.to_dict() if self.cover else None,
            "picture_count": len(pictures),
            "people": [p.to_dict() for p in self.people],
            "pictures": pictures,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    write_access = db.Column(db.Boolean, default=False)

    person = db.relationship("Person")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "write_access": bool(self.write_access),
            "person": self.person.to_dict() if self.person else None,
        }

    def summary(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.person.name if self.person else self.username,
        }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.Column(db.String(255), default="")
    text = db.Column(db.Text, default="")
    image_id = db.Column(db.Integer, db.ForeignKey("picture.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship("User")
    image = db.relationship("Picture", foreign_keys=[image_id])
    tags = db.relationship("Tag", secondary=pin_tag, backref="pins", order_by=Tag.name)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author or "",
            "text": self.text or "",
            "image": self.image.to_dict() if self.image else None,
            "tags": [tag.to_dict() for tag in self.tags],
            "user": self.user.summary() if self.user else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    position = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    entries = db.relationship(
        "Knowledge",
        backref="subject",
        cascade="all, delete-orphan",
        order_by="Knowledge.updated_at.desc()",
    )

    def to_dict(self, with_entries=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description or "",
            "position": self.position or 0,
            "entry_count": len(self.entries),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if with_entries:
            data["entries"] = [entry.to_dict(summary=True) for entry in self.entries]
        return data


class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def excerpt(self, length=200):
        text = re.sub(r"[#>*_`\[\]()!|~\-]+", " ", self.content or "")
        text = re.sub(r"\s+", " ", text).strip()
        return text[:length] + ("…" if len(text) > length else "")

    def to_dict(self, summary=False):
        data = {
            "id": self.id,
            "subject_id": self.subject_id,
            "title": self.title,
            "excerpt": self.excerpt(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if summary:
            data["subject_name"] = self.subject.name if self.subject else ""
        else:
            data["content"] = self.content or ""
            data["subject"] = self.subject.to_dict() if self.subject else None
        return data
