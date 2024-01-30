from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.service_keyboards import start_keyboard, feedback_keyboard
from access_filters.tg_filter import IsGame
from workers.database import create_connection

router: Router = Router()
# using user's status (game, not game) to access service handlers
router.message.filter(IsGame())

user_collection = create_connection()


@router.message(Command('start'))
async def start_handler(message: Message):
    start_message = (
        'Welcome to the game Gucotomap! 🗺\n'
        'In this game you have to guess countries by satellite images of their cities🧐\n'
        'To start playing click on the Let\'s play button 🎮\n'
    )
    await message.answer(start_message, reply_markup=start_keyboard)


@router.message(Command('help'))
async def help_handler(message: Message):
    help_message = (
        'To start playing you need to tap "Play"\n\n'
        'The rules of this game📃\n'
        '- A satellite image of the city appears in front of you🏙\n'
        '- There are  4️⃣ options for which country the city belongs to\n'
        '- Click on the suggested answer❓\n'
        '- If the answer is correct✅, you get 1 point for the correct answer\n'
        '- If the answer is wrong❌, you are taken off one attempt and the correct answer is shown.\n'
        '-The total number of incorrect attempts per game is 5️⃣.\n\n'
        'Have a good game🤗'
    )
    await message.answer(help_message)


@router.message(F.text == 'Feedback')
async def feedback_handler(message: Message):
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


@router.message(F.text == 'Get user id')
async def admin_get_user_id(message: Message):
    user_id_info = f"Your user id: <code>{message.from_user.id}</code>"
    await message.answer(user_id_info)


@router.message(Command('admin'))
async def no_admin_show_manual(message: Message):
    manual_no_admin_message = (
        'You do not have access to admin commands'
    )
    await message.answer(manual_no_admin_message)
