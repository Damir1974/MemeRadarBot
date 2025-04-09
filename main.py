import time
import requests
import telegram

bot = telegram.Bot(token='8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w')
chat_id = 956286581  # только тебе

def get_btc_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    r = requests.get(url)
    return r.json()['bitcoin']['usd']

def send_signal(price):
    message = f"""*BTC ALERT:*
Цена: ${price:,.2f}
BTC пробил ключевой уровень.

Я рядом. — Катя"""
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

while True:
    try:
        price = get_btc_price()
        if price >= 81500:  # можешь поменять уровень сам
            send_signal(price)
    except Exception as e:
        print("Ошибка:", e)
    
    time.sleep(300)  # проверка каждые 5 минут
