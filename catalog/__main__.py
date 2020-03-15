import aiohttp
from sanic import Sanic
from sanic_jwt import Authentication, Initialize
from sanic_transmute import add_swagger
from catalog.views import catalog
from catalog.db import db


app = Sanic(name='Catalog')


class MyAuthentication(Authentication):
    my_token = None

    async def store_refresh_token(self, *args, **kwargs):
        return

    async def retrieve_refresh_token(self, *args, **kwargs):
        return

    async def authenticate(self, *args, **kwargs):
        print('authenticate')
        request = {'username': 'test-user', 'password': 'test-password'}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    'http://auth:8001/api/v1/auth',
                    json=request,
                    verify_ssl=False,
                    timeout=10
            ) as response:
                res = await response.json()
                self.my_token = res['access_token']
                return res

    async def generate_access_token(self,  *args, **kwargs):
        print('generate_access_token')
        return self.my_token

    async def retrieve_user(self, *args, **kwargs):
        print('retrieve_user', self.my_token)
        headers = {'Authorization': f'Bearer {self.my_token}'}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'http://auth:8001/api/v1/auth/me',
                    verify_ssl=False,
                    timeout=10,
                    headers=headers
            ) as response:
                res = await response.json()
                return res['me']

    # async def is_authenticated(self, *args, **kwargs):
    #     result = await self.retrieve_user()
    #     return bool(result.get('me'))

    def extract_payload(self, request, verify=True, *args, **kwargs):
        return


def setup_auth():
    Initialize(
        app,
        authentication_class=MyAuthentication,
        refresh_token_enabled=True,
        url_prefix='/api/v1/auth',
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