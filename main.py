import requests
import time
import threading
import telegram
from datetime import datetime
from flask import Flask

app = Flask(__name__)

# === Telegram настройки ===
TOKEN = '8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w'
CHAT_ID = '956286581'
bot = telegram.Bot(token=TOKEN)

# === Уровни BTC и DOGE ===
btc_levels = [78800, 90000, 95000, 100000, 150000]
doge_levels = [0.14, 0.20, 0.25, 0.30]

# === Состояние сигналов с буфером отката ===
triggered = {
    "btc": {},
    "doge": {}
}
buffer_pct = 0.005  # 0.5%

# === CoinGecko API ===
def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin&vs_currencies=usd"
    try:
        res = requests.get(url).json()
        btc = res['bitcoin']['usd']
        doge = res['dogecoin']['usd']
        return btc, doge
    except:
        return None, None

# === Катя отправляет сообщение ===
def send_signal(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")
    bot.send_message(chat_id=CHAT_ID, text=f"⚠️ {msg}")

# === Логика отслеживания ===
def monitor():
    send_signal("Система на связи. Катя следит.")
    while True:
        btc_price, doge_price = get_prices()
        if not btc_price or not doge_price:
            time.sleep(30)
            continue

        # === BTC ===
        for lvl in btc_levels:
            buf = lvl * buffer_pct
            if btc_price >= lvl and not triggered["btc"].get(lvl, False):
                send_signal(f"BTC достиг уровня ${lvl:,}")
                triggered["btc"][lvl] = True
            elif btc_price < lvl - buf and triggered["btc"].get(lvl, False):
                triggered["btc"][lvl] = False

        # === DOGE ===
        for lvl in doge_levels:
            buf = lvl * buffer_pct
            if doge_price >= lvl and not triggered["doge"].get(lvl, False):
                send_signal(f"DOGE достиг уровня ${lvl}")
                triggered["doge"][lvl] = True
            elif doge_price < lvl - buf and triggered["doge"].get(lvl, False):
                triggered["doge"][lvl] = False

        time.sleep(60)

# === Flask-заглушка для Render ===
@app.route('/')
def index():
    return "Катя онлайн. Бот работает."

if __name__ == '__main__':
    t = threading.Thread(target=monitor)
    t.start()
    app.run(host='0.0.0.0', port=10000)
