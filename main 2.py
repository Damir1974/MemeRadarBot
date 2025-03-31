import telebot
import time
import threading
from config import TOKEN, CHAT_ID
from radar import fetch_memecoins, format_memecoin_list

bot = telebot.TeleBot(TOKEN)

def radar_loop():
    while True:
        memecoins = fetch_memecoins()
        message = format_memecoin_list(memecoins)
        try:
            bot.send_message(CHAT_ID, message)
        except Exception as e:
            print("Ошибка отправки сообщения:", e)
        time.sleep(300)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Бот активен! MemeRadarBot ждёт команду.")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "✅ Ping получен! Бот работает без сбоев.")

@bot.message_handler(commands=['top'])
def top(message):
    memecoins = fetch_memecoins()
    msg = format_memecoin_list(memecoins)
    bot.send_message(message.chat.id, msg)

def run_bot():
    thread = threading.Thread(target=radar_loop)
    thread.daemon = True
    thread.start()
    print("Бот запущен и ожидает команды...")
    bot.polling(non_stop=True)

if __name__ == '__main__':
    run_bot()