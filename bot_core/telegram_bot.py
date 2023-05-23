import os
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor 
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from bot_core.message_type import get_weather_by_ip, get_weather_by_input

load_dotenv(os.path.dirname(__file__) + '/.env')
logging.basicConfig(level=logging.INFO)

def start_point():
    print('Bot is running!')
    executor.start_polling(dp)

class Location(StatesGroup):
    location = State()
storage = MemoryStorage()
bot = Bot(token=os.getenv('TELEGRAM'))
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start", 'weather'])
async def start_command(message: types.Message):
    await message.answer(text=await get_weather_by_ip(os.getenv('WEATHERAPI')))
    
@dp.message_handler(commands=["location"])
async def start_command(message: types.Message):
    await Location.location.set()
    await message.answer('Название города?')

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Отменено', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Location.location)
async def process_name(message: types.Message, state: FSMContext):
    city = message.text.lower()
    await message.answer(text=await get_weather_by_input(os.getenv('WEATHERAPI'), city))
    await state.finish()