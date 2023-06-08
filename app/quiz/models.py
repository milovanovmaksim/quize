from dataclasses import field
from typing import Type, ClassVar

from marshmallow_dataclass import dataclass
from marshmallow import Schema as MarshmallowSchema, EXCLUDE

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.store.database.sqlalchemy_base import db


@dataclass
class Question:
    """Data класс, описывающий ответ на get-запрос к ресурсу https://jservice.io/api/random?count=1
    В классе определены магические методы __hash__, __eq__ для возможности хэшироания и сравнения объетов этого класса.
    """
    id: int
    title: str = field(metadata={"data_key": "question"})
    created_at: str
    answer: str

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    Schema: ClassVar[Type[MarshmallowSchema]] = MarshmallowSchema

    class Meta:
        unknown = EXCLUDE


class QuestionModel(db):
    """
    Класс, отображающий вопросы в таблице "qustions" базы данных.

    Args:
        id: ндентификатор записи.
        title: текст вопроса.
        created_at: время создания записи.
        answe: текст ответа.
    """
    __tablename__ = "questions"
    id = Column(Integer(), primary_key=True)
    jservice_id = Column(Integer(), nullable=False)
    title = Column(String(), nullable=False)
    created_at = Column(DateTime())
    answer = Column(String(), nullable=False)
