# Open-Meteo API Reference

## Base URL

```
https://api.open-meteo.com/v1/forecast
```

## Weather Forecast Endpoint

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| latitude | float | Yes | Location latitude (-90 to 90) |
| longitude | float | Yes | Location longitude (-180 to 180) |
| daily | array | No | Daily variables to fetch |
| hourly | array | No | Hourly variables to fetch |
| timezone | string | No | Timezone (default: GMT, use "auto") |
| forecast_days | int | No | Days ahead (1-16, default 7) |
| past_days | int | No | Past days to include (0-92) |

### Daily Variables Used

```
temperature_2m_max      - Maximum temperature at 2m (°C)
temperature_2m_min      - Minimum temperature at 2m (°C)
precipitation_sum       - Total precipitation (mm)
precipitation_probability_max - Max precipitation probability (%)
wind_speed_10m_max      - Maximum wind speed at 10m (km/h)
wind_direction_10m_dominant - Dominant wind direction (°)
relative_humidity_2m_mean - Mean relative humidity (%)
et0_fao_evapotranspiration - Reference evapotranspiration (mm)
uv_index_max            - Maximum UV index
sunrise                 - Sunrise time (ISO8601)
sunset                  - Sunset time (ISO8601)
```

### Hourly Soil Variables

```
soil_temperature_0cm    - Surface soil temperature (°C)
soil_temperature_6cm    - Soil temperature at 6cm (°C)
soil_temperature_18cm   - Soil temperature at 18cm (°C)
soil_temperature_54cm   - Soil temperature at 54cm (°C)
soil_moisture_0_to_1cm  - Surface moisture (m³/m³)
soil_moisture_1_to_3cm  - Shallow moisture (m³/m³)
soil_moisture_3_to_9cm  - Mid-depth moisture (m³/m³)
soil_moisture_9_to_27cm - Root zone moisture (m³/m³)
soil_moisture_27_to_81cm - Deep moisture (m³/m³)
```

## Example Request

```python
import requests

params = {
    "latitude": 41.5868,
    "longitude": -93.6250,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max"
    ],
    "hourly": [
        "soil_temperature_6cm",
        "soil_moisture_9_to_27cm"
    ],
    "timezone": "auto",
    "forecast_days": 7
}

response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params=params
)

data = response.json()
```

## Example Response

```json
{
    "latitude": 41.58,
    "longitude": -93.62,
    "timezone": "America/Chicago",
    "elevation": 262.0,
    "daily": {
        "time": ["2025-01-15", "2025-01-16", ...],
        "temperature_2m_max": [5.2, 8.1, ...],
        "temperature_2m_min": [-2.3, 1.5, ...],
        "precipitation_sum": [0.0, 12.5, ...],
        "precipitation_probability_max": [10, 85, ...]
    },
    "hourly": {
        "time": ["2025-01-15T00:00", ...],
        "soil_temperature_6cm": [2.1, 1.8, ...],
        "soil_moisture_9_to_27cm": [0.32, 0.33, ...]
    }
}
```

## Rate Limits

- **Non-commercial**: No hard limit, recommended max 10 req/min
- **Commercial**: API key required, higher limits

## Data Sources

Open-Meteo combines data from:
- ECMWF (European Centre for Medium-Range Weather Forecasts)
- NOAA (US National Oceanic and Atmospheric Administration)
- DWD (German Weather Service)
- Météo-France
- Canadian Meteorological Centre

## Soil Data Notes

- Soil temperature available at 4 depths (0, 6, 18, 54 cm)
- Soil moisture in volumetric water content (m³/m³)
- ERA5-Land reanalysis for historical data
- Updated hourly

## Links

- [API Documentation](https://open-meteo.com/en/docs)
- [Soil Variables](https://open-meteo.com/en/docs#hourly=soil_temperature_0cm)
- [Weather Variables](https://open-meteo.com/en/docs#daily=temperature_2m_max)
