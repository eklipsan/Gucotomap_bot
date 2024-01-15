from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (service_handlers,
                      user_handlers,
                      pass_handler,
                      admin_handlers)
import asyncio


async def main():
    # Load configuration, using .env file
    config: Config = load_config()

    # Create bot instance
    bot: Bot = Bot(token=config.TelegramBot.bot_token, parse_mode='HTML')

    # Create dispatcher instance
    dp: Dispatcher = Dispatcher()

    # Include routers
    # Service handlers works with commands starting with '\'
    dp.include_router(router=service_handlers.router)
    # User handlers are need for the game
    dp.include_router(router=user_handlers.router)

    # Commands, that allowed only for admins
    dp.include_router(router=admin_handlers.router)
    # Notify user of using only buttons and deletes inappropriate message
    dp.include_router(router=pass_handler.router)

    # Delete webhook to drop accumulated updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
