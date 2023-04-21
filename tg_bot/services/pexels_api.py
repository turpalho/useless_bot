import aiohttp

from tg_bot.config import Config


class Pexels:
    @staticmethod
    async def search_photos(config: Config, query: str,
                            per_page: int = 10, page: int = 1):
        url = (f"https://api.pexels.com/v1/search?\query={query}&per_page={per_page}&page={page}")
        headers = {"Authorization": config.tg_bot.pexels_token}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.json()
