import logging

from config import TOKEN
from aiogram import Bot, Dispatcher, executor


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
