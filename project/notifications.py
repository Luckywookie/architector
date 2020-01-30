import aiohttp


async def send_email(config, recipient, message):
    url = config.EMAIL_SERVICE
    request = {"recipient": recipient, "message": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=request, verify_ssl=False) as response:
            return await response.json()


async def send_telegram(config, message):
    url = config.PUSH_SERVICE
    request = {"chat_id": config.chat_id, "message": message}
    async with aiohttp.ClientSession().post(url, json=request, verify_ssl=False) as response:
        return await response.json()
