import re
from functools import wraps

from typing import Callable, Dict, List, Optional, Union, get_type_hints

from sanic import Sanic
from sanic_transmute.handler import extract_params
from sanic.response import HTTPResponse
from transmute_core import default_context, describe, TransmuteFunction, TransmuteContext
from sanic_transmute.swagger import get_swagger_spec, _add_blueprint_specs

from auth.utils.response import BaseResponse


class Route:

    def __init__(
        self,
        app_or_blueprint: Sanic,
        ignore = None,
        auth: bool = False,
        # scope: Scopes = None,
        context: TransmuteContext = default_context,
        **kwargs,
    ):
        self.app = app_or_blueprint
        self.ignore = ignore
        self.auth = auth
        # self.scope = scope
        self.context = context
        self.kwargs = kwargs

    @staticmethod
    def _convert_to_sanic_path(path: str, annotations: dict) -> str:
        """
        convert based on route syntax.
        """
        path = path.replace('{', '<').replace('}', '>')
        vars = re.findall('<(.*?)>', path)
        for var in vars:
            var_type = annotations[var]
            # if isinstance(var_type, ObjectIdType):
            #     path = path.replace(var, f'{var}:[a-fA-F0-9]{{24}}')
        return path

    def bind_to_swagger(self, func) -> TransmuteFunction:
        ignore = self.ignore

        args_to_ignore = ['request']
        if ignore:
            args_to_ignore += [ignore] if isinstance(ignore, str) else ignore

        transmute_func = TransmuteFunction(func, args_not_from_request=args_to_ignore)
        if ignore:
            for arg in transmute_func.signature.args:
                if arg.name in ignore:
                    transmute_func.signature.args.remove(arg)
        get_swagger_spec(self.app).add_func(transmute_func, self.context)
        print('paths:', transmute_func.paths)
        return transmute_func

    def describe_func(self, func, **kwargs):
        if self.auth:
            kwargs.setdefault('header_parameters', []).append('authorization')
            kwargs.setdefault('parameter_descriptions', {}).update({'authorization': r'Cookie: jwt=access token'})
            response_types = kwargs.setdefault('response_types', {})
            # response_types.update({401: {'description': 'Authentication failed', 'type': BaseResponse}})
        return describe(**kwargs)(func)

    def create_handler(self, transmute_func: TransmuteFunction):
        """Sanic_transmute's refactored create_handler:
         Does not catch any exception. We raise exception and pass it to Sanic where handle it.
        """
        DEFAULT_HTTP_CONTENT_TYPE = "application/octet-stream"

        @wraps(transmute_func.raw_func)
        async def handler(request, *args, **kwargs):
            exc, result = None, None
            args, kwargs = await extract_params(request, self.context, transmute_func)
            result = await transmute_func.raw_func(*args, **kwargs)
            content_type = request.headers.get("Content-Type", DEFAULT_HTTP_CONTENT_TYPE)
            response = transmute_func.process_result(self.context, result, exc, content_type)
            return HTTPResponse(
                status=response["code"],
                content_type=response["content-type"],
                headers=response["headers"],
                body_bytes=response["body"],
            )

        handler.transmute_func = transmute_func
        return handler

    # def add_scope_into_handler(self, handler):
    #     scope = [name.lower() for name, value in Scopes.__members__.items() if value in self.scope]
    #     return scoped(scope, require_all=False)(handler)

    def __call__(self, func: Callable) -> Callable:
        func = self.describe_func(func, **self.kwargs)
        transmute_func = self.bind_to_swagger(func)
        handler = self.create_handler(transmute_func)
        # if self.scope:
        #     handler = self.add_scope_into_handler(handler)
        for path in transmute_func.paths:
            sanic_path = self._convert_to_sanic_path(path, get_type_hints(func))
            self.app.add_route(handler, sanic_path, methods=list(transmute_func.methods))
        return handler


route = Route
