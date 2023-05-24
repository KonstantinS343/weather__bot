from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

BUTTON_LOCATION = InlineKeyboardButton(
    'Погода в другом городе',
    callback_data='location')
BUTTON_CANCEL = InlineKeyboardButton('Отмена', callback_data='cancel')
BUTTON_CURRENT_WEATHER = InlineKeyboardButton(
    'Текущая погода', callback_data='weather')

BUTTON_GET_LOCATION = ReplyKeyboardMarkup(resize_keyboard=True)
GET_LOCATION = KeyboardButton('📍 Моё местоположение', request_location=True)
BUTTON_GET_LOCATION.add(GET_LOCATION)

WEATHER = InlineKeyboardMarkup().add(BUTTON_CURRENT_WEATHER).add(BUTTON_LOCATION)
HELP = InlineKeyboardMarkup().add(BUTTON_CURRENT_WEATHER).add(BUTTON_LOCATION)
LOCATION = InlineKeyboardMarkup().add(BUTTON_CANCEL)
CURRENT_WEATHER = InlineKeyboardMarkup().add(
    BUTTON_CURRENT_WEATHER).add(BUTTON_LOCATION)
