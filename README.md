# UV Index Notifier

A production-ready Flask API service that provides UV index forecasts and low UV time recommendations for any location.


## API Endpoints

### Health Check
```http
GET /health
```
Returns service status and version information.

### Get UV Data
```http
POST /get_uv_data
Content-Type: application/json

{
  "data": {
    "lat": 40.7128,
    "lon": -74.0060,
    "timezone": "America/New_York"
  }
}
```

**Response:**
```json
{
  "uv_index_forecast": ["9 AM - 11 AM", "4 PM - 6 PM"],
  "current_time": "2:30 PM",
  "current_date": "2025-01-15",
  "current_uv_index": 3
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
