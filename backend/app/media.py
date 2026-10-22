import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from .models import Picture

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
THUMBNAIL_SIZE = (640, 640)


def allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _upload_dir() -> str:
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    return folder


def make_thumbnail(source: str, destination: str) -> bool:
    """Generate a small JPEG thumbnail. Returns False when Pillow is unavailable."""
    try:
        from PIL import Image
    except ImportError:
        return False
    try:
        with Image.open(source) as image:
            image = image.convert("RGB")
            image.thumbnail(THUMBNAIL_SIZE)
            image.save(destination, "JPEG", quality=82)
        return True
    except Exception:
        return False


def store_picture(file, name: str | None = None, description: str = "") -> Picture:
    """Persist an uploaded file (plus thumbnail) and return an unsaved Picture."""
    extension = file.filename.rsplit(".", 1)[1].lower()
    identifier = uuid.uuid4().hex
    stored_name = f"{identifier}.{extension}"
    thumb_name = f"{identifier}_thumb.jpg"

    folder = _upload_dir()
    original_path = os.path.join(folder, stored_name)
    file.save(original_path)

    thumb_path = os.path.join(folder, thumb_name)
    if not make_thumbnail(original_path, thumb_path):
        thumb_name = stored_name

    return Picture(
        name=name or secure_filename(file.filename),
        path=stored_name,
        thumb_path=thumb_name,
        description=description or "",
    )


def delete_picture_files(picture: Picture) -> None:
    folder = _upload_dir()
    for relative in {picture.path, picture.thumb_path}:
        if not relative:
            continue
        try:
            os.remove(os.path.join(folder, relative))
        except OSError:
            pass
