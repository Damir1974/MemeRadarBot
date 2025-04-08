import requests
import time
import telegram
from datetime import datetime

# === Настройки ===
TOKEN = '8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w'
CHAT_ID = '956286581'  # @HuiDungan

btc_levels = [78800, 90000, 95000, 100000, 150000]
doge_levels = [0.14, 0.20, 0.25, 0.30]

headers = {"accept": "application/json"}
bot = telegram.Bot(token=TOKEN)

triggered = {
    "btc": set(),
    "doge": set()
}

def send_signal(text):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")
    bot.send_message(chat_id=CHAT_ID, text=f"⚠️ {text}")

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cdogecoin&vs_currencies=usd"
    try:
        res = requests.get(url, headers=headers).json()
        btc = res["bitcoin"]["usd"]
        doge = res["dogecoin"]["usd"]
        return btc, doge
    except Exception as e:
        print("Ошибка при получении цен:", e)
        return None, None

def run():
    while True:
        btc_price, doge_price = get_prices()
        if btc_price and doge_price:
            for lvl in btc_levels:
                if btc_price >= lvl and lvl not in triggered["btc"]:
                    send_signal(f"BTC достиг уровня ${lvl:,}")
                    triggered["btc"].add(lvl)
                elif btc_price < lvl and lvl in triggered["btc"]:
                    triggered["btc"].remove(lvl)

            for lvl in doge_levels:
                if doge_price >= lvl and lvl not in triggered["doge"]:
                    send_signal(f"DOGE достиг уровня ${lvl}")
                    triggered["doge"].add(lvl)
                elif doge_price < lvl and lvl in triggered["doge"]:
                    triggered["doge"].remove(lvl)

        time.sleep(60)

if __name__ == "__main__":
    send_signal("Система на связи. Катя следит.")
    run()
