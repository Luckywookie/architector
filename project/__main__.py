from sanic import Sanic
from sanic_transmute import add_swagger
from sanic_jwt import Initialize

from project.db import db
from user.views import bp
from utils.auth import authenticate

app = Sanic(load_env=False)


def setup_database():
    app.config.DB_HOST = 'postgres'
    app.config.DB_DATABASE = 'sanic_postgres'
    app.config.DB_USER = 'test_user'
    app.config.DB_PASSWORD = 'pwd0123456789'
    # app.config.DB_ECHO = True

    db.init_app(app)
    Initialize(app, authenticate=authenticate, url_prefix='/api/v1/auth')

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await db.gino.create_all()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await db.gino.drop_all()


if __name__ == "__main__":
    app.blueprint(bp)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()

    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True,
        auto_reload=True,
    )