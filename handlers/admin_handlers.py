from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config_data.config import Config, load_config
from access_filters.admin_filter import IsAdmin

config: Config = load_config()

router: Router = Router()
router.message.filter(IsAdmin())


@router.message(F.text == 'Am I admin?')
async def send_answer_is_admin(message: Message):
    await message.answer("Yes, you are admin.")


@router.message(Command('admin'))
async def admin_show_manual(message: Message):
    manual_admin_message = (
        'List of commands that are available to you as an admin\n'
        '<code>Get answer</code> - show the right answer during the game\n\n'
        'Other commands, that are hidden, but available to everyone\n'
        '<code>Get user id</code> - show user\'s id'
    )

    await message.answer(manual_admin_message)
