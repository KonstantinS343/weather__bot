from bot_core.weather_api import weather_by_ip, weather_by_input
from bot_core.coordinates import get_coordinates

async def get_weather_by_ip(weather_api_key: str) -> str:
    current_weather = await weather_by_ip(await get_coordinates(), weather_api_key)
    return f'{current_weather.location}, {current_weather.description.capitalize()}\n'\
        f'Температура {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'

async def get_weather_by_input(weather_api_key: str, location: str) -> str:
    current_weather = await weather_by_input(location, weather_api_key)
    return f'{current_weather.location}, {current_weather.description.capitalize()}\n'\
        f'Температура {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'

async def get_wind_data(weather_api_key: str) -> str:
    current_weather = await weather_by_ip(await get_coordinates(), weather_api_key)
    wind_directin_ru = {'North': 'Север',
                        'Northeast':'Северо-восток',
                        'East':'Восток',
                        'Southeast':'Юго-восток',
                        'South':'Юг',
                        'Southwest':'Юго-запад',
                        'West':'Запад',
                        'Northwest':'Северо-запад'
                        }
    return f'Скорость ветра {current_weather.wind_speed} м/c\n'\
        f'Направление ветра {wind_directin_ru[current_weather.wind_derection]}'
        
async def get_sun_time(weather_api_key: str) -> str:
    current_weather = await weather_by_ip(await get_coordinates(), weather_api_key)
    return f'Восход солнца в {current_weather.sunrise}\n'\
        f'Заход солнца в {current_weather.sunset}'