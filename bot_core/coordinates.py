from typing import NamedTuple, Dict
import aiohttp

class Coordinates(NamedTuple):
    latitude: float
    longitude: float