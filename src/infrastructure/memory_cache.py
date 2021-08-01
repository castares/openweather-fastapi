from datetime import datetime, timedelta
from schemas.weather import WeatherRequest, WeatherResponse
from typing import Optional, Tuple, Protocol
from pydantic import BaseModel


class Cache(Protocol):
    def get_cached_values(self) -> Optional[dict]:
        ...

    def save_to_cache(self) -> dict:
        ...


class RequestMemoryCache(BaseModel):
    _instance = None
    _vals: dict = {}
    lifetime_in_hours = 1.0

    def __new__(cls):
        """
        Singleton implementation, to ensure only one Cache instance exists.
        """
        if cls._instance is None:
            cls._instance = super(RequestMemoryCache, cls).__new__(cls)
        return cls._instance

    def _build_key(self, object):
        key = hash(str(object))
        return key

    def get_cached_values(self, request_dict: dict) -> Optional[dict]:
        key = self._build_key(request_dict)
        data = self._vals.get(key, False)
        if not data:
            return None
        if data["time"] + timedelta(minutes=60) > datetime.now():
            return data["value"]
        del self._vals[key]
        return None

    def save_to_cache(self, request_dict, response_dict: dict) -> dict:
        key = self._build_key(request_dict)
        data = {
            "time": datetime.now(),
            "value": response_dict,
        }
        self._vals[key] = data
        return data
