import asyncio
import logging
from aiogram import Bot, Dispatcher
from radar import scan_new_memecoins

API_TOKEN = "8067243807:AAH3xot3O0iEx_c1BSWPwAMrqf-0OZ-lB1w"
CHAT_ID = "956286581"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def run_radar():
    while True:
        try:
            message = await scan_new_memecoins()
            if message:
                await bot.send_message(CHAT_ID, message)
        except Exception as e:
            print(f"Ошибка в радаре: {e}")
        await asyncio.sleep(300)  # каждые 5 минут

async def main():
    asyncio.create_task(run_radar())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
