from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from catalog.models import Product, Category
from catalog.schemas import ProductSchema, CategorySchema, NewProductSchema
from catalog.utils.response import BaseResponse


catalog = Blueprint("catalog", url_prefix="/api/v1")


@describe(paths="/products", methods="GET", tags=['Catalog'])
async def get_product(request):
    products = await Product.query.gino.all()
    for product in products:
        product.category = await Category.get(product.category_id)
    schema = ProductSchema(many=True)
    return schema.dump(products)


@describe(paths="/product", methods="POST", tags=['Catalog'])
@protected()
async def add_product(request):
    category = await Category.get(request.json['category_id'])
    if not category:
        return BaseResponse().dump({"success": False, "error": "Category don't exist"})
    new_product = await Product.create(
        title=request.json['title'],
        description=request.json['description'],
        category_id=category.id
    )
    return NewProductSchema().dump({"success": True, "id": new_product.id})


@describe(paths="/product", methods="DELETE", tags=['Catalog'])
@protected()
async def delete_product(request):
    await Product.delete.where(Product.id == request.json['id']).gino.status()
    return BaseResponse().dump({"success": True})


@describe(paths="/categories", methods="GET", tags=['Catalog'])
async def get_categories(request: Request):
    categories = await Category.query.gino.all()
    schema = CategorySchema(many=True)
    return schema.dump(categories)


@describe(paths="/category", methods="POST", tags=['Catalog'])
@protected()
async def add_category(request):
    new_category = await Category.create(title=request.json['title'], description=request.json['description'])
    return NewProductSchema().dump({"success": True, "id": new_category.id})


@describe(paths="/category", methods="DELETE", tags=['Catalog'])
@protected()
async def delete_category(request):
    await Category.delete.where(Category.id == request.json['id']).gino.status()
    return BaseResponse().dump({"success": True})


add_route(catalog, get_product)
add_route(catalog, add_product)
add_route(catalog, delete_product)
add_route(catalog, add_category)
add_route(catalog, get_categories)
add_route(catalog, delete_category)
