import aiohttp
import asyncio

from database import requests


async def is_live() -> bool:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            result = await requests.get_url_stream()
            if result:
                async with session.get(f"{await requests.get_url_stream()}") as resp:
                    response = await resp.text()
                    if '"isLive":true' in response:
                        return True
                    else:
                        return False







