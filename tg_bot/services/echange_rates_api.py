import aiohttp

from tg_bot.config import Config


class Exchanger:
    @staticmethod
    async def fetch_one(config: Config):
        url = f"https://api.fastforex.io/fetch-one?from=USD&to=RUB&api_key={config.tg_bot.exchanger_api}"
        headers = {"accept": "application/json"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.json()
