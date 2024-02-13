from environs import Env
from dataclasses import dataclass


@dataclass
class TelegramBot:
    bot_token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    mongodb_name: str
    mongodb_password: str
    mongodb_cluster: str


@dataclass
class MapKeyAPI:
    api_key: str


@dataclass
class LogConfig:
    console_on: int
    file_on: int
    filepath: str
    level_info_console: int
    level_info_file: int

@dataclass
class Config:
    TelegramBot: TelegramBot
    DatabaseConfig: DatabaseConfig
    MapKeyAPI: MapKeyAPI
    LogConfig: LogConfig


def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env(path)

    admin_ids = list(map(int, env.list("ADMIN_IDS")))

    return Config(
        TelegramBot=TelegramBot(
            bot_token=env("BOT_TOKEN"),
            admin_ids=admin_ids
        ),
        DatabaseConfig=DatabaseConfig(
            mongodb_name=env("MONGODB_NAME"),
            mongodb_password=env("MONGODB_PASSWORD"),
            mongodb_cluster=env("MONGODB_CLUSTER")
        ),
        MapKeyAPI=MapKeyAPI(api_key=env("API_KEY_MAP")),
        LogConfig=LogConfig(
            console_on=env.int("LOG_CONSOLE_ON"),
            file_on=env.int("LOG_FILE_ON"),
            filepath=env("LOG_FILEPATH"),
            level_info_console=env.int("LOG_LEVEL_INFO_CONSOLE"),
            level_info_file=env.int("LOG_LEVEL_INFO_FILE")
        )

    )
