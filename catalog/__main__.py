from sanic import Sanic
from sanic_jwt import Authentication, Initialize
from sanic_transmute import add_swagger
from catalog.views import catalog
from catalog.db import db

app = Sanic(name='Catalog')


class MyAuthentication(Authentication):
    async def store_refresh_token(self, *args, **kwargs):
        return

    async def retrieve_refresh_token(self, *args, **kwargs):
        return

    async def authenticate(self, *args, **kwargs):
        return

    async def retrieve_user(self, *args, **kwargs):
        return

    def extract_payload(self, request, verify=True, *args, **kwargs):
        return


def setup_auth():
    Initialize(
        app, authentication_class=MyAuthentication, refresh_token_enabled=True
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
    setup_auth()
    app.blueprint(catalog)
    add_swagger(app, '/swagger_json', '/swagger')
    setup_database()
    port = app.config.SERVER_PORT

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        auto_reload=True,
    )