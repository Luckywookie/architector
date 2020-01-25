import aiohttp
from sanic import Sanic
from sanic.response import json

app = Sanic(name='Push')


@app.route("/", methods=['GET'])
async def root(request):
    return json({})


@app.route("/send_push", methods=['POST'])
async def send_push(request):
    chat_id = request.json.get("chat_id")
    message = request.json.get("message")
    bot_token = app.config.BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}"
    req = f'{url}&text={message}'
    async with aiohttp.ClientSession().get(req, verify_ssl=False, proxy=app.config.PROXY) as response:
        res = await response.json()
    return json(res)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        auto_reload=True,
    )