import aiohttp


async def send_email(recipient="olga.belykh@gmail.com", message="Super message"):
    url = "http://email:5000/send_email"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"recipient": recipient, "message": message}, verify_ssl=False) as response:
            return await response.json()


async def send_telegram(chat_id, message):
    url = "http://push:5000/send_push"
    async with aiohttp.ClientSession().post(url, json={"chat_id": chat_id, "message": message}, verify_ssl=False) as response:
        return await response.json()
