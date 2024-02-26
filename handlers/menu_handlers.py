from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu_keyboards import feedback_keyboard
from keyboards.parameter_keyboards import (
    parameter_menu,
    RETURN_PARAMETERS,
    create_map_language_keyboard,
    create_map_scale_keyboard,
    create_map_size_keyboard
)
from access_filters.tg_filter import IsGame
from workers.database import create_connection, get_user_info
from workers.logset import logger


router: Router = Router()
# using user's status (game, not game) to access menu handlers
router.message.filter(IsGame())

user_collection = create_connection()


@router.message(F.text == 'Feedback')
async def feedback_handler(message: Message):
    user_id = message.from_user.id
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
    logger.debug(f"User id {user_id} clicks on 'Feedback' button")


@router.message(F.text == 'Statistic')
# This function shows user their game statistic
async def show_statistic(message: Message):
    user_id = message.from_user.id
    user = user_collection.find_one({"user_id": user_id})
    stat_text = (
        "🌟 Here is your progress! 🎉\n\n"
        f"Your maximum score so far is: {user['max_score']} 🏆\n"
        f"Total games played: {user['played_games']} 🕹️\n\n"
        "Keep playing to know more country cities! 🚀💪\n\n"
        "Challenge yourself to beat your own record and become a quiz master! 🌟🧠\n\n"
        "Thank you for playing and being part of the excitement! 🙌✨"
    )
    await message.answer(stat_text)
    logger.debug(f"User id {user_id} click on 'Statistic' button")


@router.message((F.text == "Parameters") | (F.text == RETURN_PARAMETERS))
async def show_parameters(message: Message):
    user_id = message.from_user.id
    user_dict = get_user_info(user_collection, user_id)
    parameters_text = (
        "⚙ Here is your parameters! \n\n"
        f"Your map language is {user_dict['map_lang']}\n"
        f"Your map scale is {user_dict['map_scale']}\n"
        f"Your map size is {user_dict['map_size']}"
    )
    await message.answer(parameters_text, reply_markup=parameter_menu)
    logger.debug(f"User id {user_id} clicks on 'Parameters' button")


@router.message(F.text == 'Change map language')
async def show_map_languages(message: Message):
    user_id = message.from_user.id
    map_language_text = (
        'This option is used to display maps that are localized in various languages and reflect differences for specific countries.\n'
        'For example, for the regions RU, UA, and TR, distance is shown in kilometers. For US, distance is shown in miles.\n\n'
        '<b>Note</b>: The map language is set to English by default.\n'
        'If you want to change the map language, you can choose from the following options:'
    )
    await message.answer(map_language_text, reply_markup=create_map_language_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map language' button")
