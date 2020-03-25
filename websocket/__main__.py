from sanic import Sanic
from sanic.request import Request
from sanic.response import json

app = Sanic(name='Websocket')


@app.route("/", methods=['GET'])
async def root(request):
    return json({})


@app.route("/websocket", methods=['POST'])
async def send_email(request: Request):
    pass


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True,
        auto_reload=True,
    )