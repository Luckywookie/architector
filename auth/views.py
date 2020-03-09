import aiohttp
from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from auth.models import User
from auth.schemas import UserSchema
from auth.utils.response import BaseResponse
from auth.notifications import send_email, send_telegram


users = Blueprint("user", url_prefix="/api/v1/user")


@describe(paths="/register", methods="POST", tags=['User'])
async def register(request, username: str, password: str):
    await User.create(username=username, password=password)
    message = f"Congratulation for register, {username}"
    await send_email(request.app.config, recipient=username, message=message)
    # await send_telegram(request.app.config, message=message)
    return BaseResponse().dump({"success": True})


@describe(paths="/", methods="GET", tags=['User'])
@protected()
async def get_user(request: Request):
    user = await User.query.where(User.username == request.args.get("username", None)).gino.first()
    schema = UserSchema()
    return schema.dump(user)


add_route(users, register)
add_route(users, get_user)
