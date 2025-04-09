import requests
import time
import threading
from telegram import Bot
from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)

def get_memecoins():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        keywords = ['pepe', 'doge', 'shiba', 'floki', 'inu', 'meme', 'baby', 'elon', 'cat', 'frog', 'ghibli', 'cz', 'banana']
        memecoins = [coin for coin in data if any(k in coin['id'] or k in coin['name'].lower() for k in keywords)]
        return memecoins[:10]
    except Exception as e:
        print(f"Ошибка при получении мемкоинов: {e}")
        return []

def get_top_alts():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False
        }, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при получении топ-альтов: {e}")
        return []

def format_coins(coins):
    return '\n'.join([f"{coin['name']} (${coin['current_price']})" for coin in coins])

def send_update():
    memecoins = get_memecoins()
    alts = get_top_alts()

    if memecoins:
        message = "🔥 Горячие мемкоины:\n" + format_coins(memecoins)
        bot.send_message(chat_id=CHAT_ID, text=message)

    if alts:
        message = "📊 Альты (CoinGecko):\n" + format_coins(alts)
        bot.send_message(chat_id=CHAT_ID, text=message)

def radar_loop():
    while True:
        send_update()
        time.sleep(300)  # каждые 5 минут

def start_radar():
    thread = threading.Thread(target=radar_loop)
    thread.daemon = True
    thread.start()
