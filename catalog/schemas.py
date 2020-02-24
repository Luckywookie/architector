from marshmallow import Schema, fields, pprint

from project.utils.response import BaseResponse


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()


class NewProductSchema(BaseResponse):
    id = fields.Integer()


class ProductSchema(NewProductSchema):
    title = fields.String()
    description = fields.String()
    cost = fields.Float()
    amount = fields.Integer()
    category = fields.Nested(CategorySchema, only=['title'])


class ProductResponse(BaseResponse):
    products = fields.Nested(ProductSchema, many=True)
