import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_cities_scores_with_default_end_date():
    """Test that endpoint works with only start_date"""
    start_date = date.today() - timedelta(days=7)
    response = client.get(f"/api/v1/cities-scores?start_date={start_date.isoformat()}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "cities" in data
    assert len(data["cities"]) == 6 
    assert data["start_date"] == start_date.isoformat()
    
    for city in data["cities"]:
        assert "city" in city
        assert "country" in city
        assert "temperature" in city
        assert "wind_speed" in city
        assert "relative_humidity" in city
        assert "cloud_cover" in city
        assert "score" in city
        
        assert 0 <= city["score"] <= 10
    
    scores = [city["score"] for city in data["cities"]]
    assert scores == sorted(scores, reverse=True)

def test_get_cities_scores_with_date_range():
    """Test endpoint with both start and end dates"""
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=3)
    
    response = client.get(
        f"/api/v1/cities-scores?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["start_date"] == start_date.isoformat()
    assert data["end_date"] == end_date.isoformat()
    assert len(data["cities"]) == 6

def test_invalid_date_range():
    """Test that start_date after end_date returns error"""
    start_date = date.today() - timedelta(days=1)
    end_date = date.today() - timedelta(days=7)
    
    response = client.get(
        f"/api/v1/cities-scores?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )
    
    assert response.status_code == 400
    assert "start_date must be before or equal to end_date" in response.json()["detail"]

def test_future_date_not_allowed():
    """Test that future dates are not allowed"""
    future_date = date.today() + timedelta(days=1)
    
    response = client.get(f"/api/v1/cities-scores?start_date={future_date.isoformat()}")
    
    assert response.status_code == 400

def test_missing_start_date():
    """Test that missing start_date returns error"""
    response = client.get("/api/v1/cities-scores")
    
    assert response.status_code == 422 

def test_root_returns_html():
    """Test that root endpoint returns HTML page"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.parametrize("city_name", [
    "Warsaw", "Gdansk", "Berlin", "Krakow", "Nurnberg", "Munich"
])
def test_specific_cities_present(city_name):
    """Test that all required cities are present in the response"""
    start_date = date.today() - timedelta(days=7)
    response = client.get(f"/api/v1/cities-scores?start_date={start_date.isoformat()}")
    
    assert response.status_code == 200
    data = response.json()
    
    city_names = [city["city"] for city in data["cities"]]
    assert city_name in city_names

def test_scores_are_reasonable():
    """Test that scores are within reasonable bounds for known data"""
    start_date = date.today() - timedelta(days=7)
    response = client.get(f"/api/v1/cities-scores?start_date={start_date.isoformat()}")
    
    assert response.status_code == 200
    data = response.json()
    
    for city in data["cities"]:
        assert city["score"] >= 0
        assert city["score"] <= 10
        assert -50 <= city["temperature"] <= 50
        assert 0 <= city["wind_speed"] <= 200
        assert 0 <= city["relative_humidity"] <= 100
        assert 0 <= city["cloud_cover"] <= 100