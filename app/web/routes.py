from typing import TYPE_CHECKING

from app.quiz.routes import setup_routes as quiz_setup_routes


if TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    """
    Устанавливает конечные точки веб-приложения.
    """

    quiz_setup_routes(app)
