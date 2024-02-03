from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (menu_handlers,
                      user_handlers,
                      pass_handler,
                      admin_handlers,
                      command_handlers)
from workers.menu import set_main_menu
import asyncio


async def main():
    # Load configuration, using .env file
    config: Config = load_config()

    # Create bot instance
    bot: Bot = Bot(token=config.TelegramBot.bot_token, parse_mode='HTML')

    # Create dispatcher instance
    dp: Dispatcher = Dispatcher()
    # Include routers
    # Handlers, that allowed only for admins
    dp.include_router(router=admin_handlers.router)
    # Handler for commands starting with '/'
    dp.include_router(router=command_handlers.router)
    # Main menu handlers
    dp.include_router(router=menu_handlers.router)
    # User handlers for the game
    dp.include_router(router=user_handlers.router)

    # Notify user of using only buttons and deletes inappropriate message
    dp.include_router(router=pass_handler.router)

    # Delete webhook to drop accumulated updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
