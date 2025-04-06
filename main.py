import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from radar import check_new_memecoins
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я MemeRadarBot. Отслеживаю новые мемкоины!")

# Команда /check
@dp.message_handler(commands=['check'])
async def handle_check(message: types.Message):
    result = check_new_memecoins()
    await message.reply(result)

# Фоновая задача: проверка каждые 5 минут
async def auto_check():
    await bot.wait_until_ready()  # Только если бот будет использовать webhook
    while True:
        try:
            result = check_new_memecoins()
            await bot.send_message(chat_id=956286581, text="Авто-проверка:\n" + result)
        except Exception as e:
            logging.error(f"Ошибка в авто-проверке: {e}")
        await asyncio.sleep(300)  # 5 минут

# Запуск
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_check())
    executor.start_polling(dp, skip_updates=True)
