from pydantic import BaseModel
from typing import Optional
from datetime import date

class CityWeather(BaseModel):
    city: str
    country: str
    temperature: float
    wind_speed: float
    relative_humidity: float
    cloud_cover: float
    score: float
    
class CityScoresResponse(BaseModel):
    start_date: date
    end_date: date
    cities: list[CityWeather]