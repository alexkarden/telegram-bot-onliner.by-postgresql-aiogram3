import asyncio
import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import CHECKINTERVAL,CHECKINTERVALR

from scripts import init_db, create_pool
from scripts_scheduler import update_orders,rassilka_for_users

load_dotenv()



bot = Bot(token=os.getenv("TOKEN_TG"))
dp = Dispatcher()

# Импортируем роутеры из файлов обработчиков
from handlers.start_handler import router as start_router
from handlers.about_handler import router as about_handler
# Подключаем роутер
dp.include_router(start_router)
dp.include_router(about_handler)



#-----------------------------------------------------------------------------------------------------------------------Основная функция
async def main():
    pool = await create_pool()
    #Создаем базу данных, если ее нет.
    await init_db(pool)
    #Запускаем проверку цен и рассылку
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(update_orders, trigger='interval', seconds=CHECKINTERVAL,
                      kwargs={
                          'pool': pool,
                      }
                      )
    scheduler.add_job(rassilka_for_users, trigger='interval', seconds=CHECKINTERVALR,
                      kwargs={
                          'bot': bot,
                          'pool': pool,
                      }
                      )

    # scheduler.add_job(update_orders, args=[pool], trigger='interval', seconds=CHECKINTERVAL)
    # scheduler.add_job(rassilka_for_users, args=[bot, pool], trigger='interval', seconds=CHECKINTERVALR)



    # Запускаем шейдулер
    scheduler.start()
    # Запускаем поллинг
    await dp.start_polling(bot)
    await pool.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        filename='logfile.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.error('Exit')