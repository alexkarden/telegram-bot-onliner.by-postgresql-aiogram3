from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message




router = Router()

@router.message(Command('about','alexkarden'))
async def cmd_about(message: Message):
    about_text = 'Бот написан Alex Karden - https://github.com/alexkarden'
    await message.answer(about_text, parse_mode=ParseMode.HTML)








