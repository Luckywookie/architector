from sanic import Sanic
from sanic_jwt import Initialize
from sanic_transmute import add_swagger
from auth.views import users
from auth.db import db
from auth.utils.auth import authenticate, Logout, auth_stub, refresh_stub, me_stub, auth_verify_stub, setup_docs, \
    retrieve_user

app = Sanic(name='Auth')


def init_auth():
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

    Initialize(
        app,
        authenticate=authenticate,
        class_views=(("/logout", Logout),),
        url_prefix='/api/v1/auth',
        path_to_retrieve_user='/me',
        retrieve_user=retrieve_user,
    )


def setup_database():
    db.init_app(app)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await db.gino.create_all()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        # await db.gino.drop_all()
        pass


if __name__ == "__main__":
    init_auth()
    app.blueprint(users)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()
    port = app.config.SERVER_PORT

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        auto_reload=True,
    )