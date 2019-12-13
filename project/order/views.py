from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from db import db
from order.models import Order
from order.schemas import OrderSchema
from utils.response import BaseResponse


orders = Blueprint("order", url_prefix="/api/v1/order")


@describe(paths="/order", methods="GET")
@protected()
async def get_order(request):
    orders = await db.all(Order.query)
    schema = OrderSchema(many=True)
    result = schema.dump(orders)
    return result


@describe(paths="/order", methods="POST")
async def add_order(request: Request):
    print(request.json)
    await Order.create()
    return BaseResponse().dump({"success": True})


add_route(orders, get_order)
add_route(orders, add_order)
