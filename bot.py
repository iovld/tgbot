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

def first_name = order.get('client', {}).get('first_name', '—')
last_name = order.get('client', {}).get('last_name', '—')
address = order.get('shipping_address', {}).get('address', '—')
delivery = order.get('delivery_variant_name', '—')
payment = order.get('payment_gateway_name', '—')

message = f"Новый заказ №{order['number']}\n\n"
message += f"Имя клиента: {first_name}\n"
message += f"Фамилия клиента: {last_name}\n"
message += f"Адрес заказа: {address}\n"
message += f"Способ доставки: {delivery}\n"
message += "Состав заказа:\n"

for idx, item in enumerate(order.get('order_lines', []), 1):
    title = item.get('title', '—')
    quantity = item.get('quantity', '—')
    price = item.get('price') or item.get('sale_price') or item.get('full_price') or '—'
    message += f"  {idx}. {title}. Кол-во: {quantity} шт. Цена: {price} руб\n"

message += f"Способ оплаты: {payment}\n"
message += f"Сумма: {order.get('total_price', '—')} руб\n"


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
