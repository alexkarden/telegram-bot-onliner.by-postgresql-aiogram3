import logging
import os
import asyncpg
from dotenv import load_dotenv
load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
}
print
# Создает и возвращает пул соединений к базе данных.--------------------------------------------------------------------PostgreSQL
async def create_pool():
    return await asyncpg.create_pool(**DATABASE_CONFIG)


# Инициализация базы данных---------------------------------------------------------------------------------------------PostgreSQL
async def init_db(pool):

    try:

        async with pool.acquire() as conn:

            # Создание таблицы
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS orders ("
                "id SERIAL PRIMARY KEY, "
                "number_of_order TEXT UNIQUE NOT NULL, "
                "order_text TEXT, "  
                "send_status INT NOT NULL, "
                "resend_status INT NOT NULL)"
            )

    except asyncpg.exceptions.PostgresError as e:
        logging.error(f"Ошибка при работе с PostgreSQL - Инициализация базы данных: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка при инициализации базы данных: {e}")



# Добавление заказа в базу данных --------------------------------------------------------------------------------------PostgreSQL
async def add_order_to_db(pool, number_of_order, order_text):
    send_status = 0
    resend_status = 0



    try:

        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO orders (number_of_order, order_text, send_status, resend_status) VALUES ($1, $2, $3, $4);",
                number_of_order, order_text, send_status, resend_status)

    except asyncpg.exceptions.PostgresError as e:
        logging.error(f"Ошибка при работе с PostgreSQL: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка Добавление заказа в базу данных: {e}")


# Получение последнего заказа из базы данных ---------------------------------------------------------------------------PostgreSQL
async def check_order_from_db(pool,orderkey):
    try:
        async with pool.acquire() as conn:
            # Используем SELECT EXISTS для более эффективной проверки
            check_number = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM orders WHERE number_of_order = $1);",
                orderkey
            )
            return check_number  # Вернет True или False в зависимости от наличия заказа
    except asyncpg.exceptions.PostgresError as e:
        logging.error(f"Ошибка при работе с PostgreSQL - Получение последнего заказа из базы данных: {e}")
        return False  # Возвращаем False, если произошла ошибка
    except Exception as e:
        logging.error(f"Произошла ошибка при получении последнего заказа из базы данных: {e}")
        return False  # Возвращаем False, если произошла ошибка


# Получение списка заказов из базы данных для рассылки -----------------------------------------------------------------PostgreSQL
async def get_order_list_for_rassilka(pool, status):

    try:

        async with pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM orders WHERE send_status = $1;", status)
            return result
    except asyncpg.exceptions.PostgresError as e:
        logging.error(f"Ошибка при работе с PostgreSQL - Получение списка заказов из базы данных для рассылки: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка Получение списка заказов из базы данных для рассылки: {e}")


# Смена статуса заказа для рассылки-------------------------------------------------------------------------------------PostgreSQL
async def change_status_order(pool, send_status, number_of_orders):
    try:

        async with pool.acquire() as conn:
            # Обновляем статус заказа
            await conn.execute(
                "UPDATE orders SET send_status = $1 WHERE number_of_order = $2",
                send_status, number_of_orders
            )
    except asyncpg.exceptions.PostgresError as e:
        logging.error(f"Ошибка при работе с PostgreSQL - Смена статуса заказа для рассылки: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка Смена статуса заказа для рассылки: {e}")


















