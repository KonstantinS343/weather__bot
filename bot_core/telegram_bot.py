import os
import datetime
import requests
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from dotenv import load_dotenv

from bot_core.message_type import get_weather_by_ip

load_dotenv(os.path.dirname(__file__) + '/.env')
logging.basicConfig(level=logging.INFO)

def start_point():
    print('Bot is running!')
    executor.start_polling(dp)

bot = Bot(token=os.getenv('TELEGRAM'))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(text=await get_weather_by_ip(os.getenv('WEATHERAPI')))