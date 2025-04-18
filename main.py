import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from radar import scan_new_memecoins

API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

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
        await asyncio.sleep(300)

async def main():
    asyncio.create_task(run_radar())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())