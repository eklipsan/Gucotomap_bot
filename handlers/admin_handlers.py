from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config_data.config import Config, load_config
from access_filters.tg_filter import IsAdmin
from workers.logset import logger
from workers.database import create_connection, get_user_info
from json import dumps

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


@router.message(lambda message: message.text.startswith('Get user info'))
async def admin_get_user_info(message: Message):
    user_id = message.from_user.id
    user_collection = create_connection()
    message_list = message.text.split()
    if len(message_list) == 3:
        user_dict = get_user_info(user_collection, user_id)
        del user_dict['_id']
        pretty_dict_str = dumps(user_dict, indent=4)
        await message.answer(pretty_dict_str)
    else:
        try:
            selected_user_id = int(message_list[-1])
            user_dict = get_user_info(user_collection, selected_user_id)
            del user_dict['_id']
            pretty_dict_str = dumps(user_dict, indent=4)
            await message.answer(pretty_dict_str)
        except:
            error_msg = "There is neither typed user id in the database, nor you typed the command incorrectly"
            await message.answer(error_msg)
            logger.exception(f"User id {user_id} types the wrong format of admin command: {message.text}")
    logger.debug(f"User id {user_id} gets user info")


@router.message(Command('admin'))
async def admin_show_manual(message: Message):
    user_id = message.from_user.id
    manual_admin_message = (
        'List of commands that are available to you as an admin\n'
        '<code>Get log</code> - return the log file\n'
        '<code>Get env</code> - return the env file\n'
        '<code>Get user info [user_id]</code> - return all info of user id. If user id is not typed, it returns info of the current user id\n'
        '<code>Get answer</code> - show the right answer during the game\n\n'
        'Other commands, that are hidden, but available to everyone\n'
        '<code>Get user id</code> - show user\'s id'
    )

    await message.answer(manual_admin_message)
    logger.debug(f"User id {user_id} gets the admin commands")
