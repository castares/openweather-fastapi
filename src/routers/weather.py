from fastapi import APIRouter, Response
from fastapi.params import Depends

from schemas.weather import WeatherRequest, WeatherResponse, WeatherReview
from services.weather import WeatherService

router: APIRouter = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)

# TODO: move dependencies to router, to avoid duplicities.


@router.get("/current/{city}/", response_model=WeatherResponse)
async def get_weather(
    weather_request: WeatherRequest = Depends(),
    weather_service: WeatherService = Depends(),
):
    response: dict = await weather_service.get_current_weather(weather_request)
    return response


@router.get("/reviews", response_model=list[WeatherReview])
async def get_reviews(
    weather_request: WeatherReview = Depends(),
    weather_service: WeatherService = Depends(),
):
    pass


@router.post("/review/create", status_code=201, response_model=WeatherReview)
async def post_review():
    pass
