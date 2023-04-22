import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.db import create_db, dispose_db
from database.repository import Repo
from tg_bot.config import Config, load_config
from tg_bot.handlers.admin import admin_router
from tg_bot.handlers.user import user_router
from tg_bot.middlewares.config import ConfigMiddleware
from tg_bot.middlewares.db_middleware import DbMiddleware


logger = logging.getLogger(__name__)

bot_commands = [
    types.BotCommand(command="/start", description="Главное меню"),
    types.BotCommand(command="/help", description="Инструкция"),
]


async def on_shutdown(pool) -> None:
    await dispose_db(pool)


async def configure_logging() -> None:
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                '.logs/log.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ],
        level=logging.INFO,
        # format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        format=u'#%(levelname)-3s [%(asctime)s] | %(message)s',
    )


async def create_pool(user, password, host, database, echo) -> AsyncEngine:
    engine = await create_db(user, password, host, database, echo)
    return engine


async def restore_config(config: Config, repo: Repo) -> None:
    config_parameters = await repo.get_config_parameters()
    if config_parameters:
        admin_ids = [int(admin_id)
                     for admin_id in config_parameters[0].admins_ids.split(",")]
        config.tg_bot.admin_ids = admin_ids
    else:
        await repo.create_config(config.tg_bot.admin_ids)


async def register_global_middlewares(dp: Dispatcher, config, pool, repo) -> None:
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    dp.my_chat_member.outer_middleware(ConfigMiddleware(config))
    dp.chat_member.outer_middleware(ConfigMiddleware(config))

    dp.message.middleware(DbMiddleware(pool, repo))
    dp.callback_query.outer_middleware(DbMiddleware(pool, repo))
    dp.my_chat_member.middleware(DbMiddleware(pool, repo))
    dp.chat_member.outer_middleware(DbMiddleware(pool, repo))


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    # await configure_logging()

    logger.info("Starting bot")
    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage(redis=Redis(host="redis", port=6379))
    else:
        storage = MemoryStorage()

    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        database=config.db.database,
        echo=False,
    )
    repo = Repo(pool)

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    await bot.set_my_commands(bot_commands)

    for router in [
        admin_router,
        user_router
    ]:
        dp.include_router(router)

    await restore_config(config, repo)

    await register_global_middlewares(dp, config, pool, repo)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    # await on_shutdown(pool)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Exit")
