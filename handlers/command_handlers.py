from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from workers.database import init_user, create_connection
from workers.logset import logger
from keyboards.menu_keyboards import start_keyboard


router = Router()

user_collection = create_connection()


@router.message(Command('start'))
async def start_handler(message: Message):
    user_id = message.from_user.id
    init_user(user_collection, user_id, message)
    start_message = (
        'Welcome to the game Gucotomap! 🗺\n'
        'In this game you have to guess countries by satellite images of their cities🧐\n'
        'To start playing click on the Play button 🎮\n'
    )
    await message.answer(start_message, reply_markup=start_keyboard)
    logger.debug(f"User id {user_id} clicks on '/start' button")


@router.message(Command('help'))
async def help_handler(message: Message):
    user_id = message.from_user.id
    help_message = (
        'To start playing you need to tap "Play"\n\n'
        'The rules of this game📃\n'
        '- A satellite image of the city appears in front of you🏙\n'
        '- There are  4️⃣ options for which country the city belongs to\n'
        '- Click on the suggested answer❓\n'
        '- If the answer is correct✅, you get 1 point for the correct answer\n'
        '- If the answer is wrong❌, you are taken off one attempt and the correct answer is shown.\n'
        '-The total number of incorrect attempts per game is 5️⃣.\n\n'
        'Have a good game🤗'
    )
    await message.answer(help_message)
    logger.debug(f"User id {user_id} clicks on '/help' button")


@router.message(Command('admin'))
async def no_admin_show_manual(message: Message):
    user_id = message.from_user.id
    manual_no_admin_message = (
        'You do not have access to admin commands😿\n'
        'But there are hidden commands, available to you😁:\n'
        '<code>Get user id</code> - show user\'s id'
    )
    await message.answer(manual_no_admin_message)
    logger.debug(f"User id {user_id} clicks on negative '/admin' button")


@router.message(F.text == 'Get user id')
async def admin_get_user_id(message: Message):
    user_id = message.from_user.id
    user_id_info = f"Your user id: <code>{user_id}</code>"
    await message.answer(user_id_info)
    logger.debug(f"User id {user_id} gets their user id")
