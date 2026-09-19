import aiohttp
import asyncio

from database import requests as rq


async def is_live() -> bool:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    cookies = {
        "SOCS": "CAESEwgDEgk0ODEzNzk5NDIaAmVuIAEaBgiA_LyaBg",
        "CONSENT": "PENDING+999",
    }
    async with aiohttp.ClientSession(headers=HEADERS) as session:

        while True:
            channel_name = await rq.get_channel_name()
            if channel_name:
                async with session.get(f'https://www.youtube.com/@{channel_name}/live', cookies=cookies) as resp:

                    final_url = str(resp.url)
                    has_video_redirect = "watch?v=" in final_url
                    html = await resp.text()
                    if '"isLive":true' in html or has_video_redirect:
                        return True
                    else:
                        return False







