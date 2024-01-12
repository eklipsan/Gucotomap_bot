from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# keyboard for choosing countries with 'cancel' button
def create_keyboard_countries(countries: tuple) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=countries[0]),
            KeyboardButton(text=countries[1])
        ],
        [
            KeyboardButton(text=countries[2]),
            KeyboardButton(text=countries[3])
        ],
        [
            KeyboardButton(text='Cancel the game')
        ]
    ]
    keyboard_countries = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose one"
    )
    return keyboard_countries


# keyboard, when game is over
lost_game_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Let's play"),
            KeyboardButton(text="Go to main menu")
        ]
    ],
    resize_keyboard=True
)
