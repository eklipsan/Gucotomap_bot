from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import service_handlers, user_handlers, pass_handler
import asyncio


async def main():
    config: Config = load_config()
    bot: Bot = Bot(token=config.TelegramBot.bot_token)
    dp: Dispatcher = Dispatcher()

    # There must be routers
    dp.include_router(router=service_handlers.router)
    dp.include_router(router=user_handlers.router)

    dp.include_router(router=pass_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
