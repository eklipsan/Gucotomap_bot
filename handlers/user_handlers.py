from aiogram import Router, types, F
from workers.map_worker import receive_quiz_setup
from keyboards.user_keyboards import create_keyboard_countries, lost_game_keyboard
from keyboards.service_keyboards import start_keyboard


router: Router = Router()


# Set up variables to keep track of the game state,
# including the number of attempts, user scores, and game status.
ATTEMPTS = 5
user = {
    'game': False,
    'attempts': ATTEMPTS,
    'score': 0,
    'max_score': 0,
    'played_games': 0
}


# Function sets up a quiz by retrieving a random town and associated map data.
# It creates a keyboard for selecting countries and sends a photo to the user.
async def setup_quiz(message: types.Message):
    global town, countries
    town, map, countries = receive_quiz_setup()
    keyboard = create_keyboard_countries(countries=countries)

    print(town.town_name)
    print(town.town_values)
    await message.answer_photo(
        map.url_link,
        reply_markup=keyboard,
        caption='What country is this?'
    )


@router.message(F.text == "Play")
# Message handler that starts the quiz game.
async def start_quiz(message: types.Message):
    global user
    if user['game']:
        await message.answer("You are already in the game")
    else:
        user['game'] = True
        user['score'] = 0
        await setup_quiz(message)


# This function sets up the next quiz.
async def next_quiz(message: types.Message):
    await setup_quiz(message)


@router.message(lambda message: message.text in countries)
# Message handler that checks the user's answer during the quiz game.
# It updates the user's score and attempts, and proceeds to the next quiz or ends the game based on the user's answer.
async def check_answer(message: types.Message):
    if user['game']:
        if message.text == town.town_values['country']:
            user['score'] += 1
            await message.answer(f"🌟 GOOD JOB!🌟\nYour current score is {user['score']}.\nKeep it going!✨")
            await next_quiz(message)
        elif message.text != town.town_values['country'] and user['attempts'] > 1:
            user['attempts'] -= 1
            await message.answer(f"Oops!😬\nThe right answer is {town.town_values['country']}.\nYou have {user['attempts']} attempts left.")
            await next_quiz(message)
        else:
            if user['score'] > user['max_score']:
                user['max_score'] = user['score']
            user['played_games'] += 1
            user['game'] = False
            await message.answer(
                f"Sorry, but you've used up all your {ATTEMPTS} attempts😿. Your score is {user['score']}.",
                reply_markup=lost_game_keyboard
            )
    else:
        await message.answer(
            "If you want to play again, choose the 'Play' button.🎮",
            reply_markup=lost_game_keyboard
        )


@router.message(F.text == 'Cancel the game')
# Message handler that cancels the game and returns the user to the main menu.
async def cancel_game(message: types.Message):
    global user
    if user['score'] > user['max_score']:
        user['max_score'] = user['score']
    user['played_games'] += 1
    user['game'] = False
    await message.answer(
        "You canceled the game. You are in the main menu",
        reply_markup=start_keyboard
    )


@router.message(F.text == "Go to main menu")
# Message handler that displays a message indicating that the user is in the main menu.
async def get_main_menu(message: types.Message):
    await message.answer(
        "You are in the main menu",
        reply_markup=start_keyboard
    )


@router.message(F.text == 'Statistic')
# This function shows user their game statistic
async def show_statistic(message: types.Message):
    stat_text = (
        "🌟 Here is your progress! 🎉\n\n"
        f"Your maximum score so far is: {user['max_score']} 🏆\n"
        f"Total games played: {user['played_games']} 🕹️\n\n"
        "Keep playing to know more country cities! 🚀💪\n\n"
        "Challenge yourself to beat your own record and become a quiz master! 🌟🧠\n\n"
        "Thank you for playing and being part of the excitement! 🙌✨"
    )
    await message.answer(stat_text)
