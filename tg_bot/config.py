from dataclasses import dataclass

from environs import Env

from tg_bot.services.open_weather_api import OWM
from tg_bot.services.echange_rates_api import Exchanger
from tg_bot.services.pexels_api import Pexels


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    owm_token: str
    exchanger_token: str
    pexels_token: str
    admin_ids: list[int]
    use_redis: bool
    bot_name: str
    owm_api: OWM | None = None
    exchanger_api: Exchanger | None = None
    pxels_api: Pexels | None = None


@dataclass
class Miscellaneous:
    add_admin_cmd: str
    other_params = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            owm_token=env.str("OWM_TOKEN"),
            exchanger_token=env.str("EXCHANGER_TOKEN"),
            pexels_token=env.str("PEXELS_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            bot_name=env.str("BOT_NAME"),
            owm_api=OWM(),
            exchanger_api=Exchanger(),
            pxels_api=Pexels(),

        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            add_admin_cmd=env.str("ADD_ADMIN_CMD")
        )
    )
