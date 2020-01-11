import aiohttp
from sanic import Sanic
from sanic.response import json

app = Sanic(name='Push')


@app.route("/", methods=['GET'])
async def root(request):
    return json({})


@app.route("/send_push", methods=['GET'])
async def send_push(request):
    bot_token = app.config.BOT_TOKEN
    chat_id = app.config.CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}"
    req = f'{url}&text={request.args.get("text")}'
    async with aiohttp.ClientSession().get(req, verify_ssl=False, proxy="http://130.0.25.46:34964") as response:
        res = await response.json()
    return json(res)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        auto_reload=True,
    )