from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from catalog.models import Product, Category
from catalog.schemas import ProductSchema
from db import db
from user.models import User
from user.schemas import UserSchema
from utils.response import BaseResponse


catalog = Blueprint("catalog", url_prefix="/api/v1/user")


@describe(paths="/product", methods="GET")
@protected()
async def get_product(request):
    products = await db.all(Product.query)
    schema = ProductSchema(many=True)
    result = schema.dump(products)
    return result


@describe(paths="/product", methods="POST")
async def add_product(request, username: str, password: str):
    await Product.create(username=username, password=password)
    return BaseResponse().dump({"success": True})


@describe(paths="/categories", methods="GET")
@protected()
async def get_categories(request: Request):
    categories = await Category.query.gino.all()
    schema = CategorySchema(many=True)
    return schema.dump(categories)


add_route(catalog, get_product)
add_route(catalog, add_product)
add_route(catalog, get_categories)
