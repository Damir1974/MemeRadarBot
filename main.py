import requests
import time
import threading
import telegram
from datetime import datetime
from flask import Flask

app = Flask(__name__)

# === Telegram ===
TOKEN = '8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w'
CHAT_ID = '956286581'
bot = telegram.Bot(token=TOKEN)

# === История цен для RSI, MACD, MA ===
btc_history = []

# === Отправка сигнала ===
def send_signal(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")
    bot.send_message(chat_id=CHAT_ID, text=f"⚠️ {msg}")

# === Получение цены BTC ===
def get_btc_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
        res = requests.get(url).json()
        return res['bitcoin']['usd']
    except:
        return None

# === Расчёты RSI, MACD, MA (простая эмуляция) ===
def calculate_indicators(prices):
    if len(prices) < 26:
        return None, None, None

    close = prices[-1]
    ma10 = sum(prices[-10:]) / 10
    ma50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else None
    ma200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else None

    # RSI
    gains = [max(prices[i+1] - prices[i], 0) for i in range(-15, -1)]
    losses = [abs(min(prices[i+1] - prices[i], 0)) for i in range(-15, -1)]
    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 100

    # MACD (разница между EMA12 и EMA26, примитивная)
    ema12 = sum(prices[-12:]) / 12
    ema26 = sum(prices[-26:]) / 26
    macd = ema12 - ema26

    return round(rsi, 2), round(macd, 2), (ma10, ma50, ma200)

# === Главный мониторинг ===
def monitor():
    send_signal("Система на связи. Катя следит.")
    while True:
        price = get_btc_price()
        if not price:
            time.sleep(30)
            continue

        btc_history.append(price)
        if len(btc_history) > 300:
            btc_history.pop(0)

        indicators = calculate_indicators(btc_history)
        if indicators:
            rsi, macd, (ma10, ma50, ma200) = indicators

            # === RSI ===
            if rsi < 30:
                send_signal(f"RSI = {rsi} — рынок перепродан. Возможен разворот вверх.")
            elif rsi > 70:
                send_signal(f"RSI = {rsi} — рынок перегрет. Возможен откат.")

            # === MACD ===
            if macd > 0:
                send_signal(f"MACD = {macd} — бычий сигнал.")
            elif macd < 0:
                send_signal(f"MACD = {macd} — медвежье давление.")

            # === MA пересечения (упрощённо) ===
            if ma10 and ma50 and ma10 > ma50:
                send_signal("MA(10) пересёк MA(50) вверх — краткосрочный бычий сигнал.")
            elif ma10 and ma50 and ma10 < ma50:
                send_signal("MA(10) ниже MA(50) — краткосрочное давление вниз.")

        time.sleep(300)  # анализ каждые 5 минут

# === Flask-заглушка для Render ===
@app.route('/')
def index():
    return "Катя работает. Анализ ведётся."

if __name__ == '__main__':
    t = threading.Thread(target=monitor)
    t.start()
    app.run(host='0.0.0.0', port=10000)
