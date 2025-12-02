"""
Weather Client for Open-Meteo API
Fetches weather forecasts and soil conditions for agricultural analysis.
"""

import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from functools import lru_cache
import time


# API Configuration
BASE_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_TTL = 3600  # 1 hour cache


class WeatherClient:
    """Client for Open-Meteo weather API with agricultural focus."""

    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between requests

    def _rate_limit(self) -> None:
        """Enforce rate limiting between API calls."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _validate_coordinates(self, latitude: float, longitude: float) -> None:
        """Validate geographic coordinates."""
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude {latitude}. Must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude {longitude}. Must be between -180 and 180.")

    def get_weather_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict:
        """
        Fetch weather forecast for specified location.

        Args:
            latitude: Location latitude (-90 to 90)
            longitude: Location longitude (-180 to 180)
            days: Forecast days (1-16, default 7)

        Returns:
            Dict with daily forecasts including temperature, precipitation,
            wind, humidity, and evapotranspiration data.

        Raises:
            ValueError: If coordinates are invalid
            requests.RequestException: If API call fails
        """
        self._validate_coordinates(latitude, longitude)
        days = max(1, min(16, days))  # Clamp to valid range

        self._rate_limit()

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_direction_10m_dominant",
                "relative_humidity_2m_mean",
                "et0_fao_evapotranspiration",
                "uv_index_max",
                "sunrise",
                "sunset"
            ],
            "timezone": "auto",
            "forecast_days": days
        }

        try:
            response = self.session.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout:
            raise ConnectionError("Weather API timeout. Please try again.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"Weather API error: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error: {e}")

        return self._parse_forecast_response(data)

    def _parse_forecast_response(self, data: Dict) -> Dict:
        """Parse API response into structured forecast data."""
        daily = data.get("daily", {})
        dates = daily.get("time", [])

        forecasts = []
        for i, date in enumerate(dates):
            forecast = {
                "date": date,
                "temp_max": daily.get("temperature_2m_max", [None])[i],
                "temp_min": daily.get("temperature_2m_min", [None])[i],
                "precipitation": daily.get("precipitation_sum", [0])[i] or 0,
                "precip_probability": daily.get("precipitation_probability_max", [0])[i] or 0,
                "wind_speed": daily.get("wind_speed_10m_max", [0])[i] or 0,
                "wind_direction": daily.get("wind_direction_10m_dominant", [0])[i] or 0,
                "humidity": daily.get("relative_humidity_2m_mean", [0])[i] or 0,
                "evapotranspiration": daily.get("et0_fao_evapotranspiration", [0])[i] or 0,
                "uv_index": daily.get("uv_index_max", [0])[i] or 0,
                "sunrise": daily.get("sunrise", [None])[i],
                "sunset": daily.get("sunset", [None])[i]
            }
            forecasts.append(forecast)

        # Calculate summary statistics
        temps = [f["temp_max"] for f in forecasts if f["temp_max"] is not None]
        temp_mins = [f["temp_min"] for f in forecasts if f["temp_min"] is not None]
        precip_total = sum(f["precipitation"] for f in forecasts)

        return {
            "location": {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone"),
                "elevation": data.get("elevation")
            },
            "daily": forecasts,
            "summary": {
                "temp_max_range": (min(temps) if temps else None, max(temps) if temps else None),
                "temp_min_range": (min(temp_mins) if temp_mins else None, max(temp_mins) if temp_mins else None),
                "total_precipitation": round(precip_total, 1),
                "rainy_days": sum(1 for f in forecasts if f["precipitation"] > 1),
                "frost_days": sum(1 for f in forecasts if f["temp_min"] is not None and f["temp_min"] < 0)
            },
            "generated_at": datetime.now().isoformat()
        }

    def get_soil_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Fetch current soil temperature and moisture at multiple depths.

        Args:
            latitude: Location latitude
            longitude: Location longitude

        Returns:
            Dict with soil temperature and moisture at various depths,
            plus workability assessment.
        """
        self._validate_coordinates(latitude, longitude)
        self._rate_limit()

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "soil_temperature_0cm",
                "soil_temperature_6cm",
                "soil_temperature_18cm",
                "soil_temperature_54cm",
                "soil_moisture_0_to_1cm",
                "soil_moisture_1_to_3cm",
                "soil_moisture_3_to_9cm",
                "soil_moisture_9_to_27cm",
                "soil_moisture_27_to_81cm"
            ],
            "timezone": "auto",
            "forecast_days": 1
        }

        try:
            response = self.session.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Soil data fetch failed: {e}")

        return self._parse_soil_response(data)

    def _parse_soil_response(self, data: Dict) -> Dict:
        """Parse soil data response."""
        hourly = data.get("hourly", {})

        # Get current hour index (use most recent data)
        current_hour = datetime.now().hour
        idx = min(current_hour, len(hourly.get("time", [])) - 1)
        idx = max(0, idx)

        def safe_get(key: str, default: float = 0.0) -> float:
            values = hourly.get(key, [])
            if idx < len(values) and values[idx] is not None:
                return values[idx]
            return default

        soil_temp_surface = safe_get("soil_temperature_0cm")
        soil_temp_6cm = safe_get("soil_temperature_6cm")
        soil_temp_18cm = safe_get("soil_temperature_18cm")
        soil_temp_54cm = safe_get("soil_temperature_54cm")

        moisture_surface = safe_get("soil_moisture_0_to_1cm")
        moisture_shallow = safe_get("soil_moisture_1_to_3cm")
        moisture_mid = safe_get("soil_moisture_3_to_9cm")
        moisture_root = safe_get("soil_moisture_9_to_27cm")
        moisture_deep = safe_get("soil_moisture_27_to_81cm")

        # Calculate root zone average (3-27cm)
        root_zone_moisture = (moisture_mid + moisture_root) / 2

        # Calculate workability score (0-100)
        workability = self._calculate_workability(
            soil_temp_6cm, moisture_surface, moisture_shallow
        )

        return {
            "temperature": {
                "surface": round(soil_temp_surface, 1),
                "depth_6cm": round(soil_temp_6cm, 1),
                "depth_18cm": round(soil_temp_18cm, 1),
                "depth_54cm": round(soil_temp_54cm, 1)
            },
            "moisture": {
                "surface": round(moisture_surface, 3),
                "shallow_1_3cm": round(moisture_shallow, 3),
                "mid_3_9cm": round(moisture_mid, 3),
                "root_zone_9_27cm": round(moisture_root, 3),
                "deep_27_81cm": round(moisture_deep, 3),
                "root_zone_average": round(root_zone_moisture, 3)
            },
            "workability_score": workability,
            "frost_risk": soil_temp_surface <= 0,
            "assessment": self._assess_soil_conditions(
                soil_temp_6cm, root_zone_moisture, workability
            ),
            "measured_at": datetime.now().isoformat()
        }

    def _calculate_workability(
        self,
        temp: float,
        moisture_surface: float,
        moisture_shallow: float
    ) -> int:
        """
        Calculate soil workability score (0-100).

        Factors:
        - Soil temperature (frozen = unworkable)
        - Moisture level (too wet = unworkable, too dry = difficult)
        """
        score = 100

        # Temperature penalty
        if temp < 0:
            score -= 80  # Frozen soil
        elif temp < 5:
            score -= 30  # Very cold
        elif temp < 10:
            score -= 10  # Cool

        # Moisture penalty
        avg_moisture = (moisture_surface + moisture_shallow) / 2

        if avg_moisture > 0.45:
            score -= 50  # Too wet, muddy
        elif avg_moisture > 0.40:
            score -= 25  # Wet
        elif avg_moisture < 0.10:
            score -= 20  # Too dry, dusty
        elif avg_moisture < 0.15:
            score -= 10  # Dry

        return max(0, min(100, score))

    def _assess_soil_conditions(
        self,
        temp: float,
        moisture: float,
        workability: int
    ) -> str:
        """Generate human-readable soil assessment."""
        conditions = []

        # Temperature assessment
        if temp < 0:
            conditions.append("frozen")
        elif temp < 5:
            conditions.append("very cold")
        elif temp < 10:
            conditions.append("cool")
        elif temp < 20:
            conditions.append("moderate")
        else:
            conditions.append("warm")

        # Moisture assessment
        if moisture > 0.45:
            conditions.append("waterlogged")
        elif moisture > 0.35:
            conditions.append("moist")
        elif moisture > 0.20:
            conditions.append("adequate moisture")
        elif moisture > 0.10:
            conditions.append("dry")
        else:
            conditions.append("very dry")

        # Workability
        if workability >= 80:
            work_status = "excellent for field work"
        elif workability >= 60:
            work_status = "suitable for light work"
        elif workability >= 40:
            work_status = "marginal workability"
        else:
            work_status = "not suitable for field work"

        return f"Soil is {conditions[0]} and {conditions[1]}. {work_status.capitalize()}."


