from typing import List, Set, Optional
from datetime import datetime
from asyncio import gather, create_task, Task

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select
from sqlalchemy.sql.functions import max as sa_max

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Question, QuestionModel
from app.store.jservice.jservice_accessor import JserviceAccessor


class QuizAccessor(BaseAccessor):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, args, kwargs)
        self.count_saved_questions: int = 0

    async def save_questions(self, count: int):
        """
        Сохраняет необходимое количество "count" уникальных вопросов,
        полученных с ресурса "https://jservice.io/api/random?count={count}", в БД.
        Args:
            count(int): количество уникальных вопросов, которые необходимо записать в БД.

        """
        jservice: JserviceAccessor = JserviceAccessor(self.app)
        while self.count_saved_questions != count:
            remainder = count - self.count_saved_questions
            unique_questions: Set[Question] = set(await jservice.get_questions(remainder))
            await self._create_questions(unique_questions)

    async def _create_questions(self, questions: Set[Question]):
        """
        Конкурентно записывает множество уникальных вопросов "questions" викторины в БД.
        Args:
            questions (Set[Question]): Множество уникальных вопросов, которые необходимо записать в БД.
        """
        tasks: List[Task] = []
        for question in questions:
            tasks.append(create_task(self._create_question(question)))
        await gather(*tasks)

    async def _create_question(self, question: Question) -> Optional[QuestionModel]:
        """Записывает вопрос в БД.

        Args:
            question (Question): Вопрос, который необходимо записать в БД.

        Returns:
            Optional[QuestionModel]: Если запись прошла успешно, возвращает QuestionModel, иначе None.
        """
        saved_question = await self._get_question_by_id(question.id)
        if not saved_question:
            question_model = QuestionModel(
                jservice_id=question.id,
                title=question.title,
                answer=question.answer,
                created_at=datetime.strptime(question.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),)
            async with self.app["database"].session() as session:
                session.add(question_model)
                await session.commit()
                self.count_saved_questions += 1
            return question_model

    async def _get_question_by_id(self, id: int) -> Optional[QuestionModel]:
        """Возвращает вопрос из БД по идентификатору записи.

        Args:
            id (int): Идентификатор записи в БД.

        Returns:
            Optional[QuestionModel]: Возвращает QuestionModel если такая запись существует, иначе None.
        """
        query: Select = select(QuestionModel).where(QuestionModel.id == id)
        async with self.app["database"].session() as session:
            result: Result = await session.execute(query)
            question_model = result.unique().scalar_one_or_none()
        if question_model:
            return question_model
        return None

    async def get_last_question(self) -> Optional[Question]:
        """
        Отправляет запрос к БД и возвращает последний сохраненный вопрос.

        Returns:
            Optional[QuestionModel]: Возвращает QuestionModel если такая запись существует, иначе None.
        """
        sub_query: Select = select(sa_max(QuestionModel.id)).scalar_subquery()
        query: Select = (select(QuestionModel).where(QuestionModel.id == sub_query))
        async with self.app["database"].session() as session:
            result: Result = await session.execute(query)
            last = result.unique().scalar_one_or_none()
        if last:
            response = Question(id=last.id,
                                answer=last.answer,
                                title=last.title,
                                created_at=last.created_at)
            return response
        return None
