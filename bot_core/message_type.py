from datetime import datetime

from bot_core.weather_api import weather_by_ip, weather_by_input, WeatherData
from bot_core.coordinates import  Coordinates
from bot_core.service import take_update

async def get_weather_by_ip(location: Coordinates, weather_api_key: str, weather_type: str, user_id: int) -> str:
    if await take_update(user_id) - int(datetime.utcnow().timestamp()) > 60:
        current_weather = await weather_by_ip(location, weather_api_key)
    else:
        pass
        
    match weather_type:
        case 'weather':
            return await get_weather(current_weather)
        case 'wind':
            return await get_wind_data(current_weather)
        case 'suntime':
            await get_sun_time(current_weather)

async def get_weather_by_input(weather_api_key: str, location: str) -> str:
    current_weather = await weather_by_input(location, weather_api_key)
    return f'<b>{current_weather.location}</b>:\n'\
        f'\n' \
        f'<i>🌤 Погода</i>: {current_weather.description.capitalize()}\n'\
        f'<i>🌡 Температура</i>: {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'
        
async def get_weather(current_weather: WeatherData):
    return f'<b>{current_weather.location}</b>:\n'\
                f'\n' \
                f'<i>🌤 Погода</i>: {current_weather.description.capitalize()}\n'\
                f'<i>🌡 Температура</i>: {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'

async def get_wind_data(current_weather: WeatherData) -> str:
    wind_directin_ru = {'North': 'Север',
                        'Northeast':'Северо-восток',
                        'East':'Восток',
                        'Southeast':'Юго-восток',
                        'South':'Юг',
                        'Southwest':'Юго-запад',
                        'West':'Запад',
                        'Northwest':'Северо-запад'
                        }
    return f'<i>💨 Ветер: </i>\n'\
        f'<i>Скорость ветра:</i> {current_weather.wind_speed} м/c\n'\
        f'<i>Направление ветра:</i> {wind_directin_ru[current_weather.wind_derection]}'
        
async def get_sun_time(current_weather: WeatherData) -> str:
    return f'<i>🌄 Восход солнца в</i> {current_weather.sunrise}\n'\
        f'<i>🌅 Заход солнца в</i> {current_weather.sunset}'
