import logging
import ast

from aiogram import Bot

from apionliner import get_order_list, get_order
from scripts import check_order_from_db, add_order_to_db, get_order_list_for_rassilka,  change_status_order
from config import LISTOFADMINS



async def update_orders(pool):
    orders = get_order_list()

    for order in orders['orders']:
        check_order = await check_order_from_db(pool,str(order['key']))
        if check_order == False:
            await add_order_to_db(pool, order['key'], str(get_order(order['key'])))


async def rassilka_for_users(bot:Bot, pool):
    try:
        order_list_for_rassilka = await get_order_list_for_rassilka(pool,0)
        for order in order_list_for_rassilka:
            number_of_orders = order[1]
            data_tuple = ast.literal_eval(order[2])

            # Извлечение данных

            order_id = data_tuple['key']

            price = f'{data_tuple['order_price']['amount']} {data_tuple['order_price']['currency']}'
            products = data_tuple['product_names']  # Список из продуктов

            # Вывод извлеченных данных
            text = (f"<b>Заказ №: {order_id}</b>\n"
                    f"Стоимость заказа:<b> {price}</b>\n\n")


            # Вывод информации о продуктах
            text = f'{text}<b>Продукты в заказе:</b>\n\n'
            for product in products:
                text = f'{text}{product}\n'


            for idtg in LISTOFADMINS:
                await bot.send_message(chat_id=idtg, text = text, parse_mode='HTML')

            await change_status_order(pool,1,number_of_orders)

    except Exception as e:
        logging.error(f"Ошибка при рассылке: {e}")