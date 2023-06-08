import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BaseAccessor:
    """
    Базовый класс accessor.
    Класс accessor - это сущность, которая умеет обращаться к сторонним источникам данных,
    умеет преобразовать полученные данные в нужный вид.
    Например, можно сделать accessor для доступа к PostgreSQL или к внешнему API.
    Также, accessor обычно умеет выполнять подключение и отключение от внешнего источника данных.
    Args:
        app: Экземпляр класса Aplication.
        database: Экземпляр класса Database.

    """
    def __init__(self, app: "Application", *args, **kwargs):
        self.app = app

