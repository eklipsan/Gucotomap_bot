from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.service_keyboards import start_keyboard, feedback_keyboard

router: Router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    start_message = '''Welcome to the game GeoGuesser! 🗺
    In this game you have to guess countries by satellite images of their cities🧐
    To start playing click on the Let's play button 🎮'''
    await message.answer(start_message, reply_markup=start_keyboard)


@router.message(F.text == 'Feedback')
async def feedback_handler(message: Message):
    feedback_message = (
        "Thank you for reaching out regarding my Telegram bot! 😊\n"
        "I appreciate your interest and feedback.\n"
        "Please provide any comments, suggestions, or issues you have encountered while using the bot.\n"
        "Your feedback is valuable to me, and I will be happy to talk to you about it.\n"
        "Please feel free to share any thoughts or questions you may have.\n"
        "I'm also attaching a link to my GitHub so you can see the code for this bot.\n"
        "Thank you again for your support! 🚀"
    )

    await message.answer(feedback_message, reply_markup=feedback_keyboard)


@router.message(F.text == 'Get user id')
async def admin_get_user_id(message: Message):
    user_id_info = f"Your user id: <code>{message.from_user.id}</code>"
    await message.answer(user_id_info)
