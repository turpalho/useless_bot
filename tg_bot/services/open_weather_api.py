import aiohttp


class OWM:
    @staticmethod
    async def get_weather(config, city: str):
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'units': 'metric',
            'lang': 'ru',
            'APPID': config.tg_bot.owm_token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()
