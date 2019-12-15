from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from project.catalog.models import Product, Category
from project.catalog.schemas import ProductSchema, CategorySchema, NewProductSchema
from project.utils.response import BaseResponse


catalog = Blueprint("catalog", url_prefix="/api/v1")


@describe(paths="/products", methods="GET")
async def get_product(request):
    products = await Product.query.gino.all()
    for product in products:
        product.category = await Category.get(product.category_id)
    schema = ProductSchema(many=True)
    return schema.dump(products)


@describe(paths="/product", methods="POST")
@protected()
async def add_product(request, title: str, description: str, category_id: str):
    category = await Category.get(category_id)
    if not category:
        return BaseResponse().dump({"success": False, "error": "Category don't exist"})
    new_product = await Product.create(title=title, description=description, category_id=category.id)
    return NewProductSchema().dump({"success": True, "product_id": new_product.id})


@describe(paths="/categories", methods="GET")
async def get_categories(request: Request):
    categories = await Category.query.gino.all()
    schema = CategorySchema(many=True)
    return schema.dump(categories)


@describe(paths="/category", methods="POST")
@protected()
async def add_category(request, title: str, description: str):
    new_category = await Category.create(title=title, description=description)
    return NewProductSchema().dump({"success": True, "id": new_category.id})


add_route(catalog, get_product)
add_route(catalog, add_product)
add_route(catalog, add_category)
add_route(catalog, get_categories)
