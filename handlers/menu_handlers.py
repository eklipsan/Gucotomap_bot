from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu_keyboards import feedback_keyboard
from access_filters.tg_filter import IsGame
from workers.database import create_connection

router: Router = Router()
# using user's status (game, not game) to access menu handlers
router.message.filter(IsGame())

user_collection = create_connection()


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
