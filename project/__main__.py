from sanic import Sanic, Blueprint, response
from sanic.response import json
from sanic_transmute import describe, add_route, add_swagger, APIException
from sanic_jwt import Initialize, exceptions
from sanic.request import Request
from sanic_jwt.decorators import protected

from project.db import db
from project.user.models import User
from project.user.schemas import UserSchema, UsersResponse
from project.utils.response import BaseResponse


async def authenticate(request: Request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await User.query.where(User.username == username).gino.first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


app = Sanic(load_env=False)
bp = Blueprint("test_blueprints", url_prefix="/api/v2")

Initialize(app, authenticate=authenticate, url_prefix='/api/v1/auth')


def setup_database():
    app.config.DB_HOST = 'postgres'
    app.config.DB_DATABASE = 'sanic_postgres'
    app.config.DB_USER = 'test_user'
    app.config.DB_PASSWORD = 'pwd0123456789'
    # app.config.DB_ECHO = True

    db.init_app(app)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await db.gino.create_all()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await db.gino.create_all()


@describe(paths="/api/v1/users", methods="GET")
@protected()
async def get_users(request):
    all_users = await db.all(User.query)
    schema = UserSchema(many=True)
    result = schema.dump(all_users)
    return result


@describe(paths="/api/v1/register", methods="POST")
async def register(request, username: str, password: str):
    await User.create(username=username, password=password)
    return BaseResponse().dump({"success": True})


@describe(paths="/api/v1/user", methods="GET")
@protected()
async def get_user(request: Request):
    user = await User.query.where(User.username == request.args.get("username", None)).gino.first()
    schema = UserSchema()
    return schema.dump(user)


@describe(paths="/multiply")
async def get_blueprint_params(request, left: int, right: int) -> str:
    """
    API Description: Multiply, left * right. This will show in the swagger page (localhost:8000/api/v1/).
    """
    res = left * right
    return "{left}*{right}={res}".format(left=left, right=right, res=res)


if __name__ == "__main__":
    add_route(app, get_users)
    add_route(app, register)
    add_route(app, get_user)
    add_route(bp, get_blueprint_params)
    app.blueprint(bp)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()

    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True,
        auto_reload=True,
    )