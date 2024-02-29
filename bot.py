from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (menu_handlers,
                      user_handlers,
                      pass_handler,
                      admin_handlers,
                      command_handlers)
from workers.menu import set_main_menu
from workers.logset import logger, get_log_state
import asyncio
from time import sleep


async def main():
    # Load configuration, using .env file
    logger.debug("Loading configuration from .env file")
    config: Config = load_config()
    # Print current log configuration
    get_log_state(config)
    # Create bot instance
    logger.debug("Creating bot instance")
    bot: Bot = Bot(token=config.TelegramBot.bot_token, parse_mode='HTML')

    # Create dispatcher instance
    logger.debug("Creating dispatcher instance")
    dp: Dispatcher = Dispatcher()
    # Include routers
    logger.debug("Including routers")
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
    logger.debug("Deleting webhook to drop accumulated updates")
    await bot.delete_webhook(drop_pending_updates=True)
    logger.debug("Setting main menu")
    await set_main_menu(bot)
    logger.debug("Starting polling")
    await dp.start_polling(bot, none_stop=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        logger.exception("The bot has stopped!")
        sleep(3)
        asyncio.run(main())
