import smtplib

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

app = Sanic(name='Email')


@app.route("/", methods=['GET'])
async def root(request):
    return json({})


@app.route("/send_email", methods=['POST'])
async def send_email(request: Request):
    recipient = request.json.get("recipient")
    message = request.json.get("message")
    session = smtplib.SMTP("mailhog", port=1025)
    session.sendmail("admin@market.ru", recipient, message)
    session.quit()
    return json({'result': 'OK'})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        auto_reload=True,
    )