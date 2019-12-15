from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from project.order.models import Order, OrderProducts
from project.order.schemas import OrderSchema, NewOrderSchema


orders = Blueprint("order", url_prefix="/api/v1/order")


@describe(paths="/all", methods="GET")
@protected()
async def get_orders(request: Request):
    # order_id = request.args.get("order_id", None)
    orders = await Order.query.gino.all()
    schema = OrderSchema(many=True)
    result = schema.dump(orders)
    return result


@describe(paths="/", methods="GET")
@protected()
async def get_order_by_id(request: Request):
    order_id = request.args.get("order_id", None)
    order = await Order.get(order_id)
    return OrderSchema().dump(order)


@describe(paths="/", methods="POST")
@protected()
async def add_order(request: Request):
    # print(request.json)
    data = request.json
    products = data.pop("products")
    new_order = await Order.create(**data)
    for product in products:
        await OrderProducts.create(order_id=new_order.id, id=product["id"])
    return NewOrderSchema().dump({"success": True, "id": new_order.id})


add_route(orders, get_orders)
add_route(orders, get_order_by_id)
add_route(orders, add_order)
