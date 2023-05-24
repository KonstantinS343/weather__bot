from enum import IntEnum
from typing import NamedTuple, Dict
from datetime import datetime
import aiohttp
import json

from bot_core.coordinates import Coordinates


class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315


class WeatherData(NamedTuple):
    location: str
    temperature: float
    temperature_feeling: float
    description: str
    wind_speed: float
    wind_derection: int
    sunset: datetime
    sunrise: datetime


async def weather_by_ip(coordinates: Coordinates, weather_api_key: str) -> WeatherData:
    openweather = await _openweather_response_by_ip(coordinates, weather_api_key)
    weather_in_dict = json.loads(openweather)
    weather = _parse_response_openweather(weather_in_dict)
    return weather


async def weather_by_input(location: str, weather_api_key: str) -> WeatherData | None:
    openweather = await _openweather_response_by_input(location, weather_api_key)
    weather_in_dict = json.loads(openweather)
    if weather_in_dict['cod'] == '404':
        return None
    weather = _parse_response_openweather(weather_in_dict)
    return weather


async def _openweather_response_by_input(location: str, weather_api_key: str) -> str:
    openweather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&lang=ru&units=metric&lang=ru&appid={weather_api_key}'
    async with aiohttp.ClientSession() as session:
        async with session.get(openweather_url) as response:
            weather_response = await response.text()
            return weather_response


async def _openweather_response_by_ip(coordinates: Coordinates, weather_api_key: str) -> str:
    openweather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={coordinates.latitude}&lon={coordinates.longitude}&lang=ru&appid={weather_api_key}&units=metric'
    async with aiohttp.ClientSession() as session:
        async with session.get(openweather_url) as response:
            weather_response = await response.text()
            return weather_response


def _parse_response_openweather(weather: Dict[str, str]) -> WeatherData:
    return WeatherData(
        location=_parse_location(weather),
        temperature=_parse_temperature(weather),
        temperature_feeling=_parse_temperature_feeling(weather),
        description=_parse_description(weather),
        wind_speed=_parse_wind_speed(weather),
        wind_derection=_parse_wind_derection(weather),
        sunrise=_parse_sun_time(weather, 'sunrise'),
        sunset=_parse_sun_time(weather, 'sunset')
    )


def _parse_location(weather: Dict[str, str]) -> str:
    return weather['name']


def _parse_temperature(weather: Dict[str, str]) -> float:
    return weather['main']['temp']


def _parse_temperature_feeling(weather: Dict[str, str]) -> float:
    return weather['main']['feels_like']


def _parse_description(weather: Dict[str, str]) -> str:
    return weather['weather'][0]['description']


def _parse_wind_speed(weather: Dict[str, str]) -> float:
    return weather['wind']['speed']


def _parse_wind_derection(weather: Dict[str, str]) -> int:
    degree = weather['wind']['deg']
    degree = round(degree / 45) * 45
    if degree == 360:
        degree = 0
    return WindDirection(degree).name


def _parse_sun_time(weather: Dict[str, str], time_type: str) -> datetime:
    return datetime.fromtimestamp(weather['sys'][time_type])
