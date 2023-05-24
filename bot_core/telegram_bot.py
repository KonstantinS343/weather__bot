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
from bot_core.coordinates import Coordinates
from bot_core.service import db_init, insert_data_into_db

load_dotenv(os.path.dirname(__file__) + '/.env')
logging.basicConfig(level=logging.INFO)

def start_point():
    print('Bot is running!')
    executor.start_polling(dp)

class Location(StatesGroup):
    location = State()

LOCATION = Coordinates(0.0, 0.0)
    
storage = MemoryStorage()
bot = Bot(token=os.getenv('TELEGRAM'), parse_mode="html")
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['weather'])
async def start_command(message: types.Message):
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather', message.chat.id)
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind', message.chat.id)
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime', message.chat.id)
        await message.answer(text=weather, reply_markup = button.WEATHER)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, message.chat.id)
    else:
        await message.answer('Поделитесь своим местоположением')
    
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
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather')
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind')
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime')
        await message.answer(text=wind_weather, reply_markup = button.WIND)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, message.chat.id)
    else:
        await message.answer('Поделитесь своим местоположением')

@dp.message_handler(commands=['suntime'])
async def sun_time(message: types.Message):
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather')
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind')
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime')
        await message.answer(text=sun_time_weather, reply_markup = button.SUN_TIME)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, message.chat.id)
    else:
        await message.answer('Поделитесь своим местоположением')
  
@dp.callback_query_handler(text='weather')
async def callback_weather(callback_query: types.CallbackQuery):
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather')
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind')
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime')
        await callback_query.message.answer(text=weather, reply_markup = button.WEATHER)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, callback_query.message.chat.id)
    else:
        await callback_query.message.answer('Поделитесь своим местоположением')
    await callback_query.answer()
  
@dp.callback_query_handler(text='wind')
async def callback_wind(callback_query: types.CallbackQuery):
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather')
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind')
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime')
        await callback_query.message.answer(text=wind_weather, reply_markup = button.WIND)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, callback_query.message.chat.id)
    else:
        await callback_query.message.answer('Поделитесь своим местоположением')
    await callback_query.answer()


@dp.callback_query_handler(text='suntime')
async def callback_sun_time(callback_query: types.CallbackQuery):
    if not LOCATION.latitude == 0.0 and not LOCATION.longitude == 0.0:
        weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'weather')
        wind_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'wind')
        sun_time_weather = await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI'), 'suntime')
        await callback_query.message.answer(text=sun_time_weather, reply_markup = button.SUN_TIME)
        await insert_data_into_db(LOCATION, weather, wind_weather, sun_time_weather, callback_query.message.chat.id)
    else:
        await callback_query.message.answer('Поделитесь своим местоположением')
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
    await callback_query.message.answer(text=await get_weather_by_ip(LOCATION, os.getenv('WEATHERAPI')), reply_markup = button.WEATHER)
    await callback_query.answer()
    await state.finish()

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    temp = Coordinates(latitude=message.location.latitude, longitude=message.location.longitude)
    global LOCATION
    LOCATION = temp
    logging.info(LOCATION.latitude)
    logging.info(LOCATION.longitude)
    await message.answer(text=await get_weather_by_ip(Coordinates(latitude=message.location.latitude, longitude=message.location.longitude),
                                                      os.getenv('WEATHERAPI'), 'weather', message.chat.id), reply_markup = button.WEATHER)

@dp.message_handler(commands=['start'])
async def cmd_locate_me(message: types.Message):
    await db_init(logging)
    reply = "Нажмите на кнопку,чтобы поделить своим местоположением"
    await message.answer(reply, reply_markup=button.BUTTON_GET_LOCATION)



    