def get_weather_forecast(
    latitude: float,
    longitude: float,
    days: int = 7
) -> Dict:
    """
    Convenience function to get weather forecast.

    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        days: Forecast days (1-16, default 7)

    Returns:
        Dict with daily forecasts and summary statistics.

    Example:
        >>> forecast = get_weather_forecast(40.7128, -74.0060)
        >>> print(forecast['summary']['total_precipitation'])
    """
    client = WeatherClient()
    return client.get_weather_forecast(latitude, longitude, days)


def get_soil_conditions(latitude: float, longitude: float) -> Dict:
    """
    Convenience function to get soil conditions.

    Args:
        latitude: Location latitude
        longitude: Location longitude

    Returns:
        Dict with soil temperature, moisture, and workability data.

    Example:
        >>> soil = get_soil_conditions(40.7128, -74.0060)
        >>> print(f"Soil temp at 6cm: {soil['temperature']['depth_6cm']}°C")
    """
    client = WeatherClient()
    return client.get_soil_conditions(latitude, longitude)


if __name__ == "__main__":
    # Test the client
    print("Testing Weather Client...")

    # Test coordinates: Des Moines, Iowa
    lat, lon = 41.5868, -93.6250

    print(f"\nFetching forecast for {lat}, {lon}...")
    forecast = get_weather_forecast(lat, lon)
    print(f"Location: {forecast['location']}")
    print(f"Summary: {forecast['summary']}")
    print(f"First day: {forecast['daily'][0]}")

    print(f"\nFetching soil conditions...")
    soil = get_soil_conditions(lat, lon)
    print(f"Temperature: {soil['temperature']}")
    print(f"Moisture: {soil['moisture']}")
    print(f"Workability: {soil['workability_score']}/100")
    print(f"Assessment: {soil['assessment']}")
