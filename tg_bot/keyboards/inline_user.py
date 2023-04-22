from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


async def get_main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="⛅  Прогноз погоды",
                             callback_data="weather"),
        InlineKeyboardButton(text="💵  Конвертация валют",
                             callback_data="exchange"),
        InlineKeyboardButton(text="🗣  Создание опроса",
                             callback_data="polls"),
        InlineKeyboardButton(text="🎲  Случайная картинка",
                             callback_data="imgs"),
    ])
    kb.adjust(1)
    return kb.as_markup()


async def get_cancel_to_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ])
    kb.adjust(1)
    return kb.as_markup()


async def get_currency_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="🇷🇺  Рубль", callback_data="currency_RUB"),
        InlineKeyboardButton(text="🇺🇸  Доллар", callback_data="currency_USD"),
        InlineKeyboardButton(text="🇪🇺  Евро", callback_data="currency_EUR"),
        InlineKeyboardButton(text="🇹🇷  Лир", callback_data="currency_TRY"),
        InlineKeyboardButton(text="🇬🇧  Фунт", callback_data="currency_GBP"),
        InlineKeyboardButton(text="🇨🇳  Юань", callback_data="currency_CNY"),
    ])
    kb.adjust(1)
    return kb.as_markup()
