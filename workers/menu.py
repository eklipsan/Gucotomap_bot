from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Launch the bot'),
        BotCommand(command='/help',
                   description='Show bot manual'),
        BotCommand(command='/admin',
                   description='Admin commands')
    ]

    await bot.set_my_commands(main_menu_commands)
