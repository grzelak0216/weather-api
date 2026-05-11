from typing import Dict

class ScoringService:
    @staticmethod
    def calculate_temperature_score(temp: float) -> float:
        """Score temperature - 24°C is optimal (10 points)"""
        optimal_temp = 24
        max_deviation = 30  # Maximum reasonable deviation
        deviation = abs(temp - optimal_temp)
        score = max(0, 10 - (deviation / max_deviation * 10))
        return round(score, 2)
    
    @staticmethod
    def calculate_wind_speed_score(wind_speed: float) -> float:
        """Score wind speed - lower is better, 0 is optimal (10 points)"""
        max_wind = 50  # km/h - maximum wind speed for scoring
        score = max(0, 10 - (wind_speed / max_wind * 10))
        return round(score, 2)
    
    @staticmethod
    def calculate_humidity_score(humidity: float) -> float:
        """Score humidity - 50% is optimal (10 points), 0% or 100% = 0 points"""
        optimal_humidity = 50
        # Parabolic function peaking at 50%
        score = max(0, 10 * (1 - ((humidity - optimal_humidity) / optimal_humidity) ** 2))
        return round(score, 2)
    
    @staticmethod
    def calculate_cloud_cover_score(cloud_cover: float) -> float:
        """Score cloud cover - 25% is optimal (10 points), 0% or 100% = 0 points"""
        optimal_cloud = 25
        # Parabolic function peaking at 25%
        if cloud_cover <= optimal_cloud:
            score = 10 * (1 - ((optimal_cloud - cloud_cover) / optimal_cloud) ** 2)
        else:
            score = 10 * (1 - ((cloud_cover - optimal_cloud) / (100 - optimal_cloud)) ** 2)
        return round(max(0, score), 2)
    
    @classmethod
    def calculate_total_score(cls, weather_data: Dict) -> float:
        """Calculate weighted total score"""
        temp_score = cls.calculate_temperature_score(weather_data["temperature"])
        wind_score = cls.calculate_wind_speed_score(weather_data["wind_speed"])
        humidity_score = cls.calculate_humidity_score(weather_data["relative_humidity"])
        cloud_score = cls.calculate_cloud_cover_score(weather_data["cloud_cover"])
        
        # Weights: 35% temperature, 20% wind speed, 20% humidity, 25% cloud cover
        total_score = (
            temp_score * 0.35 +
            wind_score * 0.20 +
            humidity_score * 0.20 +
            cloud_score * 0.25
        )
        
        return round(total_score, 2)