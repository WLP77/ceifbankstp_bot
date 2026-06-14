from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.keyboards.application import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Hello! This bot is used for preliminary credit application submission on behalf of a legal entity.\n\n"
        "Press 'Start application' to begin.",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("myid"))
async def cmd_myid(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    await message.answer(
        f"Your user ID: {user_id}\n"
        f"Current chat ID: {chat_id}"
    )
