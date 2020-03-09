from sanic import Sanic
from sanic_jwt import Initialize
from sanic_transmute import add_swagger
from auth.views import users
from auth.db import db
from auth.utils.auth import authenticate

app = Sanic(name='Auth')


def setup_database():
    db.init_app(app)

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
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()
    port = app.config.SERVER_PORT

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        auto_reload=True,
    )