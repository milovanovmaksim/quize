from typing import TYPE_CHECKING

from app.quiz.views import QuestionListView


if TYPE_CHECKING:
    from aiohttp.web import Application


def setup_routes(app: "Application"):
    """
    Устанавливает конечную точку /questions.get.
    """
    app.router.add_view("/questions.get", QuestionListView)
