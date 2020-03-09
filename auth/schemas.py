from marshmallow import Schema, fields, pprint

from auth.utils.response import BaseResponse


class UserSchema(Schema):
    username = fields.String()


class UsersResponse(BaseResponse):
    users = fields.Nested(UserSchema, many=True)
