import aiohttp

from bot_core.weather_api import weather_by_ip
from bot_core.coordinates import get_coordinates

async def get_weather_by_ip(weather_api_key: str) -> str:
    current_weather = await weather_by_ip(await get_coordinates(), weather_api_key)
    return f'{current_weather.location}, {current_weather.description.capitalize()}\n'\
        f'Temperature is {current_weather.temperature}°C, feels like {current_weather.temperature_feeling}°C'