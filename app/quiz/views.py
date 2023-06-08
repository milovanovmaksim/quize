from aiohttp_apispec import docs, request_schema, response_schema

from app.quiz.schemes import QuestionResponseSchema, QuestionRequestSchema
from app.web.utils import json_response
from app.web.bases import View
from app.store.quiz.accessor import QuizAccessor


class QuestionListView(View):
    """
    Класс представление для конечной точки "/questions.get.

    Args:
        View (_type_): Базовый класс представление.
    """
    @docs(tags=["quiz"], summary="Get the last saved question")
    @request_schema(QuestionRequestSchema)
    @response_schema(QuestionResponseSchema, 200)
    async def post(self):
        """
        Вью-метод для POST-запроса.
        Метод декорируется "@response_schema", "@docs", "@request_schema" с целью добавления информации о запросе
        в спецификацию Swagger и промежуточное программное обеспечение validation_middleware для валидации данных.

        Returns:
            _type_: Возвращает экземпляр класса aiohttp.web_response.Response.
        """
        quiz_accessor = QuizAccessor(self.request.app)
        count = self.data.get("questions_num", 1)
        question = await quiz_accessor.get_last_question()
        await quiz_accessor.save_questions(count)
        return json_response(data={"question": question if question else {}}, schema=QuestionResponseSchema())
