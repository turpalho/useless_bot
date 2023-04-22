import aiohttp
from typing import List


class Exchanger:
    @staticmethod
    async def fetch_one(config, currency_from: str, currencies_to: List):
        url = "https://api.apilayer.com/exchangerates_data/latest?symbols="
        for currency in currencies_to:
            url += f"{currency}%2C"

        url += f"&base={currency_from}"
        headers = {
            "accept": "application/json",
            "apikey": config.tg_bot.exchanger_token
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.json()
