import aiohttp
from sanic import Blueprint
from sanic.request import Request
from sanic_jwt import protected
from sanic_transmute import add_route
from transmute_core import describe

from project.user.models import User
from project.user.schemas import UserSchema
from project.utils.response import BaseResponse
from project.notifications import send_email, send_telegram


users = Blueprint("user", url_prefix="/api/v1/user")


@describe(paths="/all", methods="GET")
@protected()
async def get_users(request):
    all_users = await User.query.gino.all()
    schema = UserSchema(many=True)
    result = schema.dump(all_users)
    return result


@describe(paths="/register", methods="POST")
async def register(request, username: str, password: str):
    await User.create(username=username, password=password)
    await send_email(recipient=username, message="Congratulation for register")
    await send_telegram(request.app.config.CHAT_ID, message="Congratulation for register")
    return BaseResponse().dump({"success": True})


@describe(paths="/", methods="GET")
@protected()
async def get_user(request: Request):
    user = await User.query.where(User.username == request.args.get("username", None)).gino.first()
    schema = UserSchema()
    return schema.dump(user)


# @describe(paths="/send_email", methods="GET")
# async def send_email(request: Request):
#     url = "http://email:6000/send_email"
#     async with aiohttp.ClientSession().get(url, verify_ssl=False) as response:
#         return await response.json()


add_route(users, get_users)
add_route(users, register)
add_route(users, get_user)
# add_route(users, send_email)
