from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu_keyboards import feedback_keyboard, start_keyboard
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
    set_user_map_size,
    reset_map_parameters
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
        "⚙️ Welcome to your personalized settings! 🌈\n\n"
        f"🗣️ Map Language: {user_dict['map_lang']}\n"
        f"🔍 Map Scale: {user_dict['map_scale']}\n"
        f"📏 Map Size: {user_dict['map_size']}\n\n"
        "Everything is set just the way you like it! Feel free to adjust these settings anytime to enhance your experience. 😊"
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
        'If you want to change the map language, you can choose from the following options:\n'
        '1. 🇷🇺 Russian: ru_RU\n'
        '2. 🇺🇸 English-USA: en_US\n'
        '3. 🇷🇺 🇺🇸 English-Russian: en_RU\n'
        '4. 🇷🇺 🇺🇦 Russian-Ukranian: ru_UA\n'
        '5. 🇺🇦 Ukranian: uk_UA\n'
        '6. 🇹🇷 Turkish: tr_TR\n\n'
        '<b>Note</b>: The map language is set to 🇺🇸 English-USA by default.'
    )
    await message.answer(map_language_text, reply_markup=create_map_language_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map language' button")


@router.message(F.text == 'Change map scale')
async def show_map_scale(message: Message):
    user_id = message.from_user.id
    set_user_parameter_state(user_collection, user_id, map_option='scale')
    map_scale_text = (
        'Ready to see the world a bit differently? 🌍✨\n'
        'Adjusting the map scale lets you zoom in on the details or zoom out for the bigger picture. It’s like having a magnifying glass for everything from street signs to entire cities!\n'
        'You can set the zoom level anywhere from a close-up 1.0 to a wide-angle 3.5.\n\n'
        '<b>Note</b>: We start you off at a comfortable 1.0 zoom. Ready to explore?\n'
        'Pick your preferred scale from the options below and let the adventure begin!'
    )
    await message.answer(map_scale_text, reply_markup=create_map_scale_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map scale' button")


@router.message(F.text == 'Change map size')
async def show_map_size(message: Message):
    user_id = message.from_user.id
    set_user_parameter_state(user_collection, user_id, map_option='size')
    map_size_text = (
        '🌟 Ready to fine-tune your map\'s view? This setting lets you adjust the image resolution to make every detail count.\n'
        'You can pick any value between 0 and 12, where each increase in zoom level sharpens your map\'s resolution twofold.\n'
        'At a glance, zoom level 0 gives you a world view, while higher values zoom in closer.\n\n'
        '<b>Heads up</b>: Your map size is set to 11 to start for comfortable gaming\n'
        'Eager for a change? Dive into the options below to adjust your map size:'
    )
    await message.answer(map_size_text, reply_markup=create_map_size_keyboard())
    logger.debug(f"User id {user_id} clicks on 'Change map size' button ")


@router.message(F.text == 'Reset map parameters')
async def reset_user_parameters(message: Message):
    user_id = message.from_user.id
    if reset_map_parameters(user_collection, user_id):
        map_reset_text = (
            "🔄 Hooray! We've refreshed your map settings back to their cozy defaults 🌟:\n"
        "- Language: English-USA (en_US) 🇺🇸\n"
        "- Scale: A friendly 1.0 for easy navigation 🌍\n"
        "- Size: Set at 11 for the perfect balance of detail and overview 🔍\n"
        "Everything's set for your next adventure!"
        )
        await message.answer(
            text=map_reset_text,
            reply_markup=start_keyboard
        )
        logger.debug(f"User id {user_id} resets map parameters to default values")


@router.message(lambda message: message.text in map_lang_dict.keys())
async def change_map_language(message: Message):
    user_id = message.from_user.id
    new_map_parameter = map_lang_dict[message.text]
    result = set_user_map_language(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(
            f"🌍✨ Your map language has been updated to <b>{new_map_parameter}</b>! Explore the world in your preferred language.",
            reply_markup=parameter_menu
        )
    logger.debug(f"User id {user_id} changes map language to {new_map_parameter}")


@router.message(lambda message: message.text in generate_scale_range())
async def change_map_scale(message: Message):
    user_id = message.from_user.id
    new_map_parameter = float(message.text)
    result = set_user_map_scale(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(
            f"🔍🌐 Your map scale is now set to <b>{new_map_parameter}</b>! Get ready to zoom in and discover new details.",
            reply_markup=parameter_menu
        )
    logger.debug(f"User id {user_id} changes map scale to {new_map_parameter}")


@router.message(lambda message: message.text in generate_size_range())
async def change_map_size(message: Message):
    user_id = message.from_user.id
    new_map_parameter = int(message.text)
    result = set_user_map_size(user_collection, user_id, new_map_parameter)
    if result:
        await message.answer(
            f"🖼️🔎 Your map's resolution is now adjusted to <b>{new_map_parameter}</b>! Enjoy the clearer views on your adventures.",
            reply_markup=parameter_menu
        )
    logger.debug(f"User id {user_id} changes map size to {new_map_parameter}")


@router.message(F.text == "Go to main menu")
async def get_main_menu(message: Message):
    user_id = message.from_user.id
    set_user_parameter_state(user_collection, user_id, map_option='')
    await message.answer(
        "🏠 Welcome back to the main menu! What would you like to do next?",
        reply_markup=start_keyboard
    )
    logger.debug(f"Going to the main menu for user id {user_id}")