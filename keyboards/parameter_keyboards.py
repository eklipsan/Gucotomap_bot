from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


parameter_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Change map language')
        ],
        [
            KeyboardButton(text='Change map scale')
        ],
        [
            KeyboardButton(text='Change map size')
        ],
        [
            KeyboardButton(text='Go to main menu')
        ]
    ],
    resize_keyboard=True
)
