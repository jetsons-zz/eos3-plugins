"""
Weather Farming Advisor - Agricultural Intelligence Skill

This package provides agricultural weather analysis and crop recommendations
using the Open-Meteo API.
"""

from .weather_client import (
    WeatherClient,
    get_weather_forecast,
    get_soil_conditions
)

from .crop_advisor import (
    CROP_DATABASE,
    get_crop_info,
    find_similar_crops,
    list_available_crops,
    calculate_crop_suitability,
    get_irrigation_advice
)

from .alert_system import (
    check_weather_alerts,
    format_alerts_summary
)

from .report_generator import (
    comprehensive_agricultural_report,
    format_report_text,
    get_farming_recommendations
)

__version__ = "1.0.0"
__author__ = "Agent-Skill-Creator"

__all__ = [
    # Weather
    "WeatherClient",
    "get_weather_forecast",
    "get_soil_conditions",

    # Crop
    "CROP_DATABASE",
    "get_crop_info",
    "find_similar_crops",
    "list_available_crops",
    "calculate_crop_suitability",
    "get_irrigation_advice",

    # Alerts
    "check_weather_alerts",
    "format_alerts_summary",

    # Reports
    "comprehensive_agricultural_report",
    "format_report_text",
    "get_farming_recommendations"
]
