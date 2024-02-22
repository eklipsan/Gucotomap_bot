from aiogram import Router
from aiogram.types import Message
from asyncio import sleep
from workers.logset import logger
from workers.map_worker import receive_pass_photo

router: Router = Router()


@router.message()
async def default_message(message: Message):
    "The pass message for if the all router does not handle the update message"
    user_id = message.from_user.id
    pass_text = 'Sorry, but you should use only buttons 😐\nIf you need help, then enter /help command'
    pass_photo_text = 'You got an Easter egg 🐰 in the shape of a cute dog🐶.'
    sent_message = await message.reply(text=pass_text)
    sent_photo = await message.answer_photo(photo=receive_pass_photo(), caption=pass_photo_text)
    await sleep(10)
    await message.delete()
    await sent_message.delete()
    await sent_photo.delete()
    logger.debug(f"User id {user_id} causes the pass message by typing: {message.text}")
