from aiogram import Router
from aiogram.types import Message
from asyncio import sleep
from workers.logset import logger

router: Router = Router()


@router.message()
async def default_message(message: Message):
    "The pass message for if the all router does not handle the update message"
    user_id = message.from_user.id
    pass_text = 'Sorry, but you should use only buttons 😐\nIf you need help, then enter /help command'
    sent_message = await message.reply(text=pass_text)
    await sleep(10)
    await message.delete()
    await sent_message.delete()
    logger.debug(f"User id {user_id} causes the pass message by typing: {message.text}")
