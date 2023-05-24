from datetime import datetime, date
import time

from bot_core.weather_api import weather_by_ip, weather_by_input, WeatherData
from bot_core.coordinates import Coordinates
from bot_core.service import take_update, insert_or_update_data_into_db, get_weather_db, get_user_location


async def get_weather_by_ip(location: Coordinates, weather_api_key: str, user_id: int) -> str:
    if not await get_user_location(user_id):
        current_weather = await weather_by_ip(location, weather_api_key)
        await insert_or_update_data_into_db(location, await get_weather(current_weather) + await get_wind_data(current_weather) + await get_sun_time(current_weather), user_id)
        return await get_weather(current_weather) + await get_wind_data(current_weather) + await get_sun_time(current_weather)

    if int(time.time()) - int((await take_update(user_id)).timestamp()) > 60:
        current_weather = await weather_by_ip(location, weather_api_key)
        await insert_or_update_data_into_db(location, await get_weather(current_weather) + await get_wind_data(current_weather) + await get_sun_time(current_weather), user_id)
        return await get_weather(current_weather) + await get_wind_data(current_weather) + await get_sun_time(current_weather)
    else:
        return await get_weather_db(user_id)


async def get_weather_by_input(weather_api_key: str, location: str) -> str:
    current_weather = await weather_by_input(location, weather_api_key)
    if not current_weather:
        return 'Такого города не существует, проверьте название еще раз'
    return await get_weather(current_weather) + await get_wind_data(current_weather) + await get_sun_time(current_weather)


async def get_weather(current_weather: WeatherData):
    return f'<b>{current_weather.location}</b>\n'\
        f'<b>🕖 Время</b>: {datetime.now().strftime("%H:%M:%S")}, {date.today().strftime("%B %d, %Y")}\n' \
        f'\n' \
        f'<i>🌤 Погода</i>: {current_weather.description.capitalize()}\n'\
        f'<i>🌡 Температура</i>: {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'\
        f'\n'


async def get_wind_data(current_weather: WeatherData) -> str:
    wind_directin_ru = {'North': 'Север',
                        'Northeast': 'Северо-восток',
                        'East': 'Восток',
                        'Southeast': 'Юго-восток',
                        'South': 'Юг',
                        'Southwest': 'Юго-запад',
                        'West': 'Запад',
                        'Northwest': 'Северо-запад'
                        }
    return f'\n<i>💨 Ветер: </i>\n'\
        f'<i>Скорость ветра:</i> {current_weather.wind_speed} м/c\n'\
        f'<i>Направление ветра:</i> {wind_directin_ru[current_weather.wind_derection]}' \
        f'\n'


async def get_sun_time(current_weather: WeatherData) -> str:
    return f'\n<i>🌄 Восход солнца в</i> {current_weather.sunrise.strftime("%H:%M:%S")}\n'\
        f'<i>🌅 Заход солнца в</i> {current_weather.sunset.strftime("%H:%M:%S")}'\
        f'\n'
