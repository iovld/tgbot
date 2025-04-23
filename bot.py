import os
import time
import datetime
import requests
from telegram import Bot

INS_API_KEY = os.getenv("INS_API_KEY")
INS_PASSWORD = os.getenv("INS_PASSWORD")
INS_DOMAIN = os.getenv("INS_DOMAIN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def get_orders():
    url = f"https://{INS_API_KEY}:{INS_PASSWORD}@{INS_DOMAIN}/admin/orders.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching orders:", e)
        return []

def send_order_notification(order):
    message = f"Новый заказ №{order['number']}\n\n"
    message += f"Имя клиента: {order['client'].get('first_name', '')}\n"
    message += f"Фамилия клиента: {order['client'].get('last_name', '')}\n"
    message += f"Адрес заказа: {order['shipping_address'].get('address', '')}\n"
    message += f"Способ доставки: {order.get('delivery_variant_name', '')}\n"
    message += "Состав заказа:\n"
    for idx, item in enumerate(order['order_lines'], 1):
        message += f"  {idx}. {item['title']}. Кол-во: {item['quantity']} шт. Цена: {item['price']} руб\n"
    message += f"Способ оплаты: {order.get('payment_gateway_name', '')}\n"
    message += f"Сумма: {order['total_price']} руб\n"
    bot.send_message(chat_id=CHAT_ID, text=message)

def run():
    seen = set()
    while True:
        orders = get_orders()
        for order in orders:
            if order["id"] not in seen:
                send_order_notification(order)
                seen.add(order["id"])
        time.sleep(60)

if __name__ == "__main__":
    run()
