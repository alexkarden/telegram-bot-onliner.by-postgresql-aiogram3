# © 2025
# Лицензия: MIT License
# Все права защищены.


"""Этот модуль предоставляет функциональность для запуска
бота Telegram с использованием библиотеки Aiogram.

Основные компоненты:
- Инициализация бота и диспетчера.
- Подключение обработчиков для управления командами и сообщениями.
- Настройка планировщика задач для регулярного обновления заказов
 и рассылки сообщений пользователям.
"""


import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler,
)
from dotenv import (
    load_dotenv,
)

from config import (
    CHECKINTERVAL,
    CHECKINTERVALR,
)
from handlers.about_handler import (
    router as about_handler,
)

# Импортируем роутеры из файлов обработчиков
from handlers.start_handler import (
    router as start_router,
)
from scripts import (
    create_pool,
    init_db,
)
from scripts_scheduler import (
    rassilka_for_users,
    update_orders,
)

load_dotenv()

bot = Bot(token=os.getenv("TOKEN_TG"))
dp = Dispatcher()

# Подключаем роутер
dp.include_router(start_router)
dp.include_router(about_handler)


async def main() -> None:
    """Главная функция."""
    pool = await create_pool()
    # Создаем базу данных, если ее нет.
    await init_db(pool)
    # Запускаем проверку цен и рассылку
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(update_orders, trigger="interval", seconds=CHECKINTERVAL,
                      kwargs={
                          "pool": pool,
                      },
                      )
    scheduler.add_job(rassilka_for_users, trigger="interval", seconds=CHECKINTERVALR,
                      kwargs={
                          "bot": bot,
                          "pool": pool,
                      },
                      )

    scheduler.start()
    await dp.start_polling(bot)
    await pool.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.ERROR,
        filename="logfile.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.exception("Exit")
