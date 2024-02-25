from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


map_lang_dict = {
        'Russian': 'ru_RU',
        'English-USA': 'en_US',
        'English-Russian': 'en_RU',
        'Russian-Ukranian': 'ru_UA',
        'Ukranian': 'uk_UA',
        'Turkish': 'tr_TR'
}
RETURN_PARAMETERS = 'Go to parameters'


def create_map_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Returns the keyboard that displays map languages
    """
    builder = ReplyKeyboardBuilder()
    # iterate through the keys in map_lang_dict
    for i in map_lang_dict.keys():
        builder.add(KeyboardButton(text=i))
    # add a button for returning parameters
    builder.add(KeyboardButton(text=RETURN_PARAMETERS))
    # adjust the layout of the keyboard
    builder.adjust(3)
    # return the keyboard as a markup with the option to resize
    return builder.as_markup(resize_keyboard=True)
