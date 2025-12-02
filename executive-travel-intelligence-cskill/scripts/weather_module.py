"""
Weather Module - 天气预报模块
使用 Open-Meteo API 获取天气数据
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

API_BASE = "https://api.open-meteo.com/v1/forecast"

# 主要城市坐标
CITY_COORDINATES = {
    # 亚洲
    "东京": (35.6762, 139.6503, "Asia/Tokyo", "JPY"),
    "tokyo": (35.6762, 139.6503, "Asia/Tokyo", "JPY"),
    "北京": (39.9042, 116.4074, "Asia/Shanghai", "CNY"),
    "beijing": (39.9042, 116.4074, "Asia/Shanghai", "CNY"),
    "上海": (31.2304, 121.4737, "Asia/Shanghai", "CNY"),
    "shanghai": (31.2304, 121.4737, "Asia/Shanghai", "CNY"),
    "香港": (22.3193, 114.1694, "Asia/Hong_Kong", "HKD"),
    "hongkong": (22.3193, 114.1694, "Asia/Hong_Kong", "HKD"),
    "新加坡": (1.3521, 103.8198, "Asia/Singapore", "SGD"),
    "singapore": (1.3521, 103.8198, "Asia/Singapore", "SGD"),
    "首尔": (37.5665, 126.9780, "Asia/Seoul", "KRW"),
    "seoul": (37.5665, 126.9780, "Asia/Seoul", "KRW"),
    "迪拜": (25.2048, 55.2708, "Asia/Dubai", "AED"),
    "dubai": (25.2048, 55.2708, "Asia/Dubai", "AED"),
    # 欧洲
    "伦敦": (51.5074, -0.1278, "Europe/London", "GBP"),
    "london": (51.5074, -0.1278, "Europe/London", "GBP"),
    "巴黎": (48.8566, 2.3522, "Europe/Paris", "EUR"),
    "paris": (48.8566, 2.3522, "Europe/Paris", "EUR"),
    "法兰克福": (50.1109, 8.6821, "Europe/Berlin", "EUR"),
    "frankfurt": (50.1109, 8.6821, "Europe/Berlin", "EUR"),
    "苏黎世": (47.3769, 8.5417, "Europe/Zurich", "CHF"),
    "zurich": (47.3769, 8.5417, "Europe/Zurich", "CHF"),
    # 美洲
    "纽约": (40.7128, -74.0060, "America/New_York", "USD"),
    "newyork": (40.7128, -74.0060, "America/New_York", "USD"),
    "new york": (40.7128, -74.0060, "America/New_York", "USD"),
    "洛杉矶": (34.0522, -118.2437, "America/Los_Angeles", "USD"),
    "losangeles": (34.0522, -118.2437, "America/Los_Angeles", "USD"),
    "los angeles": (34.0522, -118.2437, "America/Los_Angeles", "USD"),
    "旧金山": (37.7749, -122.4194, "America/Los_Angeles", "USD"),
    "san francisco": (37.7749, -122.4194, "America/Los_Angeles", "USD"),
    "多伦多": (43.6532, -79.3832, "America/Toronto", "CAD"),
    "toronto": (43.6532, -79.3832, "America/Toronto", "CAD"),
    # 大洋洲
    "悉尼": (-33.8688, 151.2093, "Australia/Sydney", "AUD"),
    "sydney": (-33.8688, 151.2093, "Australia/Sydney", "AUD"),
}


def get_city_info(city: str) -> Optional[tuple]:
    """获取城市信息"""
    city_lower = city.lower().replace(" ", "")
    for name, info in CITY_COORDINATES.items():
        if name.lower().replace(" ", "") == city_lower:
            return info
    return None


def get_weather_forecast(city: str, days: int = 7) -> Dict:
    """
    获取城市天气预报

    Args:
        city: 城市名称
        days: 预报天数 (1-7)

    Returns:
        天气预报数据
    """
    city_info = get_city_info(city)
    if not city_info:
        return {"error": f"未找到城市: {city}"}

    lat, lon, timezone, currency = city_info

    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "weather_code"
            ],
            "timezone": timezone,
            "forecast_days": min(days, 7)
        }

        response = requests.get(API_BASE, params=params, timeout=10)
        data = response.json()

        if "daily" not in data:
            return {"error": "无法获取天气数据"}

        daily = data["daily"]
        forecasts = []

        weather_codes = {
            0: "晴天", 1: "晴朗", 2: "多云", 3: "阴天",
            45: "有雾", 48: "雾凇", 51: "小雨", 53: "中雨",
            55: "大雨", 61: "小雨", 63: "中雨", 65: "大雨",
            71: "小雪", 73: "中雪", 75: "大雪", 95: "雷雨"
        }

        for i in range(len(daily["time"])):
            code = daily["weather_code"][i]
            forecasts.append({
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "rain_probability": daily["precipitation_probability_max"][i],
                "wind_speed": daily["wind_speed_10m_max"][i],
                "weather": weather_codes.get(code, "未知"),
                "weather_code": code
            })

        # 计算平均温度范围
        avg_max = sum(f["temp_max"] for f in forecasts) / len(forecasts)
        avg_min = sum(f["temp_min"] for f in forecasts) / len(forecasts)
        max_rain_prob = max(f["rain_probability"] for f in forecasts)

        return {
            "city": city,
            "timezone": timezone,
            "currency": currency,
            "coordinates": {"lat": lat, "lon": lon},
            "forecasts": forecasts,
            "summary": {
                "avg_high": round(avg_max, 1),
                "avg_low": round(avg_min, 1),
                "temp_range": f"{round(avg_min)}-{round(avg_max)}°C",
                "max_rain_probability": max_rain_prob,
                "needs_umbrella": max_rain_prob > 40
            }
        }

    except Exception as e:
        return {"error": str(e)}


def get_clothing_advice(temp_max: float, temp_min: float, rain_prob: float) -> Dict:
    """
    根据天气获取穿衣建议

    Args:
        temp_max: 最高温度
        temp_min: 最低温度
        rain_prob: 降雨概率

    Returns:
        穿衣建议
    """
    avg_temp = (temp_max + temp_min) / 2

    if avg_temp < 5:
        clothing = "厚羽绒服/大衣"
        category = "严寒"
        items = ["羽绒服", "围巾", "手套", "帽子", "保暖内衣"]
    elif avg_temp < 10:
        clothing = "厚外套/毛衣"
        category = "寒冷"
        items = ["厚外套", "毛衣", "围巾"]
    elif avg_temp < 15:
        clothing = "薄外套/夹克"
        category = "凉爽"
        items = ["薄外套", "长袖衬衫", "薄毛衣"]
    elif avg_temp < 22:
        clothing = "长袖衬衫/薄外套"
        category = "舒适"
        items = ["长袖衬衫", "薄外套备用"]
    elif avg_temp < 28:
        clothing = "短袖/轻薄衣物"
        category = "温暖"
        items = ["短袖", "薄长裤", "防晒衣"]
    else:
        clothing = "轻薄透气衣物"
        category = "炎热"
        items = ["短袖", "短裤", "防晒用品", "遮阳帽"]

    if rain_prob > 40:
        items.append("雨伞")
    if rain_prob > 60:
        items.append("防水外套")

    return {
        "recommendation": clothing,
        "category": category,
        "temperature_feel": f"{category} ({round(avg_temp)}°C)",
        "essential_items": items,
        "rain_gear_needed": rain_prob > 40
    }


def get_supported_cities() -> List[str]:
    """获取支持的城市列表"""
    seen = set()
    cities = []
    for name in CITY_COORDINATES.keys():
        if name not in seen and not name.islower():
            cities.append(name)
            seen.add(name)
    return sorted(cities)
