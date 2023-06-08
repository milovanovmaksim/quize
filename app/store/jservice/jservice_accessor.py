from typing import Any, List

from aiohttp import ClientResponse, ClientSession

from marshmallow.exceptions import ValidationError
from marshmallow import Schema


from app.base.base_accessor import BaseAccessor
from app.quiz.models import Question


class JserviceAccessorException(Exception):
    def __init__(self, response: ClientResponse, content: Any):
        self.response = response
        self.content = content


class JserviceAccessor(BaseAccessor):
    """
    Класс для доступа к данным ресурса https://jservice.io/api/random?count={count}
    """
    BASE_PATH = "https://jservice.io/api/random?count={count}"

    async def get_questions(self, count: int) -> List[Question]:
        """
        Отправляет get-запрос на ресурс "https://jservice.io/api/random?count={count}".

        Args:
            count (int): Количество вопросов, необходимое получить с ресурса https://jservice.io/api/random?count={count}.

        Returns:
            List[Question]: Список вопросов.
        """
        async with ClientSession() as session:
            url = JserviceAccessor.BASE_PATH.format(count=count)
            async with session.get(url) as response:
                await self.check_status_200(response)
                questions = set(await self.load_data(response))
                return questions

    async def check_status_200(self, resp: ClientResponse):
        """
        Проверяет статус ответа.
        """
        if resp.status != 200:
            raise JserviceAccessorException(resp, await resp.text())

    async def load_data(self, response: ClientResponse) -> List[Question]:
        """
        Загружает данные из ответа "response" в List[Question].
        Args:
            response (ClientResponse): ответ, полученый с ресурса https://jservice.io/api/random?count={count}.
            List[Question]: Список вопросов.
        """
        schema: Schema = Question.Schema()
        questions: List[Question]
        data = await response.json()
        try:
            questions: List[Question] = [schema.load(question) for question in data]  # type: ignore
        except ValidationError as e:
            raise JserviceAccessorException(response, e.messages)
        return questions
