import aiohttp

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