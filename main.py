import logging
from aiogram import Bot, Dispatcher, executor, types
from radar import check_new_memecoins
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я MemeRadarBot. Отслеживаю новые мемкоины!")

@dp.message_handler(commands=['check'])
async def handle_check(message: types.Message):
    result = check_new_memecoins()
    await message.reply(result)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)