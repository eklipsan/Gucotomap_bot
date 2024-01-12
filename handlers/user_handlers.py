from aiogram import Router, types, F
from workers.map_worker import receive_quiz_setup
from keyboards.user_keyboards import create_keyboard_countries, lost_game_keyboard
from keyboards.service_keyboards import start_keyboard


router: Router = Router()

ATTEMPTS = 5

user = dict()
user['game'] = False
user['attempts'] = ATTEMPTS
user['score'] = 0
user['max_score'] = 0
user['played_games'] = 0


async def setup_quiz(message: types.Message):
    global town, countries
    town, map, countries = receive_quiz_setup()
    keyboard = create_keyboard_countries(countries=countries)

    print(town.town_name)
    print(town.town_values)
    await message.answer_photo(map.url_link,
                               reply_markup=keyboard,
                               caption='What country is this?')


@router.message(F.text == "Let's play")
async def start_quiz(message: types.Message):
    global user
    if user['game']:
        await message.answer("You are already in game")
    else:
        user['game'] = True
        user['score'] = 0
        await setup_quiz(message)


async def next_quiz(message: types.Message):
    await setup_quiz(message)


@router.message(lambda message: message.text in countries)
async def check_answer(message: types.Message):
    if user['game']:
        if message.text == town.town_values['country']:
            user['score'] += 1
            await message.answer(f"GOOD JOB. Your current score is {user['score']}. Keep it going!✨")
            await next_quiz(message)
        elif message.text != town.town_values['country'] and user['attempts'] > 1:
            user['attempts'] -= 1
            await message.answer(f"SHIT HAPPENS. You have {user['attempts']} attempts left")
            await next_quiz(message)
        else:
            if user['score'] > user['max_score']:
                user['max_score'] = user['score']
            user['played_games'] += 1
            user['game'] = False
            await message.answer(
                f"Sorry, but you have spent all {ATTEMPTS} attempts. Your score is {user['score']}",
                reply_markup=lost_game_keyboard
            )
    else:
        await message.answer(
            "If you want to play again, choose Let\'s start button, please.",
            reply_markup=lost_game_keyboard
        )


@router.message(F.text == 'Cancel the game')
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
async def get_main_menu(message: types.Message):
    await message.answer(
        "You are in the main menu",
        reply_markup=start_keyboard
    )


@router.message(F.text == 'Show statistic')
async def show_statistic(message: types.Message):
    stat_text = f'Your maximum score is {user["max_score"]}'
    await message.answer(stat_text)
