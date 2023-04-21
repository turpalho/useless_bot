import aiohttp

from tg_bot.config import Config


class OWM:
    @staticmethod
    async def get_weather(config: Config, city: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.tg_bot.owm_token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()