from bot_core.weather_api import weather_by_ip, weather_by_input
from bot_core.coordinates import  Coordinates

async def get_weather_by_ip(location: Coordinates, weather_api_key: str) -> str:
    current_weather = await weather_by_ip(location, weather_api_key)
    return f'<b>{current_weather.location}</b>:\n'\
        f'\n' \
        f'<i>🌤 Погода</i>: {current_weather.description.capitalize()}\n'\
        f'<i>🌡 Температура</i>: {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'

async def get_weather_by_input(weather_api_key: str, location: str) -> str:
    current_weather = await weather_by_input(location, weather_api_key)
    return f'<b>{current_weather.location}</b>:\n'\
        f'\n' \
        f'<i>🌤 Погода</i>: {current_weather.description.capitalize()}\n'\
        f'<i>🌡 Температура</i>: {current_weather.temperature}°C, ощущается как {current_weather.temperature_feeling}°C'

async def get_wind_data(location: Coordinates, weather_api_key: str) -> str:
    current_weather = await weather_by_ip(location, weather_api_key)
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
        
async def get_sun_time(location: Coordinates, weather_api_key: str) -> str:
    current_weather = await weather_by_ip(location, weather_api_key)
    return f'<i>🌄 Восход солнца в</i> {current_weather.sunrise}\n'\
        f'<i>🌅 Заход солнца в</i> {current_weather.sunset}'