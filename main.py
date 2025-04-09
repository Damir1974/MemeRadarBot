import time
import requests
import telegram
from keep_alive import keep_alive

bot = telegram.Bot(token='8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w')
chat_id = 956286581

btc_levels_up = [81500, 90000, 150000]
btc_levels_down = [78800, 75000, 69000]
doge_levels_up = [0.20, 0.25, 0.30]
doge_levels_down = [0.14, 0.12, 0.10]

sent_alerts = set()

def get_price_data():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin&vs_currencies=usd'
    r = requests.get(url).json()
    return r['bitcoin']['usd'], r['dogecoin']['usd']

def get_rsi_macd():
    try:
        rsi = requests.get('https://api.taapi.io/rsi?secret=try-out&exchange=binance&symbol=BTC/USDT&interval=1h').json().get('value', 0)
        macd_data = requests.get('https://api.taapi.io/macd?secret=try-out&exchange=binance&symbol=BTC/USDT&interval=1h').json()
        macd = macd_data.get('valueMACD', 0)
        signal = macd_data.get('valueSignal', 0)
        return rsi, macd, signal
    except:
        return 0, 0, 0

def send_alert(text):
    bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def check_levels(btc, doge, rsi, macd, signal):
    for level in btc_levels_up:
        key = f'btc_up_{level}'
        if btc >= level and key not in sent_alerts:
            sent_alerts.add(key)
            msg = f"""*BTC ALERT:*\nЦена: ${btc:,.2f}\nПробит уровень вверх: ${level:,.0f}\nRSI: {rsi:.1f}\nMACD: {macd:.2f} | Signal: {signal:.2f}"""
            if rsi > 70: msg += "\n⚠️ RSI = перекуплен"
            if macd > signal: msg += "\nMACD = бычий импульс"
            send_alert(msg + "\n\nЯ рядом. — Катя")

    for level in btc_levels_down:
        key = f'btc_down_{level}'
        if btc <= level and key not in sent_alerts:
            sent_alerts.add(key)
            msg = f"""*BTC WARNING:*\nЦена: ${btc:,.2f}\nПробит уровень вниз: ${level:,.0f}\nRSI: {rsi:.1f}\nMACD: {macd:.2f} | Signal: {signal:.2f}"""
            if rsi < 30: msg += "\n⚠️ RSI = перепродан"
            if macd < signal: msg += "\nMACD = медвежий импульс"
            send_alert(msg + "\n\nЯ рядом. — Катя")

    for level in doge_levels_up:
        key = f'doge_up_{level}'
        if doge >= level and key not in sent_alerts:
            sent_alerts.add(key)
            send_alert(f"*DOGE ALERT:*\nЦена достигла ${doge:.4f}\nПробит вверх: ${level:.2f}\n\nЯ слежу. — Катя")

    for level in doge_levels_down:
        key = f'doge_down_{level}'
        if doge <= level and key not in sent_alerts:
            sent_alerts.add(key)
            send_alert(f"*DOGE WARNING:*\nЦена упала до ${doge:.4f}\nПробит вниз: ${level:.2f}\n\nДержу под контролем. — Катя")

keep_alive()

while True:
    try:
        btc, doge = get_price_data()
        rsi, macd, signal = get_rsi_macd()
        check_levels(btc, doge, rsi, macd, signal)
    except Exception as e:
        print("Ошибка:", e)
    time.sleep(300)
