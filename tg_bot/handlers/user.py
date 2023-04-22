import logging
import random

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from database.repository import Repo
from tg_bot.config import Config
from tg_bot.keyboards.inline_user import (
    get_main_keyboard, get_cancel_to_menu_keyboard,
    get_currency_keyboard)
from tg_bot.filters.user import AddAdminFilter
from tg_bot.misc.states import WeatherState, PollsState

logger = logging.getLogger(__name__)

user_router = Router()
user_router.message.filter(F.chat.type == "private")
user_router.callback_query.filter(F.message.chat.type == "private")


@user_router.message(CommandStart())
async def user_start(message: Message, repo: Repo, state: FSMContext) -> None:
    if (not await repo.user_exists(message.chat.id)):
        await repo.add_user(user_id=message.chat.id,
                            username=message.chat.username,
                            full_name=message.chat.full_name)

    await state.clear()
    text = f"Меню:"
    await message.answer(text=text,
                         reply_markup=await get_main_keyboard())


@user_router.callback_query(F.data == "main_menu")
async def user_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = f"Меню:"
    try:
        await call.message.edit_text(text=text,
                                     reply_markup=await get_main_keyboard())
    except:
        await call.message.delete()
        await call.message.answer(text=text,
                                  reply_markup=await get_main_keyboard())

# Прогноз погоды
@user_router.callback_query(F.data == "weather")
async def application_sent(call: CallbackQuery, repo: Repo, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(WeatherState.waiting_enter_city)
    text = 'Введите название города:'
    await call.message.edit_text(text=text,
                                 reply_markup=await get_cancel_to_menu_keyboard())


@user_router.message(WeatherState.waiting_enter_city)
async def application_sent(message: Message, state: FSMContext, config: Config) -> None:
    await state.clear()
    response = await config.tg_bot.owm_api.get_weather(config=config, city=message.text)
    text = f"🏢  Город: {message.text}\n⛅  Погода: {response['weather'][0]['description']}\n🌡  Температура: {response['main']['temp']} °C"
    await message.answer(text=text,
                         reply_markup=await get_cancel_to_menu_keyboard())

# Конвертация валют
@user_router.callback_query(F.data == "exchange")
async def application_sent(call: CallbackQuery) -> None:
    await call.answer()
    text = 'Выберите валюту, которую будете менять:'
    await call.message.edit_text(text=text,
                                 reply_markup=await get_currency_keyboard())


@user_router.callback_query(Text(startswith="currency_"))
async def application_sent(call: CallbackQuery, config: Config) -> None:
    await call.answer()
    currencies_to = {"EUR": "🇪🇺  Евро",
                     "RUB": "🇷🇺  Рубль",
                     "USD": "🇺🇸  Доллар",
                     "TRY": "🇹🇷  Турецкая лира",
                     "GBP": "🇬🇧  Фунт",
                     "CNY": "🇨🇳  Юань"}
    currency_from = call.data.split("_")[1]
    rates = [f"{currencies_to[currency_from]}: \n"]
    currencies_to.pop(currency_from)
    response = await config.tg_bot.exchanger_api.fetch_one(config=config,
                                                           currency_from=currency_from,
                                                           currencies_to=currencies_to)

    for currency, rate in response['rates'].items():
        rates.append(currencies_to[currency] + ": " + str(rate))
    await call.message.edit_text(text='\n'.join(rates),
                                 reply_markup=await get_cancel_to_menu_keyboard())

# Создание опроса
@user_router.callback_query(F.data == "polls")
async def application_sent(call: CallbackQuery, repo: Repo, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(PollsState.waiting_question)
    text = 'Введите вопрос для своего опроса:'
    await call.message.edit_text(text=text,
                                 reply_markup=await get_cancel_to_menu_keyboard())


@user_router.message(PollsState.waiting_question)
async def application_sent(message: Message, state: FSMContext, config: Config) -> None:
    await state.set_data({"question": message.text})
    await state.set_state(PollsState.waiting_options)
    text = "Введите варианты ответов через запятую"
    await message.answer(text=text,
                         reply_markup=await get_cancel_to_menu_keyboard())


@user_router.message(PollsState.waiting_options)
async def application_sent(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await bot.send_poll(message.chat.id,
                        question=state_data['question'],
                        options=message.text.split(','),
                        is_anonymous=True,
                        allows_multiple_answers=True)
    text = "Опрос создан"
    await message.answer(text=text,
                         reply_markup=await get_cancel_to_menu_keyboard())
    await state.clear()

# Картинка с милыми животными
@user_router.callback_query(F.data == "imgs")
async def application_sent(call: CallbackQuery, config: Config) -> None:
    await call.answer()
    query = "cute-animals"
    response = await config.tg_bot.pxels_api.search_photos(config=config, query=query)
    text = 'Картинка с милыми животными:'

    await call.message.delete()
    await call.message.answer_photo(
        response['photos'][random.randrange(1, 5)]['url'],
        caption=text,
        parse_mode="markdown",
        reply_markup=await get_cancel_to_menu_keyboard())


@user_router.message(AddAdminFilter())
async def add_admin(message: Message, config: Config, repo: Repo) -> None:
    if not message.chat.id in config.tg_bot.admin_ids:
        config.tg_bot.admin_ids.append(message.chat.id)
        await repo.update_admin_ids(config.tg_bot.admin_ids)
        await message.answer("Вы получили права администратора")
    else:
        await message.answer("Вы уже являетесь администратором!")


@user_router.message(Command(commands=["help"]))
async def get_help(message: Message):
    text = (
        """```
Чтобы узнать погоду, нажмите 'Прогноз погоды'.
--------------------------
Чтобы конвертировать валюту, нажмите 'Конвертакция валют'.
--------------------------
Чтобы создать опрос, нажмите 'Создание опроса'.
--------------------------
Чтобы получить случайную картинку с милыми животными, нажмите 'Случайная картинка'.
```"""
    )
    await message.answer(text=text, parse_mode="Markdown")
