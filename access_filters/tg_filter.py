from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_config, Config
from workers.database import (create_connection,
                              check_user_game_status,
                              get_user_info)


class IsAdmin(BaseFilter):
    "Aiogram filter, that checks if user is in the admin list"

    def __self__(self, admins_ids):
        self.admin_ids = self.admin_ids

    async def __call__(self, message: Message) -> bool:
        config: Config = load_config()
        self.admin_ids = config.TelegramBot.admin_ids
        return message.from_user.id in self.admin_ids


class IsGame(BaseFilter):
    """
    Aiogram filter, that checks if user is in the game status.
    It returns True if user is not in the game status.
    """

    def __self__(self, game_status):
        self.game_status = self.game_status

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user_collection = create_connection()
        self.game_status = check_user_game_status(user_collection, user_id)
        return self.game_status is False


class IsParameterStateEmpty(BaseFilter):
    """
    Aiogram filter, that checks if user's parameter state is empty.
    It returns True if user's parameter state is empty.
    """

    def __self__(self, parameter_state):
        self.parameter_state = self.parameter_state

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user_collection = create_connection()
        user_dict = get_user_info(user_collection, user_id)
        self.parameter_state = user_dict['parameter_state']
        return self.parameter_state == ''
