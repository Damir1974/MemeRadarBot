import requests
import time
import threading
from datetime import datetime
from flask import Flask
import telebot
from telebot import types

TOKEN = '8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w'
CHAT_ID = '956286581'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

btc_levels = [78800, 90000, 95000, 100000, 150000]
doge_levels = [0.14, 0.20, 0.25, 0.30]
triggered = {"btc": {}, "doge": {}}
btc_history = []
buffer_pct = 0.005

def send_signal(text):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {text}")
    bot.send_message(CHAT_ID, f"⚠️ {text}")

def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin&vs_currencies=usd"
        res = requests.get(url).json()
        return res["bitcoin"]["usd"], res["dogecoin"]["usd"]
    except:
        return None, None

def calculate_indicators(prices):
    if len(prices) < 26:
        return None

    ma10 = sum(prices[-10:]) / 10
    ma50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else None
    ma200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else None

    gains = [max(prices[i+1] - prices[i], 0) for i in range(-15, -1)]
    losses = [abs(min(prices[i+1] - prices[i], 0)) for i in range(-15, -1)]
    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 100

    ema12 = sum(prices[-12:]) / 12
    ema26 = sum(prices[-26:]) / 26
    macd = ema12 - ema26

    return round(rsi, 2), round(macd, 2), (ma10, ma50, ma200)

def monitor():
    send_signal("Система на связи. Катя следит.")
    while True:
        btc, doge = get_prices()
        if not btc or not doge:
            time.sleep(30)
            continue

        btc_history.append(btc)
        if len(btc_history) > 300:
            btc_history.pop(0)

        for lvl in btc_levels:
            buf = lvl * buffer_pct
            if btc >= lvl and not triggered["btc"].get(lvl):
                send_signal(f"BTC достиг уровня ${lvl:,}")
                triggered["btc"][lvl] = True
            elif btc < lvl - buf and triggered["btc"].get(lvl):
                triggered["btc"][lvl] = False

        for lvl in doge_levels:
            buf = lvl * buffer_pct
            if doge >= lvl and not triggered["doge"].get(lvl):
                send_signal(f"DOGE достиг уровня ${lvl}")
                triggered["doge"][lvl] = True
            elif doge < lvl - buf and triggered["doge"].get(lvl):
                triggered["doge"][lvl] = False

        indicators = calculate_indicators(btc_history)
        if indicators:
            rsi, macd, (ma10, ma50, ma200) = indicators

            if rsi < 30:
                send_signal(f"RSI = {rsi} — рынок перепродан. Возможен разворот.")
            elif rsi > 70:
                send_signal(f"RSI = {rsi} — рынок перегрет. Возможен откат.")

            if macd > 0:
                send_signal(f"MACD = {macd} — бычий сигнал.")
            elif macd < 0:
                send_signal(f"MACD = {macd} — медвежий сигнал.")

            if ma10 and ma50:
                if ma10 > ma50:
                    send_signal("MA(10) пересёк MA(50) вверх — бычий сигнал.")
                elif ma10 < ma50:
                    send_signal("MA(10) ниже MA(50) — давление вниз.")

        time.sleep(300)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🔥 Горячие мемкоины", "📊 Альты (CoinGecko)")
    bot.send_message(message.chat.id, "Привет! Катя следит за рынком.", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "🔥 Горячие мемкоины")
def handle_memecoins(message):
    bot.send_message(message.chat.id, "Сканирую горячие мемкоины на CoinGecko...")

@bot.message_handler(func=lambda m: m.text == "📊 Альты (CoinGecko)")
def handle_alts(message):
    bot.send_message(message.chat.id, "Актуальные альты: ETH, SOL, LINK, RNDR, ARB, SUI")

@app.route('/')
def index():
    return "Катя онлайн. Бот работает."

if __name__ == '__main__':
    t = threading.Thread(target=monitor)
    t.start()
    app.run(host='0.0.0.0', port=10000)
