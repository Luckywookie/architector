from marshmallow import Schema, fields, pprint

from project.utils.response import BaseResponse


class CategorySchema(Schema):
    title = fields.String()
    description = fields.String()


class ProductSchema(Schema):
    title = fields.String()
    description = fields.String()
    cost = fields.Float()
    amount = fields.Integer()


class ProductResponse(BaseResponse):
    products = fields.Nested(ProductSchema, many=True)
