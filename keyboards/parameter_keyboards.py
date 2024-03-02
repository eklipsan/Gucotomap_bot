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


def generate_scale_range() -> list:
    "Generate range of string-type scales options for map settings with step 0.5"
    result = list()
    start = 1
    while start <= 4:
        result.append(str(start))
        start += 0.5
    return result


def create_map_scale_keyboard(adjust: int = 3) -> ReplyKeyboardMarkup:
    """
    Returns the keyboard that displays map scales
    """
    # Initialize the keyboard builder
    builder = ReplyKeyboardBuilder()
    # Create number list from function with step 0.5
    scale_list = generate_scale_range()
    # Add buttons to the keyboard for each scale
    for number in scale_list:
        builder.add(KeyboardButton(text=str(number)))
    # Add a return parameters button
    builder.add(KeyboardButton(text=RETURN_PARAMETERS))
    # Adjust the keyboard layout
    builder.adjust(adjust)
    # return the keyboard as a markup with the option to resize
    return builder.as_markup(resize_keyboard=True)


def generate_size_range() -> list:
    "Generate range of string-type sizes options for map settings"
    result = list()
    start = 1
    while start <= 21:
        result.append(str(start))
        start += 1
    return result


def create_map_size_keyboard(adjust: int = 4) -> ReplyKeyboardMarkup:
    """
    Returns the keyboard that displays map sizes
    """
    # Initialize the keyboard builder
    builder = ReplyKeyboardBuilder()
    # Add buttons to the keyboard for each size
    for number in generate_size_range():
        builder.add(KeyboardButton(text=str(number)))
    # Add a return parameters button
    builder.add(KeyboardButton(text=RETURN_PARAMETERS))
    # Adjust the keyboard layout
    builder.adjust(adjust)
    # Return the keyboard markup with resized keyboard
    return builder.as_markup(resize_keyboard=True)
