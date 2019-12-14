from marshmallow import Schema, fields, pprint

from project.utils.response import BaseResponse


class OrderProductsSchema(Schema):
    title = fields.String()
    description = fields.String()


class NewOrderSchema(Schema):
    id = fields.Integer()


class OrderSchema(NewOrderSchema):
    total_cost = fields.Float()
    total_amount = fields.Integer()
    delivery = fields.Float()
    products = fields.Nested(OrderProductsSchema, many=True)


class OrderResponse(BaseResponse):
    orders = fields.Nested(OrderSchema, many=True)
