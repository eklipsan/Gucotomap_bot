from aiogram import Router
from aiogram.types import Message
from asyncio import sleep

router: Router = Router()


@router.message()
async def default_message(message: Message):
    pass_text = 'Sorry, but you should use only buttons 😐\nIf you need help, then enter /help command'
    sent_message = await message.reply(text=pass_text)
    await sleep(10)
    await message.delete()
    await sent_message.delete()
