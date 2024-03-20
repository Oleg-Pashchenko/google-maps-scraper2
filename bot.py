import dotenv
import os

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile

from main import search, execute_query

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Введите запрос")


@dp.message()
async def cmd_start(message: types.Message):
    await message.answer("Идет поиск... Это займет определенное время.")
    execute_query(message.text)
    await message.answer('Result:')
    doc = FSInputFile('answer.xlsx')
    await message.reply_document(doc)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
