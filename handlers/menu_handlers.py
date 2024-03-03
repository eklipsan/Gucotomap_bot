from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu_keyboards import feedback_keyboard
from keyboards.parameter_keyboards import (
    parameter_menu,
    RETURN_PARAMETERS,
    map_lang_dict,
    generate_scale_range,
    generate_size_range,
    create_map_language_keyboard,
    create_map_scale_keyboard,
    create_map_size_keyboard
)
from access_filters.tg_filter import IsGame
from workers.database import (
    create_connection,
    get_user_info,
    set_user_parameter_state,
    set_user_map_language,
    set_user_map_scale,
    set_user_map_size
)
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
    set_user_parameter_state(user_collection, user_id, map_option='parameter')
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
    set_user_parameter_state(user_collection, user_id, map_option='lang')
    map_language_text = (
        'This option is used to display maps that are localized in various languages and reflect differences for specific countries.\n'
        'For example, for the regions RU, UA, and TR, distance is shown in kilometers. For US, distance is shown in miles.\n\n'
        '<b>Note</b>: The map language is set to English by default.\n'
        'If you want to change the map language, you can choose from the following options:'
    )
    await message.answer(map_language_text, reply_markup=create_map_language_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map language' button")


@router.message(F.text == 'Change map scale')
async def show_map_scale(message: Message):
    user_id = message.from_user.id
    set_user_parameter_state(user_collection, user_id, map_option='scale')
    map_scale_text = (
        'This option allows you to change the size of objects on the map.\n'
        'It increases the font size on labels and displays larger geographical objects (buildings, roads, bus stops, metro stations, and so on).\n'
        'So it determines the coefficient for enlarging all objects on the map and takes fractional values from 1.0 to 4.0.\n\n'
        '<b>Note</b>: The map scale is set to 1.0 by default.\n'
        'If you want to change the map scale, you can choose from the following options:'
    )
    await message.answer(map_scale_text, reply_markup=create_map_scale_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map scale' button")


@router.message(F.text == 'Change map size')
async def show_map_size(message: Message):
    user_id = message.from_user.id
    set_user_parameter_state(user_collection, user_id, map_option='size')
    map_size_text = (
        'This option determines the current resolution of the image from the map.\n'
        'The parameter  can take integer values from 0 to 21.\n'
        'When the zoom level is increased by one, the image resolution doubles.\n'
        'At the zero zoom level, the map shows the entire world, while at the maximum zoom level, it shows a single building.\n\n'
        '<b>Note</b>: The map size is set to 11 by default.\n'
        'If you want to change the map scale, you can choose from the following options:'
    )
    await message.answer(map_size_text, reply_markup=create_map_size_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map size' button ")


@router.message(lambda message: message.text in map_lang_dict.keys())
async def change_map_language(message: Message):
    user_id = message.from_user.id
    new_map_parameter = map_lang_dict[message.text]
    result = set_user_map_language(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(f"Map language has been changed to <b>{new_map_parameter}</b>", reply_markup=parameter_menu)


@router.message(lambda message: message.text in generate_scale_range())
async def change_map_scale(message: Message):
    user_id = message.from_user.id
    new_map_parameter = float(message.text)
    result = set_user_map_scale(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(f"Map scale has been changed to <b>{new_map_parameter}</b>", reply_markup=parameter_menu)


@router.message(lambda message: message.text in generate_size_range())
async def change_map_size(message: Message):
    user_id = message.from_user.id
    new_map_parameter = int(message.text)
    result = set_user_map_size(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(f"Map size has been changed to <b>{new_map_parameter}</b>", reply_markup=parameter_menu)