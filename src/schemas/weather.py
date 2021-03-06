from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class Units(Enum):
    METRIC: str = "metric"
    STANDARD: str = "standard"
    IMPERIAL: str = "imperial"


class WeatherRequest(BaseModel):
    city: str
    state: Optional[str]
    country: Optional[str]
    units: Units = Units.METRIC

    # TODO Add Validators for data parsing per field


class WeatherResponse(BaseModel):
    status: str
    description: str
    temp: float
    country: str
    state: Optional[str]
    city: str


class WeatherReview(BaseModel):
    location: WeatherRequest
    username: Optional[str]
    description: str
    create_time: datetime
