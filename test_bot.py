import telegram

TOKEN = '8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w'
CHAT_ID = '956286581'

bot = telegram.Bot(token=TOKEN)
bot.send_message(chat_id=CHAT_ID, text="Проверка связи. Катя здесь.")
