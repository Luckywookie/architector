from sanic import Sanic
from sanic_transmute import add_swagger
from project.db import db
from project.order.views import orders

app = Sanic(name='Market')


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
    app.blueprint(orders)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()

    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True,
        auto_reload=True,
    )