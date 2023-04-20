from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class DbMiddleware(BaseMiddleware):
    def __init__(self, pool, repo):
        self.pool = pool
        self.repo = repo

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data["pool"] = self.pool
        data["repo"] = self.repo
        return await handler(event, data)
