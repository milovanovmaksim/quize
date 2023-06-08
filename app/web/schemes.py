from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    """
    Класс schema, представляющий статус ответа на успешный get или post запросы.
    """

    status = fields.Str(dump_default='ok')

    class Meta:
        ordered = True
