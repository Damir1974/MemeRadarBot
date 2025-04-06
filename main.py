from telegram.ext import Updater, CommandHandler
from config import TOKEN
from radar import start_radar, handle_command

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я MemeRadarBot. Отслеживаю новые мемкоины!")

def check(update, context):
    handle_command("/check")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check))

    start_radar()  # запускает авто-радар в фоне
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
