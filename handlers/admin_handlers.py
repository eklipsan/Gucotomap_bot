from aiogram import Router, F
from aiogram.types import Message
from config_data.config import Config, load_config
from access_filters.admin_filter import IsAdmin

config: Config = load_config()

router: Router = Router()
router.message.filter(IsAdmin())


@router.message(F.text == 'Am I admin?')
async def send_answer_is_admin(message: Message):
    await message.answer("Yes, you are admin.")
