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


from bot_core.message_type import get_weather_by_ip, get_weather_by_input, \
    get_wind_data, get_sun_time
import bot_core.bot_buttons as button

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

@dp.message_handler(commands=['start', 'weather'])
async def start_command(message: types.Message):
    await message.answer(text=await get_weather_by_ip(os.getenv('WEATHERAPI')), reply_markup = button.WEATHER)
    
@dp.message_handler(commands=['location'])
async def input_location(message: types.Message):
    await Location.location.set()
    await message.answer('Название города?', reply_markup = button.LOCATION)

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

@dp.message_handler(state=Location.location)
async def process_location(message: types.Message, state: FSMContext):
    city = message.text.lower()
    await message.answer(text=await get_weather_by_input(os.getenv('WEATHERAPI'), city), reply_markup= button.CURRENT_WEATHER)
    await state.finish()
    
@dp.message_handler(commands=['wind'])
async def wind(message: types.Message):
    await message.answer(text=await get_wind_data(os.getenv('WEATHERAPI')), reply_markup = button.WIND)

@dp.message_handler(commands=['suntime'])
async def sun_time(message: types.Message):
    await message.answer(text=await get_sun_time(os.getenv('WEATHERAPI')), reply_markup = button.SUN_TIME)
  
@dp.callback_query_handler(text='weather')
async def callback_weather(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text=await get_weather_by_ip(os.getenv('WEATHERAPI')), reply_markup = button.WEATHER)
    await callback_query.answer()
  
@dp.callback_query_handler(text='wind')
async def callback_wind(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text=await get_wind_data(os.getenv('WEATHERAPI')), reply_markup = button.WIND)
    await callback_query.answer()


@dp.callback_query_handler(text='suntime')
async def callback_sun_time(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text=await get_sun_time(os.getenv('WEATHERAPI')), reply_markup = button.SUN_TIME)
    await callback_query.answer()

@dp.message_handler(commands='help')
async def show_help_message(message: types.Message):
    await message.answer(text=f'Этот бот показывает текущую погоду по IP адресу.' 
                         'Кроме этого может показать погоду а месте,которе запросил пользователь.',
                         reply_markup=button.HELP)

@dp.callback_query_handler(text='location')
async def callback_input_location(callback_query: types.CallbackQuery):
    await Location.location.set()
    await callback_query.message.answer('Название города?', reply_markup = button.LOCATION)
    await callback_query.answer()

@dp.callback_query_handler(state='*', text='cancel')
@dp.callback_query_handler(Text(equals='cancel', ignore_case=True), state='*')
async def callback_cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await callback_query.message.answer(text=await get_weather_by_ip(os.getenv('WEATHERAPI')), reply_markup = button.WEATHER)
    await callback_query.answer()
    await state.finish()