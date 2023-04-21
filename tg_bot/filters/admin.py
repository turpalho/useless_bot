from aiogram.filters import BaseFilter
from aiogram.types import Message

from tg_bot.config import Config


class AdminFilter(BaseFilter):

    def __init__(self, is_admin: bool = True) -> None:
        self.is_admin = is_admin

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin # type: ignore
