from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from db import db
from user.models import User
from user.schemas import UserSchema
from utils.response import BaseResponse


users = Blueprint("user", url_prefix="/api/v1/user")


@describe(paths="/all", methods="GET")
@protected()
async def get_users(request):
    all_users = await db.all(User.query)
    schema = UserSchema(many=True)
    result = schema.dump(all_users)
    return result


@describe(paths="/register", methods="POST")
async def register(request, username: str, password: str):
    await User.create(username=username, password=password)
    return BaseResponse().dump({"success": True})


@describe(paths="/", methods="GET")
@protected()
async def get_user(request: Request):
    user = await User.query.where(User.username == request.args.get("username", None)).gino.first()
    schema = UserSchema()
    return schema.dump(user)


add_route(users, get_users)
add_route(users, register)
add_route(users, get_user)
