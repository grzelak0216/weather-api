from fastapi import APIRouter, Query, HTTPException
from datetime import date, timedelta
from typing import Optional
from app.services.weather_service import WeatherService
from app.services.scoring_service import ScoringService
from app.models.schemas import CityWeather, CityScoresResponse

router = APIRouter()
weather_service = WeatherService()
scoring_service = ScoringService()

@router.get("/cities-scores", response_model=CityScoresResponse)
async def get_cities_scores(
    start_date: date = Query(..., description="Start date for weather data"),
    end_date: Optional[date] = Query(None, description="End date for weather data (defaults to yesterday)")
):
    if end_date is None:
        end_date = date.today() - timedelta(days=1)
    
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before or equal to end_date")
    
    if end_date >= date.today():
        raise HTTPException(status_code=400, detail="end_date must be in the past")
    
    all_weather = await weather_service.get_all_cities_weather(start_date, end_date)
    
    cities_scores = []
    for city, weather_data in all_weather.items():
        total_score = scoring_service.calculate_total_score(weather_data)
        city_info = weather_service.cities[city]
        
        city_weather = CityWeather(
            city=city,
            country=city_info["country"],
            temperature=round(weather_data["temperature"], 1),
            wind_speed=round(weather_data["wind_speed"], 1),
            relative_humidity=round(weather_data["relative_humidity"], 1),
            cloud_cover=round(weather_data["cloud_cover"], 1),
            score=total_score
        )
        cities_scores.append(city_weather)
    
    cities_scores.sort(key=lambda x: x.score, reverse=True)
    
    return CityScoresResponse(
        start_date=start_date,
        end_date=end_date,
        cities=cities_scores
    )