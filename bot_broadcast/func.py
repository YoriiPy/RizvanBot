import aiohttp
import asyncio
import re

from database import requests as rq


async def is_live() -> bool | str:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    cookies = {
        "SOCS": "CAESEwgDEgk0ODEzNzk5NDIaAmVuIAEaBgiA_LyaBg",
        "CONSENT": "PENDING+999",
    }
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        channel_name = await rq.get_channel_name()
        if channel_name:
             async with session.get(f'https://www.youtube.com/@{channel_name}/live', cookies=cookies) as resp:
                if resp.status != 200:
                    return False

                html = await resp.text()

                canonical_match = re.search(
                    r'<link rel="canonical" href="(https://www\.youtube\.com/watch\?v=[^"]+)"',
                    html
                )

                if '"isLive":true' in html or '{"iconType":"LIVE"}' in html:
                    # Ищем ID текущего видео стрима
                    video_id_match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
                    if video_id_match:
                        return f"https://www.youtube.com/watch?v={video_id_match.group(1)}"

                    return f"https://www.youtube.com/@{channel_name}/live"

                return False







