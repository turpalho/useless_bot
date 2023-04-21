import logging

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.repository import Repo
from tg_bot.config import Config
from tg_bot.keyboards.inline_user import (get_main_keyboard)
from tg_bot.filters.user import AddAdminFilter

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
    await message.answer(text=text, reply_markup=await get_main_keyboard())


@user_router.callback_query(F.data == "main_menu")
async def user_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = f"Меню:"
    await call.message.edit_text(text=text,
                                 reply_markup=await get_main_keyboard())


@user_router.message(AddAdminFilter())
async def add_admin(message: Message, config: Config, repo: Repo) -> None:
    if not message.chat.id in config.tg_bot.admin_ids:
        config.tg_bot.admin_ids.append(message.chat.id)
        await repo.update_admin_ids(config.tg_bot.admin_ids)
        await message.answer("Вы получили права администратора")
    else:
        await message.answer("Вы уже являетесь администратором!")
