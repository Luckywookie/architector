import aiohttp
from aiohttp import ClientProxyConnectionError, ClientError


async def send_email(config, recipient, message):
    url = config.EMAIL_SERVICE
    request = {"recipient": recipient, "message": message}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request, verify_ssl=False) as response:
                return await response.json()
    except ClientError as ex:
        print(ex)
        return {'error': ex}


async def send_telegram(config, message):
    url = config.PUSH_SERVICE
    request = {"chat_id": config.CHAT_ID, "message": message}
    try:
        async with aiohttp.ClientSession().post(url, json=request, verify_ssl=False) as response:
            return await response.json()
    except ClientProxyConnectionError as ex:
        print(ex)
    except ClientError as ex:
        print(ex)
        return {'error': ex}

