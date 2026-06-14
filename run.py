import asyncio
from aiogram import Bot, Dispatcher

from app.database import init_db
from app.main import create_bot, create_dispatcher


async def main() -> None:
    init_db()

    bot: Bot = await create_bot()
    dp: Dispatcher = await create_dispatcher()

    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
