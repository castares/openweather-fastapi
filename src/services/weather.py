import json

import httpx
from pydantic import BaseModel
from infrastructure.memory_cache import Cache, RequestMemoryCache
from schemas.weather import WeatherRequest, WeatherResponse
from utils.settings import Settings
from utils.error_handling import ServiceResponse


class WeatherService(BaseModel):
    _settings: Settings = Settings()
    _cache: Cache = RequestMemoryCache()
    _response_validator: ServiceResponse = ServiceResponse()

    class Config:
        arbitrary_types_allowed = True

    async def _parse_response(self, resp: httpx.Response) -> dict:
        response: dict = json.loads(resp.text)
        weather = response.get("weather", [])[0]
        main = response.get("main", {})
        sys = response.get("sys", {})
        parsed_response = WeatherResponse(
            status=weather.get("main", None),
            description=weather.get("description", None),
            temp=main.get("temp", 0.0),
            country=sys.get("country", None),
            city=response.get("name", None),
        )
        return parsed_response

    async def get_current_weather(
        self,
        weather_request: WeatherRequest,
    ) -> dict:
        request_dict: dict = weather_request.dict()
        cache = self._cache.get_cached_values(request_dict)
        if cache:
            return cache
        api_key = self._settings.OPENWEATHERMAP_API_KEY
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        params = {
            "q": f"{weather_request.city},{weather_request.state},{weather_request.country}",
            "appid": api_key,
            "units": weather_request.units.value,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=base_url, params=params)
            self._response_validator.handle_response(resp)
            parsed_response: WeatherResponse = await self._parse_response(resp)
            response_dict = parsed_response.dict()
        self._cache.save_to_cache(request_dict, response_dict)
        return response_dict
