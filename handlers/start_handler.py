import os

from aiogram import (
    Router,
)
from aiogram.enums import (
    ParseMode,
)
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import (
    FSInputFile,
    Message,
)

from config import (
    ULNAME,
)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    caption = (f'👋 <b>Добро пожаловать!</b>\n\n'
               f'Это корпоративный бот ОДО {ULNAME}\n\n'
               f'Бот уведомляет Вас о новых заказах на маркетплейсе Onliner.\n\n'
               f'<i>Никаких настроек у бота нет - '
               f'если Ваш ID Telegram добавлен в список разрешенных, '
               f'то Вы будете получать уведомления. \n\n'
               f'Если не хотите получать уведомления, просто удалите бота. \n\n'
               f'Чтобы добавить ваш ID в список разрешенных - '
               f'обратитесь к администратору.</i>')

    # Отправляем пользователю приветствие
    if os.path.exists('image/start.png'):
        # Создаем объект для фотографии
        photo = FSInputFile('image/start.png')
        await message.answer_photo(photo=photo, caption=caption,
                                            parse_mode=ParseMode.HTML)
    else:
        await message.answer(text=caption, parse_mode=ParseMode.HTML)
