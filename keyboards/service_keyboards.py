from aiogram import types

# Keyboard for both the start menu and the main menu
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='Play'),
            types.KeyboardButton(text='Parameters')
        ],
        [
            types.KeyboardButton(text='Statistic'),
            types.KeyboardButton(text='Feedback')
        ]
    ],
    resize_keyboard=True
)

feedback_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text='Telegram',
                url=r'https://t.me/eklipsan'
            )
        ],
        [
            types.InlineKeyboardButton(
                text='GitHub',
                url=r'https://github.com/eklipsan'
            )
        ]
    ]
)
