"""
Timezone Manager Module - 时区管理模块
处理跨时区时间转换和计算
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

# 城市时区数据库 (UTC偏移小时数)
CITY_TIMEZONES = {
    # 中国
    "北京": 8, "上海": 8, "深圳": 8, "广州": 8, "杭州": 8,
    "香港": 8, "台北": 8,

    # 日韩
    "东京": 9, "首尔": 9, "大阪": 9,

    # 东南亚
    "新加坡": 8, "曼谷": 7, "雅加达": 7, "马尼拉": 8,
    "吉隆坡": 8, "胡志明市": 7,

    # 南亚
    "孟买": 5.5, "新德里": 5.5, "班加罗尔": 5.5,

    # 中东
    "迪拜": 4, "多哈": 3, "利雅得": 3, "特拉维夫": 2,

    # 欧洲
    "伦敦": 0, "巴黎": 1, "柏林": 1, "法兰克福": 1,
    "阿姆斯特丹": 1, "苏黎世": 1, "米兰": 1, "马德里": 1,
    "莫斯科": 3, "都柏林": 0,

    # 北美
    "纽约": -5, "洛杉矶": -8, "旧金山": -8, "西雅图": -8,
    "芝加哥": -6, "波士顿": -5, "华盛顿": -5, "迈阿密": -5,
    "多伦多": -5, "温哥华": -8,

    # 南美
    "圣保罗": -3, "布宜诺斯艾利斯": -3,

    # 大洋洲
    "悉尼": 11, "墨尔本": 11, "奥克兰": 13,

    # 英文名称
    "beijing": 8, "shanghai": 8, "shenzhen": 8,
    "hong kong": 8, "hongkong": 8,
    "tokyo": 9, "seoul": 9,
    "singapore": 8, "bangkok": 7,
    "london": 0, "paris": 1, "berlin": 1, "frankfurt": 1,
    "new york": -5, "nyc": -5, "los angeles": -8, "la": -8,
    "san francisco": -8, "sf": -8, "seattle": -8,
    "sydney": 11, "melbourne": 11,
    "dubai": 4, "mumbai": 5.5,
}


def get_city_time(city: str, reference_time: datetime = None) -> Dict:
    """
    获取指定城市的当前时间

    Args:
        city: 城市名称
        reference_time: 参考时间（默认为当前UTC时间）

    Returns:
        城市时间信息
    """
    city_lower = city.lower()

    # 查找时区
    offset = None
    matched_city = city

    for c, o in CITY_TIMEZONES.items():
        if city_lower == c.lower() or city_lower in c.lower():
            offset = o
            matched_city = c
            break

    if offset is None:
        return {
            "status": "error",
            "message": f"未找到城市 {city} 的时区信息",
            "available_cities": list(set([c for c in CITY_TIMEZONES.keys() if not c.islower()]))[:20]
        }

    # 计算时间
    if reference_time is None:
        utc_now = datetime.utcnow()
    else:
        utc_now = reference_time

    # 处理半小时时区
    hours = int(offset)
    minutes = int((offset - hours) * 60)
    city_time = utc_now + timedelta(hours=hours, minutes=minutes)

    # 判断是否是工作时间
    hour = city_time.hour
    is_business_hours = 9 <= hour < 18
    is_extended_hours = 8 <= hour < 20

    # 时间描述
    if 6 <= hour < 12:
        time_of_day = "上午"
        emoji = "🌅"
    elif 12 <= hour < 14:
        time_of_day = "中午"
        emoji = "☀️"
    elif 14 <= hour < 18:
        time_of_day = "下午"
        emoji = "🌤️"
    elif 18 <= hour < 22:
        time_of_day = "晚上"
        emoji = "🌆"
    else:
        time_of_day = "深夜"
        emoji = "🌙"

    return {
        "status": "success",
        "city": matched_city,
        "utc_offset": f"UTC{offset:+.1f}" if offset != int(offset) else f"UTC{int(offset):+d}",
        "current_time": city_time.strftime("%Y-%m-%d %H:%M"),
        "time_formatted": city_time.strftime("%H:%M"),
        "date_formatted": city_time.strftime("%m月%d日 %A"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][city_time.weekday()],
        "time_of_day": time_of_day,
        "emoji": emoji,
        "is_business_hours": is_business_hours,
        "is_extended_hours": is_extended_hours,
        "note": f"{matched_city}现在是{time_of_day} {city_time.strftime('%H:%M')}"
    }


def convert_time(time_str: str, from_city: str, to_city: str) -> Dict:
    """
    时间转换

    Args:
        time_str: 时间字符串 (HH:MM 或 HH:MM AM/PM)
        from_city: 源城市
        to_city: 目标城市

    Returns:
        转换结果
    """
    # 解析时间
    try:
        if "am" in time_str.lower() or "pm" in time_str.lower():
            time_str_clean = time_str.upper().replace(" ", "")
            if "AM" in time_str_clean:
                hour = int(time_str_clean.replace("AM", "").split(":")[0])
                minute = int(time_str_clean.replace("AM", "").split(":")[1]) if ":" in time_str_clean else 0
                if hour == 12:
                    hour = 0
            else:
                hour = int(time_str_clean.replace("PM", "").split(":")[0])
                minute = int(time_str_clean.replace("PM", "").split(":")[1]) if ":" in time_str_clean else 0
                if hour != 12:
                    hour += 12
        else:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
    except:
        return {
            "status": "error",
            "message": f"无法解析时间: {time_str}，请使用 HH:MM 格式"
        }

    # 获取时区偏移
    from_offset = None
    to_offset = None

    for city, offset in CITY_TIMEZONES.items():
        if from_city.lower() == city.lower() or from_city.lower() in city.lower():
            from_offset = offset
        if to_city.lower() == city.lower() or to_city.lower() in city.lower():
            to_offset = offset

    if from_offset is None:
        return {"status": "error", "message": f"未找到城市 {from_city}"}
    if to_offset is None:
        return {"status": "error", "message": f"未找到城市 {to_city}"}

    # 计算时差
    diff = to_offset - from_offset

    # 转换时间
    new_hour = hour + int(diff)
    new_minute = minute + int((diff - int(diff)) * 60)

    if new_minute >= 60:
        new_hour += 1
        new_minute -= 60
    elif new_minute < 0:
        new_hour -= 1
        new_minute += 60

    # 处理跨天
    day_diff = 0
    if new_hour >= 24:
        day_diff = 1
        new_hour -= 24
    elif new_hour < 0:
        day_diff = -1
        new_hour += 24

    day_note = ""
    if day_diff == 1:
        day_note = " (次日)"
    elif day_diff == -1:
        day_note = " (前一天)"

    return {
        "status": "success",
        "from_city": from_city,
        "from_time": f"{hour:02d}:{minute:02d}",
        "to_city": to_city,
        "to_time": f"{new_hour:02d}:{new_minute:02d}{day_note}",
        "time_difference": f"{diff:+.1f}小时" if diff != int(diff) else f"{int(diff):+d}小时",
        "summary": f"{from_city} {hour:02d}:{minute:02d} = {to_city} {new_hour:02d}:{new_minute:02d}{day_note}"
    }


def get_time_difference(city1: str, city2: str) -> Dict:
    """
    获取两个城市的时差

    Args:
        city1: 城市1
        city2: 城市2

    Returns:
        时差信息
    """
    offset1 = None
    offset2 = None

    for city, offset in CITY_TIMEZONES.items():
        if city1.lower() == city.lower() or city1.lower() in city.lower():
            offset1 = offset
        if city2.lower() == city.lower() or city2.lower() in city.lower():
            offset2 = offset

    if offset1 is None:
        return {"status": "error", "message": f"未找到城市 {city1}"}
    if offset2 is None:
        return {"status": "error", "message": f"未找到城市 {city2}"}

    diff = offset2 - offset1

    if diff > 0:
        relation = f"{city2} 比 {city1} 快 {abs(diff)} 小时"
    elif diff < 0:
        relation = f"{city2} 比 {city1} 慢 {abs(diff)} 小时"
    else:
        relation = f"{city1} 和 {city2} 在同一时区"

    return {
        "status": "success",
        "city1": city1,
        "city1_utc": f"UTC{offset1:+.1f}" if offset1 != int(offset1) else f"UTC{int(offset1):+d}",
        "city2": city2,
        "city2_utc": f"UTC{offset2:+.1f}" if offset2 != int(offset2) else f"UTC{int(offset2):+d}",
        "difference_hours": diff,
        "relation": relation
    }


def get_business_hours_overlap(cities: List[str], work_start: int = 9, work_end: int = 18) -> Dict:
    """
    获取多个城市的工作时间重叠

    Args:
        cities: 城市列表
        work_start: 工作开始时间（小时）
        work_end: 工作结束时间（小时）

    Returns:
        重叠时间信息
    """
    if len(cities) < 2:
        return {"status": "error", "message": "至少需要2个城市"}

    # 获取各城市时区偏移
    offsets = {}
    for city in cities:
        for c, o in CITY_TIMEZONES.items():
            if city.lower() == c.lower() or city.lower() in c.lower():
                offsets[city] = o
                break

    if len(offsets) != len(cities):
        missing = [c for c in cities if c not in offsets]
        return {"status": "error", "message": f"未找到城市: {', '.join(missing)}"}

    # 以第一个城市为基准，计算各城市的工作时间在UTC的范围
    utc_ranges = []
    for city, offset in offsets.items():
        utc_start = work_start - offset
        utc_end = work_end - offset
        utc_ranges.append({
            "city": city,
            "offset": offset,
            "utc_start": utc_start,
            "utc_end": utc_end
        })

    # 找出所有城市都在工作时间的UTC时间段
    overlap_start = max(r["utc_start"] for r in utc_ranges)
    overlap_end = min(r["utc_end"] for r in utc_ranges)

    if overlap_start >= overlap_end:
        # 没有重叠
        return {
            "status": "success",
            "has_overlap": False,
            "cities": cities,
            "message": "这些城市没有工作时间重叠，建议安排异步沟通",
            "suggestion": get_best_compromise_time(offsets, work_start, work_end)
        }

    overlap_hours = overlap_end - overlap_start

    # 计算各城市的本地时间
    overlap_local = {}
    for city, offset in offsets.items():
        local_start = overlap_start + offset
        local_end = overlap_end + offset
        overlap_local[city] = f"{int(local_start):02d}:00 - {int(local_end):02d}:00"

    return {
        "status": "success",
        "has_overlap": True,
        "cities": cities,
        "overlap_hours": overlap_hours,
        "overlap_by_city": overlap_local,
        "recommendation": f"建议会议时间: {overlap_local[cities[0]]} ({cities[0]}时间)",
        "note": f"共{overlap_hours}小时重叠，是安排会议的理想时段"
    }


def get_best_compromise_time(offsets: Dict[str, float], work_start: int, work_end: int) -> str:
    """找出妥协时间"""
    # 简单策略：找出最小化不便的时间
    min_offset = min(offsets.values())
    max_offset = max(offsets.values())

    # 建议时间：让时差最大的两个城市都在可接受范围内
    # 一个城市早上8点，另一个城市不超过晚上9点
    mid_offset = (min_offset + max_offset) / 2
    suggested_utc = 8 + mid_offset  # 假设8点开始

    suggestion = "建议早会或晚会，让每个城市轮流牺牲："
    for city, offset in offsets.items():
        local_time = suggested_utc - offset + 8
        if local_time < 0:
            local_time += 24
        elif local_time >= 24:
            local_time -= 24
        suggestion += f"\n  - {city}: {int(local_time):02d}:00"

    return suggestion


def get_world_clock(cities: List[str] = None) -> str:
    """
    生成世界时钟显示

    Args:
        cities: 城市列表，默认为主要城市

    Returns:
        格式化的世界时钟
    """
    if cities is None:
        cities = ["北京", "东京", "新加坡", "伦敦", "纽约", "旧金山"]

    lines = ["🌍 世界时钟", "=" * 40]

    for city in cities:
        result = get_city_time(city)
        if result.get("status") == "success":
            emoji = result.get("emoji", "")
            time_str = result.get("time_formatted", "")
            weekday = result.get("weekday", "")
            biz = "🏢" if result.get("is_business_hours") else "🌙"
            lines.append(f"{emoji} {city:10} {time_str} {weekday} {biz}")

    lines.append("=" * 40)
    return "\n".join(lines)
