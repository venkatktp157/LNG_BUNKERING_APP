# LNG Bunkering Application REST API

This REST API provides programmatic access to the LNG Bunkering Application functionality, allowing you to perform LNG bunkering calculations through HTTP requests.

## Features

- **LNG Bunkering Operations**: Calculate corrected levels, volumes, and bunkering quantities
- **Ship Management**: Get information about available ships and their tank configurations
- **JSON Input/Output**: All requests and responses use JSON format
- **Interactive Documentation**: Built-in Swagger UI and ReDoc documentation

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements_api.txt
   ```

2. **Run the API server:**
   ```bash
   python api.py
   ```

3. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### 1. Ship Information

#### GET `/ships`
Get list of all available ships.

**Response:**
```json
{
  "ships": [
    "MOUNT TOURMALINE",
    "MOUNT NOVATERRA",
    "CMA CGM ARCTIC",
    ...
  ]
}
```

#### GET `/ships/{ship_id}`
Get details for a specific ship.

**Response:**
```json
{
  "ship_id": "MOUNT TOURMALINE",
  "tanks": ["LNG_TK1", "LNG_TK2"],
  "tank_count": 2
}
```

### 2. LNG Bunkering Calculations

#### POST `/bunkering/calculate`
Calculate LNG bunkering operations.

**Request Body:**
```json
{
  "ship_id": "MOUNT TOURMALINE",
  "opening_tank1": {
    "level": 1000.0,
    "vapor_temp": -150.0,
    "liquid_temp": -160.0,
    "pressure": 0.1
  },
  "opening_tank2": {
    "level": 1200.0,
    "vapor_temp": -148.0,
    "liquid_temp": -158.0,
    "pressure": 0.12
  },
  "closing_tank1": {
    "level": 1500.0,
    "vapor_temp": -149.0,
    "liquid_temp": -159.0,
    "pressure": 0.15
  },
  "closing_tank2": {
    "level": 1700.0,
    "vapor_temp": -147.0,
    "liquid_temp": -157.0,
    "pressure": 0.18
  },
  "opening_trim": 0.5,
  "opening_list": 1.2,
  "closing_trim": 0.3,
  "closing_list": 0.8,
  "opening_time": "12/01/2024 08:00",
  "closing_time": "12/01/2024 16:00",
  "density": 0.425,
  "bdn_quantity": 500.0,
  "bog": 200.0,
  "gross_energy": 2500.0,
  "unreckoned_qty": 10.0,
  "net_energy": 2400.0
}
```

**Response:**
```json
{
  "ship_id": "MOUNT TOURMALINE",
  "tank1_volume_opening": 1250.45,
  "tank2_volume_opening": 1380.67,
  "tank1_volume_closing": 1850.23,
  "tank2_volume_closing": 2100.89,
  "opening_quantity": 2631.12,
  "closing_quantity": 3951.12,
  "volume_difference": 1320.0,
  "bog_consumption": 94.12,
  "loaded_quantity": 1414.12,
  "net_quantity": 1380.0,
  "difference": 34.12,
  "calculation_time": "2024-12-01T10:30:00"
}
```

## Usage Examples

### Python Example

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

# Get list of ships
response = requests.get(f"{BASE_URL}/ships")
ships = response.json()["ships"]
print(f"Available ships: {ships}")

# Calculate bunkering
bunkering_data = {
    "ship_id": "MOUNT TOURMALINE",
    "opening_tank1": {
        "level": 1000.0,
        "vapor_temp": -150.0,
        "liquid_temp": -160.0,
        "pressure": 0.1
    },
    # ... other fields
}

response = requests.post(
    f"{BASE_URL}/bunkering/calculate",
    json=bunkering_data
)

if response.status_code == 200:
    result = response.json()
    print(f"Loaded quantity: {result['loaded_quantity']} m³")
```

### cURL Example

```bash
# Get ships list
curl -X GET "http://localhost:8000/ships"

# Calculate bunkering
curl -X POST "http://localhost:8000/bunkering/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "ship_id": "MOUNT TOURMALINE",
    "opening_tank1": {
      "level": 1000.0,
      "vapor_temp": -150.0,
      "liquid_temp": -160.0,
      "pressure": 0.1
    }
  }'
```

### JavaScript Example

```javascript
// Get ships list
fetch('http://localhost:8000/ships')
  .then(response => response.json())
  .then(data => console.log(data.ships));

// Calculate bunkering
const bunkeringData = {
  ship_id: "MOUNT TOURMALINE",
  opening_tank1: {
    level: 1000.0,
    vapor_temp: -150.0,
    liquid_temp: -160.0,
    pressure: 0.1
  }
  // ... other fields
};

fetch('http://localhost:8000/bunkering/calculate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(bunkeringData)
})
.then(response => response.json())
.then(result => console.log(result.loaded_quantity));
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK`: Successful operation
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a detail message:

```json
{
  "detail": "Invalid ship ID: UNKNOWN_SHIP"
}
```

## Data Validation

The API uses Pydantic models for automatic data validation:

- All numeric fields must be valid numbers
- Required fields cannot be null
- Date/time fields must follow the specified format
- Ship IDs must exist in the available ships list

## Testing

Run the test script to verify the API works correctly:

```bash
python test_bunkering_api.py
```

This will test all endpoints and show sample requests/responses.

## Development

### Project Structure

```
LNG_APP_api version incomplete/
├── api.py              # Main API server
├── requirements_api.txt # API dependencies
├── test_bunkering_api.py # Test script
├── README_API.md       # This file
├── app.py              # Original Streamlit app
└── DATA/               # Tank data files
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Create the endpoint function
3. Add validation and error handling
4. Update this documentation

### Running in Production

For production deployment:

1. Use a production ASGI server like Gunicorn
2. Set up proper CORS policies
3. Add authentication if needed
4. Use environment variables for configuration

```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Support

For issues or questions:

1. Check the API documentation at `/docs`
2. Review the test script in `test_bunkering_api.py`
3. Check the original Streamlit app for reference implementation

## License

This API is part of the LNG Bunkering Application project.
