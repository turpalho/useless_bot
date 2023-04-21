from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


async def get_main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(*[
        InlineKeyboardButton(text="Прогноз погоды", callback_data="weather"),
        InlineKeyboardButton(text="Конвертация валют", callback_data="weather"),
        InlineKeyboardButton(text="Создание опроса", callback_data="weather"),
        InlineKeyboardButton(text="Случайная картинка", callback_data="weather"),
    ])
    kb.adjust(1)
    return kb.as_markup()
