from marshmallow import Schema, fields, pprint


class BaseResponse(Schema):
    success = fields.Boolean()
