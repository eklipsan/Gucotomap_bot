from aiogram import types

# Keyboard for both the start menu and the main menu
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='Let\'s play'),
            types.KeyboardButton(text='Thanks, later')
        ],
        [
            types.KeyboardButton(text='Change parameters'),
            types.KeyboardButton(text='Show statistic')
        ]
    ],
    resize_keyboard=True
)
