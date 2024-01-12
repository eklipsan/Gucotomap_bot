from environs import Env
from dataclasses import dataclass


@dataclass
class TelegramBot:
    bot_token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class MapKeyAPI:
    api_key: str


@dataclass
class Config:
    TelegramBot: TelegramBot
    DatabaseConfig: DatabaseConfig
    MapKeyAPI: MapKeyAPI


def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env(path)

    admin_ids_str = env.str("ADMIN_IDS").strip('[]')
    admin_ids = list(map(int, admin_ids_str.split(',')))

    return Config(
        TelegramBot=TelegramBot(
            bot_token=env("BOT_TOKEN"),
            admin_ids=admin_ids
        ),
        DatabaseConfig=DatabaseConfig(
            database=env("DATABASE"),
            db_host=env("DB_HOST"),
            db_user=env("DB_USER"),
            db_password=env("DB_PASSWORD")
        ),
        MapKeyAPI=MapKeyAPI(api_key=env("API_KEY_MAP"))
    )
