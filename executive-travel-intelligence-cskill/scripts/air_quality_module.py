"""
Air Quality Module - 空气质量模块
使用 AQICN API 获取空气质量数据
"""

import requests
from datetime import datetime
from typing import Dict, Optional

API_BASE = "https://api.waqi.info"
DEFAULT_TOKEN = "demo"  # Demo token，仅支持上海测试

# AQI 等级
AQI_LEVELS = {
    (0, 50): ("优", "🟢", "空气质量优秀"),
    (51, 100): ("良", "🟡", "空气质量良好"),
    (101, 150): ("轻度污染", "🟠", "敏感人群注意"),
    (151, 200): ("中度污染", "🔴", "减少户外活动"),
    (201, 300): ("重度污染", "🟣", "避免户外活动"),
    (301, 500): ("严重污染", "🟤", "留在室内")
}


def get_aqi_level(aqi: int) -> tuple:
    """获取 AQI 等级信息"""
    for (low, high), info in AQI_LEVELS.items():
        if low <= aqi <= high:
            return info
    return ("严重污染", "🟤", "留在室内")


def get_air_quality(city: str, token: str = None) -> Dict:
    """
    获取城市空气质量

    Args:
        city: 城市名称
        token: AQICN API token

    Returns:
        空气质量数据
    """
    token = token or DEFAULT_TOKEN

    # 城市名映射
    city_map = {
        "东京": "tokyo", "北京": "beijing", "上海": "shanghai",
        "香港": "hongkong", "新加坡": "singapore", "首尔": "seoul",
        "伦敦": "london", "巴黎": "paris", "纽约": "new-york",
        "洛杉矶": "los-angeles", "悉尼": "sydney", "迪拜": "dubai"
    }

    city_query = city_map.get(city, city.lower())

    try:
        url = f"{API_BASE}/feed/{city_query}/?token={token}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") != "ok":
            return {"error": data.get("data", "无法获取数据"), "city": city}

        aqi_data = data.get("data", {})
        aqi_value = aqi_data.get("aqi", 0)

        if isinstance(aqi_value, str):
            aqi_value = 0

        level, emoji, description = get_aqi_level(aqi_value)

        # 污染物数据
        iaqi = aqi_data.get("iaqi", {})
        pollutants = {}
        if "pm25" in iaqi:
            pollutants["PM2.5"] = iaqi["pm25"].get("v", 0)
        if "pm10" in iaqi:
            pollutants["PM10"] = iaqi["pm10"].get("v", 0)
        if "o3" in iaqi:
            pollutants["O3"] = iaqi["o3"].get("v", 0)

        return {
            "city": aqi_data.get("city", {}).get("name", city),
            "aqi": aqi_value,
            "level": level,
            "emoji": emoji,
            "description": description,
            "pollutants": pollutants,
            "dominant_pollutant": aqi_data.get("dominentpol"),
            "updated_at": aqi_data.get("time", {}).get("s", "")
        }

    except Exception as e:
        return {"error": str(e), "city": city}


def get_health_advice(aqi: int) -> Dict:
    """
    根据 AQI 获取健康建议

    Args:
        aqi: 空气质量指数

    Returns:
        健康建议
    """
    if aqi <= 50:
        return {
            "outdoor_activity": "适宜",
            "exercise": "适合户外运动",
            "mask": "无需佩戴",
            "window": "建议开窗通风",
            "sensitive_groups": "无需特别注意",
            "score_impact": 0  # 对出行评分无影响
        }
    elif aqi <= 100:
        return {
            "outdoor_activity": "基本适宜",
            "exercise": "可正常户外运动",
            "mask": "敏感人群可佩戴",
            "window": "可以开窗",
            "sensitive_groups": "敏感人群适当减少户外",
            "score_impact": -5
        }
    elif aqi <= 150:
        return {
            "outdoor_activity": "减少",
            "exercise": "减少户外剧烈运动",
            "mask": "建议佩戴口罩",
            "window": "减少开窗",
            "sensitive_groups": "敏感人群避免外出",
            "score_impact": -15
        }
    elif aqi <= 200:
        return {
            "outdoor_activity": "避免",
            "exercise": "避免户外运动",
            "mask": "必须佩戴 N95/KN95",
            "window": "关闭门窗",
            "sensitive_groups": "所有人减少外出",
            "score_impact": -25
        }
    else:
        return {
            "outdoor_activity": "禁止",
            "exercise": "禁止户外活动",
            "mask": "必须专业防护",
            "window": "紧闭门窗",
            "sensitive_groups": "所有人留在室内",
            "score_impact": -40
        }
