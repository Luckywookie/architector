import smtplib

from sanic import Sanic
from sanic.response import json

app = Sanic(name='Email', load_env=False)

@app.route("/", methods=['GET'])
async def root(request):
    return json({})

@app.route("/send_email", methods=['GET'])
async def send_email(request):
    session = smtplib.SMTP("mailhog", port=1025)
    session.sendmail("admin@market.ru", "olga.belykh@gmail.com", "Super message")
    session.quit()
    return json({'result': 'OK'})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        auto_reload=True,
    )