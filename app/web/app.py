from aiohttp.web import Application

from aiohttp_apispec import setup_aiohttp_apispec
from app.store.database.config import setup_database

from app.web.config import setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


def setup_app(config_path: str) -> Application:
    """
    Создает экземпляр приложения и устанавливает ключевые
    элементы приложения (loger, database, routes, middleware, config).
    Метод вызывается один раз в момент старта приложения.
    Returns: Возвращает экземпляр приложения.
    """

    app = Application()
    setup_logging(app)
    setup_config(app, config_path)
    setup_aiohttp_apispec(app, static_path='/swagger_static',
                          title='quize', url='/docs/json',
                          swagger_path='/docs')
    setup_routes(app)
    setup_middlewares(app)
    setup_database(app)
    return app
