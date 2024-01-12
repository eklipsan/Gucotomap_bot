from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.service_keyboards import start_keyboard

router: Router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    start_message = '''Welcome to the game GeoGuesser! 🗺
    In this game you have to guess countries by satellite images of their cities🧐
    To start playing click on the Let's play button 🎮'''
    await message.answer(start_message, reply_markup=start_keyboard)
