import typing
from dataclasses import dataclass

from app.store.database.config import setup_config as setup_db_config

if typing.TYPE_CHECKING:
    from app.web.app import Application
    from app.store.database.config import DatabaseConfig


@dataclass
class Config:
    """
    Класс, содержащий настройки ключевых элементов приложения.
    """
    database: "DatabaseConfig"


def setup_config(app: "Application", config_path: str):
    """
    Конфигурирует приложения.

    Args:
        app (Application): Экземпляр класса Application
        config_path (str): Путь к конфигурационному файлу.
    """

    database_config = setup_db_config(config_path)
    app["config"] = Config(database=database_config)
