from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_config, Config


class IsAdmin(BaseFilter):
    def __self__(self, admins_ids):
        self.admin_ids = self.admin_ids

    async def __call__(self, message: Message) -> bool:
        config: Config = load_config()
        self.admin_ids = config.TelegramBot.admin_ids
        return message.from_user.id in self.admin_ids
