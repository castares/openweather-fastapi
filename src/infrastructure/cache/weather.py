import datetime
from schemas.weather import WeatherRequest, WeatherResponse
from typing import Tuple
from pydantic import BaseModel


class WeatherCache(BaseModel):
    _instance = None
    _vals: dict = {}
    lifetime_in_hours = 1.0

    def __new__(cls):
        """
        Singleton implementation, to ensure only one Cache instance exists.
        """
        if cls._instance is None:
            cls._instance = super(WeatherCache, cls).__new__(cls)
        return cls._instance

    def _create_key(
        self,
        city: str,
        country: str,
    ) -> Tuple[str, str]:
        if not city or not country:
            raise Exception("City and country are required")
        return (
            city.strip().lower(),
            country.strip().lower(),
        )

    def _clean_out_of_date(self):
        for key, data in list(self._vals.items()):
            dt = datetime.datetime.now() - data.get("time")
            if dt / datetime.timedelta(minutes=60) > self.lifetime_in_hours:
                del self._vals[key]

    def get_cached_values(self, weather_request: WeatherRequest):
        key = self._create_key(
            weather_request.city,
            weather_request.country,
        )
        data = self._vals.get(key)
        if not data:
            return None
        last = data["time"]
        dt = datetime.datetime.now() - last
        if dt / datetime.timedelta(minutes=60) < self.lifetime_in_hours:
            return data["value"]

        del self._vals[key]
        return None

    def save_to_cache(self, weather_response=WeatherResponse):
        key = self._create_key(
            weather_response.city,
            weather_response.country,
        )
        data = {
            "time": datetime.datetime.now(),
            "value": weather_response.dict(),
        }
        self._vals[key] = data
        self._clean_out_of_date()
