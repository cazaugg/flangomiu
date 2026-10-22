from .auth import bp as auth_bp
from .calendar import bp as calendar_bp
from .diary import bp as diary_bp
from .events import bp as events_bp
from .knowledge import bp as knowledge_bp
from .people import bp as people_bp
from .pictures import bp as pictures_bp
from .pins import bp as pins_bp
from .tasks import bp as tasks_bp

BLUEPRINTS = [
    auth_bp,
    events_bp,
    people_bp,
    calendar_bp,
    diary_bp,
    tasks_bp,
    pictures_bp,
    pins_bp,
    knowledge_bp,
]
