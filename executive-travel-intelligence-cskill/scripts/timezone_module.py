"""
Timezone Module - 时区模块
处理全球时区转换和会议时间优化
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

# 主要城市时区信息 (相对于 UTC 的小时偏移)
TIMEZONE_DATA = {
    # 亚太
    "东京": {"offset": 9, "name": "JST", "dst": False},
    "tokyo": {"offset": 9, "name": "JST", "dst": False},
    "北京": {"offset": 8, "name": "CST", "dst": False},
    "beijing": {"offset": 8, "name": "CST", "dst": False},
    "上海": {"offset": 8, "name": "CST", "dst": False},
    "shanghai": {"offset": 8, "name": "CST", "dst": False},
    "香港": {"offset": 8, "name": "HKT", "dst": False},
    "hongkong": {"offset": 8, "name": "HKT", "dst": False},
    "新加坡": {"offset": 8, "name": "SGT", "dst": False},
    "singapore": {"offset": 8, "name": "SGT", "dst": False},
    "首尔": {"offset": 9, "name": "KST", "dst": False},
    "seoul": {"offset": 9, "name": "KST", "dst": False},
    "悉尼": {"offset": 11, "name": "AEDT", "dst": True},  # 夏令时
    "sydney": {"offset": 11, "name": "AEDT", "dst": True},
    "迪拜": {"offset": 4, "name": "GST", "dst": False},
    "dubai": {"offset": 4, "name": "GST", "dst": False},
    # 欧洲
    "伦敦": {"offset": 0, "name": "GMT", "dst": True},
    "london": {"offset": 0, "name": "GMT", "dst": True},
    "巴黎": {"offset": 1, "name": "CET", "dst": True},
    "paris": {"offset": 1, "name": "CET", "dst": True},
    "法兰克福": {"offset": 1, "name": "CET", "dst": True},
    "frankfurt": {"offset": 1, "name": "CET", "dst": True},
    "苏黎世": {"offset": 1, "name": "CET", "dst": True},
    "zurich": {"offset": 1, "name": "CET", "dst": True},
    # 美洲
    "纽约": {"offset": -5, "name": "EST", "dst": True},
    "newyork": {"offset": -5, "name": "EST", "dst": True},
    "new york": {"offset": -5, "name": "EST", "dst": True},
    "洛杉矶": {"offset": -8, "name": "PST", "dst": True},
    "losangeles": {"offset": -8, "name": "PST", "dst": True},
    "los angeles": {"offset": -8, "name": "PST", "dst": True},
    "旧金山": {"offset": -8, "name": "PST", "dst": True},
    "san francisco": {"offset": -8, "name": "PST", "dst": True},
    "多伦多": {"offset": -5, "name": "EST", "dst": True},
    "toronto": {"offset": -5, "name": "EST", "dst": True},
}


def get_timezone_info(origin: str, destination: str) -> Dict:
    """
    获取两地时区信息

    Args:
        origin: 出发地
        destination: 目的地

    Returns:
        时区对比信息
    """
    origin_lower = origin.lower().replace(" ", "")
    dest_lower = destination.lower().replace(" ", "")

    origin_tz = None
    dest_tz = None

    for name, tz in TIMEZONE_DATA.items():
        if name.lower().replace(" ", "") == origin_lower:
            origin_tz = tz
        if name.lower().replace(" ", "") == dest_lower:
            dest_tz = tz

    if not origin_tz:
        return {"error": f"未找到时区: {origin}"}
    if not dest_tz:
        return {"error": f"未找到时区: {destination}"}

    # 计算时差
    time_diff = dest_tz["offset"] - origin_tz["offset"]

    # 当前时间示例
    now_utc = datetime.utcnow()
    origin_time = now_utc + timedelta(hours=origin_tz["offset"])
    dest_time = now_utc + timedelta(hours=dest_tz["offset"])

    # 时差描述
    if time_diff > 0:
        diff_desc = f"{destination}比{origin}快 {time_diff} 小时"
    elif time_diff < 0:
        diff_desc = f"{destination}比{origin}慢 {abs(time_diff)} 小时"
    else:
        diff_desc = f"{destination}和{origin}时间相同"

    return {
        "origin": {
            "city": origin,
            "timezone": origin_tz["name"],
            "utc_offset": origin_tz["offset"],
            "current_time": origin_time.strftime("%H:%M")
        },
        "destination": {
            "city": destination,
            "timezone": dest_tz["name"],
            "utc_offset": dest_tz["offset"],
            "current_time": dest_time.strftime("%H:%M")
        },
        "time_difference": time_diff,
        "time_difference_desc": diff_desc,
        "conversion_examples": [
            {
                "origin_time": "09:00",
                "dest_time": f"{(9 + time_diff) % 24:02d}:00"
            },
            {
                "origin_time": "14:00",
                "dest_time": f"{(14 + time_diff) % 24:02d}:00"
            },
            {
                "origin_time": "18:00",
                "dest_time": f"{(18 + time_diff) % 24:02d}:00"
            }
        ],
        "jet_lag_advice": _get_jet_lag_advice(abs(time_diff))
    }


def _get_jet_lag_advice(hours_diff: int) -> Dict:
    """获取倒时差建议"""
    if hours_diff <= 2:
        return {
            "severity": "轻微",
            "adjustment_days": 0,
            "advice": "时差较小，无需特别调整"
        }
    elif hours_diff <= 5:
        return {
            "severity": "中等",
            "adjustment_days": 1,
            "advice": "建议提前1天调整作息，到达后多晒太阳"
        }
    elif hours_diff <= 8:
        return {
            "severity": "明显",
            "adjustment_days": 2,
            "advice": "建议提前2天逐步调整作息，避免第一天安排重要会议"
        }
    else:
        return {
            "severity": "严重",
            "adjustment_days": 3,
            "advice": "建议提前3天开始调整，到达后避免立即高强度工作，可考虑褪黑素辅助"
        }


def get_best_meeting_times(
    cities: List[str],
    duration_hours: int = 1
) -> Dict:
    """
    找出多个城市的最佳会议时间

    Args:
        cities: 参与城市列表
        duration_hours: 会议时长

    Returns:
        最佳会议时间建议
    """
    # 获取各城市时区
    city_timezones = []
    for city in cities:
        city_lower = city.lower().replace(" ", "")
        for name, tz in TIMEZONE_DATA.items():
            if name.lower().replace(" ", "") == city_lower:
                city_timezones.append({
                    "city": city,
                    "offset": tz["offset"]
                })
                break

    if len(city_timezones) < len(cities):
        return {"error": "部分城市时区未找到"}

    # 定义工作时间 (当地时间 9:00-18:00)
    work_start = 9
    work_end = 18

    # 寻找所有城市都在工作时间内的 UTC 时段
    valid_slots = []

    for utc_hour in range(24):
        all_valid = True
        local_times = []

        for tz in city_timezones:
            local_hour = (utc_hour + tz["offset"]) % 24
            local_times.append({
                "city": tz["city"],
                "local_time": f"{local_hour:02d}:00"
            })

            # 检查是否在工作时间内
            if not (work_start <= local_hour < work_end - duration_hours + 1):
                all_valid = False

        if all_valid:
            valid_slots.append({
                "utc_time": f"{utc_hour:02d}:00 UTC",
                "local_times": local_times,
                "quality": _rate_meeting_time(local_times)
            })

    # 按质量排序
    valid_slots.sort(key=lambda x: x["quality"], reverse=True)

    if not valid_slots:
        # 找出最接近的时间
        return {
            "cities": cities,
            "optimal_slots": [],
            "message": "没有所有城市都在工作时间内的时段",
            "suggestion": "考虑部分参与者在非标准工作时间参会"
        }

    return {
        "cities": cities,
        "duration_hours": duration_hours,
        "optimal_slots": valid_slots[:3],  # 返回最佳的3个时段
        "recommendation": valid_slots[0] if valid_slots else None
    }


def _rate_meeting_time(local_times: List[Dict]) -> int:
    """评估会议时间质量 (避开午餐和太早/太晚)"""
    score = 100

    for lt in local_times:
        hour = int(lt["local_time"].split(":")[0])

        # 理想时间: 10:00-11:00, 14:00-16:00
        if 10 <= hour <= 11 or 14 <= hour <= 16:
            pass  # 理想
        elif 12 <= hour <= 13:
            score -= 10  # 午餐时间
        elif hour == 9 or hour == 17:
            score -= 5  # 边缘时间
        else:
            score -= 15  # 非理想

    return score


def convert_time(time_str: str, from_city: str, to_city: str) -> Dict:
    """
    转换时间

    Args:
        time_str: 时间字符串 (HH:MM)
        from_city: 源城市
        to_city: 目标城市

    Returns:
        转换后的时间
    """
    try:
        hour, minute = map(int, time_str.split(":"))
    except:
        return {"error": "时间格式错误，请使用 HH:MM"}

    tz_info = get_timezone_info(from_city, to_city)
    if "error" in tz_info:
        return tz_info

    diff = tz_info["time_difference"]
    new_hour = (hour + diff) % 24
    day_change = (hour + diff) // 24

    result = {
        "original": f"{hour:02d}:{minute:02d}",
        "original_city": from_city,
        "converted": f"{new_hour:02d}:{minute:02d}",
        "converted_city": to_city
    }

    if day_change > 0:
        result["note"] = "次日"
    elif day_change < 0:
        result["note"] = "前一日"

    return result
