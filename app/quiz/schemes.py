from marshmallow import Schema, fields
from marshmallow.validate import Range


from app.web.schemes import OkResponseSchema


class QuestionSchema(Schema):
    """
    Кдасс Schema для вопроса.
    """
    id = fields.Int()
    title = fields.Str()
    created_at = fields.Str()
    answer = fields.Str()

    class Meta:
        ordered = True


class QuestionRequestSchema(Schema):
    """
    Класс Schema представляет тело POST-запроса для конечной точки /questions.get.

    Args:
        Schema (_type_): Колическво вопросов, необходимое получить с ресурса https://jservice.io/api/random?count=questions_num
    """
    questions_num = fields.Int(required=True, validate=Range(min=1, max=100))


class QuestionResponseSchema(OkResponseSchema):
    """
    Класс Schema представляет ответ на POST-запроса для конечной точки /questions.get.
    """
    question = fields.Nested(QuestionSchema)
