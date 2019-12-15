from sanic import Sanic
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_jwt import exceptions, BaseEndpoint
from transmute_core import default_context, describe, TransmuteFunction
from sanic_transmute.swagger import get_swagger_spec, _add_blueprint_specs

from project.user.models import User
from project.utils.response import BaseResponse


class Logout(BaseEndpoint, HTTPMethodView):
    """Custom sanic-jwt Auth endpoint"""

    async def post(self, request: Request, user, authorization: str = None, **__):
        pass


def auth_stub(username: str, password: str, merchant_id: str = None):
    """
    Generate a pair of access and refresh tokens
    To generate merchant token, pass `merchant_id` field and use test credentials: `merch` and `passwd`.
    """


def auth_verify_stub(authorization: str = None):
    """Check whether or not a given access token is valid"""


def me_stub(authorization: str = None):
    """Retrieve information about the currently authenticated user"""


def refresh_stub(refresh_token: str = None, authorization: str = None):
    """
    Ask for a new access token given an existing refresh token
    Do not forget to supply an existing access token, even if it is expired.
    """


def modify_path(path):
    prefix = '/api/v1/'
    return f"{prefix.rstrip('/')}/{path.lstrip('/')}".rstrip('/')


def describe_func(func, auth: bool = False, **kwargs):
    if auth:
        kwargs.setdefault('header_parameters', []).append('authorization')
        kwargs.setdefault('parameter_descriptions', {}).update({'authorization': r'Cookie: jwt=access token'})
        response_types = kwargs.setdefault('response_types', {})
        response_types.update({401: {'description': 'Authentication failed', 'type': str}})
    return describe(**kwargs)(func)


def bind_to_swagger(app: Sanic, func, context, ignore: bool = None):
    args_to_ignore = ["request"]
    if ignore:
        args_to_ignore += [ignore] if isinstance(ignore, str) else ignore

    transmute_func = TransmuteFunction(func, args_not_from_request=args_to_ignore)
    if ignore:
        for arg in transmute_func.signature.args:
            if arg.name in ignore:
                transmute_func.signature.args.remove(arg)
    get_swagger_spec(app).add_func(transmute_func, context)
    return transmute_func


def setup_docs(app: Sanic, func, path='', auth=None, context=default_context, **kwargs):
    ignore = kwargs.get('ignore')
    if ignore:
        del kwargs['ignore']
    func = describe_func(func, auth, tags=['Auth'], paths=modify_path(path), **kwargs)
    bind_to_swagger(app, func, context, ignore=ignore)


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
