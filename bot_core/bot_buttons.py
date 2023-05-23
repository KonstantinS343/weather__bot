from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BUTTON_WEATHER = InlineKeyboardButton('Погода', callback_data='weather')
BUTTON_WIND = InlineKeyboardButton('Ветер', callback_data='wind')
BUTTON_SUN_TIME = InlineKeyboardButton('Восход и Заход', callback_data='suntime')
BUTTON_LOCATION = InlineKeyboardButton('Город', callback_data='location')
BUTTON_CANCEL = InlineKeyboardButton('Отмена', callback_data='cancel')
BUTTON_CURRENT_WEATHER = InlineKeyboardButton('Текущая погода', callback_data='weather')

WEATHER = InlineKeyboardMarkup().add(BUTTON_WIND, BUTTON_SUN_TIME).add(BUTTON_LOCATION)
WIND = InlineKeyboardMarkup().add(BUTTON_WEATHER, BUTTON_SUN_TIME).add(BUTTON_LOCATION)
SUN_TIME = InlineKeyboardMarkup().add(BUTTON_WIND, BUTTON_WEATHER).add(BUTTON_LOCATION)
HELP = InlineKeyboardMarkup().add(BUTTON_WIND, BUTTON_SUN_TIME, BUTTON_WEATHER).add(BUTTON_LOCATION)
LOCATION = InlineKeyboardMarkup().add(BUTTON_CANCEL)
CURRENT_WEATHER = InlineKeyboardMarkup().add(BUTTON_CURRENT_WEATHER)

