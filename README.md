# Weather Scoring API

FastAPI application that fetches weather data from Open-Meteo API and scores European cities based on weather parameters. Built as a recruitment task.

## Requirements

- Python 3.11+
- pip

## Quick Start

```bash
# Clone repository
git clone <repository-url>
cd weather-api

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload
```

Visit **http://localhost:8000** for the web dashboard or **http://localhost:8000/docs** for API docs.

## Docker

```bash
docker build -t weather-api .
docker run -p 8000:8000 weather-api
```

## Scoring Algorithm

| Parameter   | Weight | Optimal | Rule                     |
| ----------- | ------ | ------- | ------------------------ |
| Temperature | 35%    | 24°C    | Decreases with deviation |
| Wind Speed  | 20%    | 0 km/h  | Lower is better          |
| Humidity    | 20%    | 50%     | 0 at extremes            |
| Cloud Cover | 25%    | 25%     | 0 at extremes            |

## Cities

Warsaw, Gdansk, Krakow (Poland) + Berlin, Nurnberg, Munich (Germany)

## API

### GET /api/v1/cities-scores

```bash
curl "http://localhost:8000/api/v1/cities-scores?start_date=2024-01-01"
```

Parameters:

- `start_date` (required) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date, defaults to yesterday

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
app/
├── api/v1/endpoints.py    # API routes
├── core/config.py         # Settings
├── models/schemas.py      # Data models
├── services/
│   ├── weather_service.py # Open-Meteo integration
│   └── scoring_service.py # Scoring logic
├── static/                # Web dashboard
└── main.py               # App entry point
tests/
└── test_api.py           # Unit tests
```

## Potential Improvements

- Redis caching for better performance
- API authentication (JWT/API key)
- Database for historical data storage
- More cities and weather parameters
- Weather forecast scoring
- User-defined scoring weights
- Mobile app
- Real-time WebSocket updates
- Monitoring (Prometheus/Grafana)
- Kubernetes deployment
- CI/CD pipeline (GitHub Actions)
- Rate limiting
- Response compression
- Dark mode for dashboard
- PWA support
- Integration tests
- E2E tests with Playwright
