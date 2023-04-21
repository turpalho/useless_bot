import logging

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tg_bot.config import Config
from database.repository import Repo
from tg_bot.filters.admin import AdminFilter

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
@admin_router.message(Command(commands = ["help"]))
async def admin_start(message: Message):
    text = "/del_admin - удалить админа"

    await message.answer(text)


@admin_router.message(Command(commands=["del_admin"]))
async def delete_admin(message: Message, repo: Repo, config: Config):
    config.tg_bot.admin_ids.remove(message.from_user.id)
    await repo.update_admin_ids(config.tg_bot.admin_ids)
    await message.answer("Администратор удален")
