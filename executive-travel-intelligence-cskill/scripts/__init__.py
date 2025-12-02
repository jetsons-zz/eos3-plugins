"""
Executive Travel Intelligence - 高管出行智囊
6维度融合：天气+空气+汇率+时区+节假日+智能建议
"""

from .weather_module import get_weather_forecast, get_clothing_advice
from .air_quality_module import get_air_quality, get_health_advice
from .forex_module import get_exchange_rate, get_budget_estimate
from .timezone_module import get_timezone_info, get_best_meeting_times
from .holiday_module import get_holidays, check_business_days
from .travel_advisor import (
    generate_travel_report,
    calculate_travel_score,
    get_packing_checklist
)

__all__ = [
    'get_weather_forecast',
    'get_clothing_advice',
    'get_air_quality',
    'get_health_advice',
    'get_exchange_rate',
    'get_budget_estimate',
    'get_timezone_info',
    'get_best_meeting_times',
    'get_holidays',
    'check_business_days',
    'generate_travel_report',
    'calculate_travel_score',
    'get_packing_checklist'
]

__version__ = '1.0.0'
