from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config_data.config import Config, load_config
from access_filters.tg_filter import IsAdmin
from workers.logset import logger

config: Config = load_config()
filename = config.LogConfig.filepath

router: Router = Router()
router.message.filter(IsAdmin())


@router.message(F.text == 'Get log')
async def admin_get_log(message: Message):
    user_id = message.from_user.id
    document = FSInputFile(path=filename)
    await message.answer_document(document=document)
    logger.debug(f"User id {user_id} gets the log file {filename}")


@router.message(F.text == 'Get env')
async def admin_delete_log(message: Message):
    user_id = message.from_user.id
    document = FSInputFile(path='.env')
    await message.answer_document(document=document)
    logger.debug(f"User id {user_id} gets the env file")


@router.message(Command('admin'))
async def admin_show_manual(message: Message):
    user_id = message.from_user.id
    manual_admin_message = (
        'List of commands that are available to you as an admin\n'
        '<code>Get log</code> - return the log file\n'
        '<code>Get env</code> - return the env file\n'
        '<code>Get answer</code> - show the right answer during the game\n\n'
        'Other commands, that are hidden, but available to everyone\n'
        '<code>Get user id</code> - show user\'s id'
    )

    await message.answer(manual_admin_message)
    logger.debug(f"User id {user_id} gets the admin commands")
