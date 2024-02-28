from aiogram import Router, types, F
from workers.map_worker import receive_quiz_setup, receive_pass_photo
from keyboards.user_keyboards import create_keyboard_countries, lost_game_keyboard
from keyboards.menu_keyboards import start_keyboard
from access_filters.tg_filter import IsAdmin
from workers.logset import logger
from workers.database import (
    create_connection,
    setup_user_question,
    check_user_game_status,
    start_user_game,
    check_positive_attempts,
    increase_user_score,
    get_user_info,
    decrease_user_attempts,
    finish_user_game,
    set_user_parameter_state
)


router: Router = Router()


# Set up variables to keep track of the user's game state,
# including the number of attempts.
ATTEMPTS = 5

# Create mongodb connection for user data storage
user_collection = create_connection()


async def setup_quiz(message: types.Message):
    """
    Sets up a quiz by retrieving a random town and associated map data.
    Creates a keyboard for selecting countries and sends a photo to the user.
    """
    user_id = message.from_user.id
    town, map, countries = receive_quiz_setup(user_collection, user_id)
    setup_user_question(user_collection, user_id, town.town_name,
                        town.town_values, map.url_link, countries)
    town, map, countries = receive_quiz_setup()
    setup_user_question(
        user_collection,
        user_id,
        town.town_name,
        town.town_values,
        map.url_link,
        map.invalid_response,
        countries
        )
    user_dict = get_user_info(user_collection, user_id)
    # These del line should reconsidered, because they take much space in logs
    del user_dict['_id']
    del user_dict['map_url']
    if user_dict['map_invalid_response'] is True:
        # If map does not load, send message with explanation and a dog photo
        error_photo = receive_pass_photo()
        finish_user_game(user_collection, user_id, ATTEMPTS, map_error=True)
        await message.answer_photo(
            error_photo,
            caption="Sorry! The map has not loaded, but you can look at this cute dog🙏🏼",
            reply_markup=start_keyboard
            )
        await message.answer("You are in the main menu, but you might try to play again now or later.")
        logger.error(f"Map has not loaded for user id {user_id}")
    else:
        keyboard = create_keyboard_countries(countries=user_dict['countries'])
        await message.answer_photo(
            map.url_link,
            reply_markup=keyboard,
            caption='What country is this?'
        )
        logger.debug(f"Sending a quiz to user id {user_id}")
    logger.debug(f"{user_dict}")


@router.message(F.text == "Play")
async def start_quiz(message: types.Message):
    "Message handler that starts the quiz game."
    user_id = message.from_user.id
    if check_user_game_status(user_collection, user_id):
        await message.answer("You are already in the game")
        logger.debug(f"Trying to start a new game, while user id {user_id} is in the game")
    else:
        start_user_game(user_collection, user_id)
        await setup_quiz(message)
        logger.debug(f"Starting a game for user id {user_id}")


async def next_quiz(message: types.Message):
    "This function sets up the next quiz."
    user_id = message.from_user.id
    await setup_quiz(message)
    logger.debug(f"Setting up a new quiz for user id {user_id}")


@router.message(lambda message: message.text in get_user_info(user_collection, message.from_user.id)['countries'])
async def check_answer(message: types.Message):
    """
    Message handler that checks the user's answer during the quiz game.
    It updates the user's score and attempts.
    Proceeds to the next quiz or ends the game based on the user's answer.
    """
    user_id = message.from_user.id
    if check_user_game_status(user_collection, user_id):
        logger.debug(f"User id {user_id} game status is active.")
        if message.text == get_user_info(user_collection, user_id)['town_values']['country']:
            logger.debug(f"User id {user_id} answered correctly - {message.text}")
            increase_user_score(user_collection, user_id)
            user_dict = get_user_info(user_collection, user_id)
            good_job_message = f"🌟 GOOD JOB!🌟\nYour current score is {user_dict['score']}.\nKeep it going!✨"
            await message.answer(good_job_message)
            await next_quiz(message)
        elif message.text != get_user_info(user_collection, user_id)['town_values']['country'] and check_positive_attempts(user_collection, user_id):
            right_answer = get_user_info(user_collection, user_id)['town_values']['country']
            decrease_user_attempts(user_collection, user_id)
            user_dict = get_user_info(user_collection, user_id)
            await message.answer(f"Oops!😬\nThe right answer is {user_dict['town_values']['country']}.\nYou have {user_dict['attempts']} attempts left.")
            await next_quiz(message)
            logger.debug(f"User id {user_id} answered incorrectly but still has attempts left. Right answer - {right_answer}. Their answer - {message.text}. Left attempts - {user_dict['attempts']} ")
        else:
            user_dict = get_user_info(user_collection, user_id)
            finish_user_game(user_collection, user_id, ATTEMPTS)
            await message.answer(
                f"Sorry, but you've used up all your {ATTEMPTS} attempts😿. Your score is {user_dict['score']}.",
                reply_markup=lost_game_keyboard
            )
            logger.debug(f"User id {user_id} used up all attempts. Earned the game score - {user_dict['score']}")
    else:
        logger.debug(f"User id {user_id} game status is inactive.")
        await message.answer(
            "If you want to play again, choose the 'Play' button.🎮",
            reply_markup=lost_game_keyboard
        )


@router.message(F.text == 'Cancel the game')
async def cancel_game(message: types.Message):
    "Message handler that cancels the game and returns the user to the main menu."
    user_id = message.from_user.id
    finish_user_game(user_collection, user_id, ATTEMPTS)
    await message.answer(
        "You have canceled the game. You are in the main menu",
        reply_markup=start_keyboard
    )
    logger.debug(f"User id {user_id} cancels the game")


@router.message(F.text == "Go to main menu")
async def get_main_menu(message: types.Message):
    "Message handler that displays a message indicating that the user is in the main menu."
    user_id = message.from_user.id
    # Set map parameter to '' to not let user change parameters when they are in the main menu
    set_user_parameter_state(user_collection, user_id, map_option='')
    await message.answer(
        "You are in the main menu",
        reply_markup=start_keyboard
    )
    logger.debug(f"Going to the main menu for user id {user_id}")


@router.message(IsAdmin() and F.text == 'Get answer')
async def admin_get_answer(message: types.Message):
    '''
    Handler, that returns the right current answer.
    It works only for admins.
    '''
    user_id = message.from_user.id
    user_dict = get_user_info(user_collection, user_id)
    admin_answer_text = f"Town: {user_dict['town_name']}\nTown values: {user_dict['town_values']}"
    await message.answer(admin_answer_text)
    logger.info(f"User id {user_id} gets the right current answer")
