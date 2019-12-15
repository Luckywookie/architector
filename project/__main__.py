from sanic import Sanic
from sanic_transmute import add_swagger
from sanic_jwt import Initialize

from project.db import db

from project.catalog.views import catalog
from project.order.views import orders
from project.user.views import users

from project.utils.auth import authenticate, setup_docs, Logout, auth_stub, refresh_stub, me_stub, auth_verify_stub

app = Sanic(load_env=False)


def setup_database():
    # app.config.DB_HOST = 'postgres'
    app.config.DB_HOST = 'localhost'
    app.config.DB_DATABASE = 'sanic_postgres'
    app.config.DB_USER = 'test_user'
    app.config.DB_PASSWORD = 'pwd0123456789'
    # app.config.DB_ECHO = True

    db.init_app(app)

    jwt_funcs = {
        Logout.post: {
            'path': 'logout',
            'methods': 'POST',
            'auth': True,
        },
        auth_stub: {
            'path': '',
            'methods': 'POST',
        },
        refresh_stub: {
            'path': 'refresh',
            'methods': 'POST',
            'auth': True,
            'header_parameters': ['refresh_token'],
            'parameter_descriptions': {
                'refresh_token': 'Cookie: refresh_token=refresh token'
            },
        },
        me_stub: {
            'path': 'me',
            'methods': 'GET',
            'auth': True,
        },
        auth_verify_stub: {
            'path': 'verify',
            'methods': 'GET',
            'auth': True,
            'ignore': 'runner',
        },
    }

    for func, kwargs in jwt_funcs.items():
        setup_docs(app, func, **kwargs)

    Initialize(app, authenticate=authenticate, url_prefix='/api/v1/auth')

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await db.gino.create_all()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        # await db.gino.drop_all()
        pass


if __name__ == "__main__":
    app.blueprint(users)
    app.blueprint(catalog)
    app.blueprint(orders)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()

    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True,
        auto_reload=True,
    )