from fastapi import APIRouter, Response
from fastapi.params import Depends

from schemas.weather import WeatherRequest, WeatherResponse
from services.weather import WeatherService

router: APIRouter = APIRouter(prefix="/weather")


@router.get("/current/{city}/", response_model=WeatherResponse)
async def get_weather(
    weather_request: WeatherRequest = Depends(),
    weather_service: WeatherService = Depends(),
):
    response: dict = await weather_service.get_current_weather(weather_request)
    return response
