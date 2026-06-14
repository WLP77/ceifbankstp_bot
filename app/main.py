from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers.start import router as start_router
from app.handlers.application import router as application_router
from app.handlers.admin import router as admin_router


async def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(application_router)
    dp.include_router(admin_router)
    return dp


async def create_bot() -> Bot:
    return Bot(token=BOT_TOKEN)
