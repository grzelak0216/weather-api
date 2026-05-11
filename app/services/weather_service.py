import httpx
from datetime import date, timedelta
from typing import List, Dict
import statistics

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.cities = {
            "Warsaw": {"country": "Poland", "lat": 52.2297, "lon": 21.0122},
            "Gdansk": {"country": "Poland", "lat": 54.3520, "lon": 18.6466},
            "Berlin": {"country": "Germany", "lat": 52.5200, "lon": 13.4050},
            "Krakow": {"country": "Poland", "lat": 50.0647, "lon": 19.9450},
            "Nurnberg": {"country": "Germany", "lat": 49.4521, "lon": 11.0767},
            "Munich": {"country": "Germany", "lat": 48.1351, "lon": 11.5820}
        }
    
    async def get_city_weather(self, city: str, start_date: date, end_date: date) -> Dict:
        city_data = self.cities[city]
        
        params = {
            "latitude": city_data["lat"],
            "longitude": city_data["lon"],
            "hourly": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m", "cloud_cover"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "timezone": "auto"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            hourly = data["hourly"]

            temps = hourly["temperature_2m"]
            wind_speeds = hourly["wind_speed_10m"]
            humidity = hourly["relative_humidity_2m"]
            cloud_cover = hourly["cloud_cover"]
            
            return {
                "temperature": statistics.mean(temps),
                "wind_speed": statistics.mean(wind_speeds),
                "relative_humidity": statistics.mean(humidity),
                "cloud_cover": statistics.mean(cloud_cover)
            }
    
    async def get_all_cities_weather(self, start_date: date, end_date: date) -> Dict[str, Dict]:
        results = {}
        for city in self.cities:
            weather_data = await self.get_city_weather(city, start_date, end_date)
            results[city] = weather_data
        return results