"""
Air Quality Advisor - 空气质量顾问
为高净值人群和企业高管提供全球空气质量监测与健康建议
"""

from .aqi_client import AQIClient, get_city_aqi, get_aqi_by_location
from .health_advisor import (
    get_health_recommendations,
    get_activity_advice,
    get_sensitive_group_warnings
)
from .report_generator import (
    generate_aqi_report,
    generate_travel_advisory,
    compare_cities
)

__all__ = [
    'AQIClient',
    'get_city_aqi',
    'get_aqi_by_location',
    'get_health_recommendations',
    'get_activity_advice',
    'get_sensitive_group_warnings',
    'generate_aqi_report',
    'generate_travel_advisory',
    'compare_cities'
]

__version__ = '1.0.0'
