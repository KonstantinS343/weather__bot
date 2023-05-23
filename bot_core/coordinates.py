from typing import NamedTuple, Dict
import aiohttp

class Coordinates(NamedTuple):
    latitude: float
    longitude: float
    
async def _get_ip_data() -> Dict[str, str]:
    url = 'http://ipinfo.io/json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            ip_data = await response.json()
            return ip_data

async def get_coordinates()-> Coordinates:
    ip_data = await _get_ip_data()
    latitude, longitude = map(float, ip_data['loc'].split(','))
    return Coordinates(latitude=latitude, longitude=longitude)