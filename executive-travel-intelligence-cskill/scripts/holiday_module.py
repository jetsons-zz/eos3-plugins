"""
Holiday Module - 节假日模块
全球主要国家/地区节假日和股市休市日历
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

# 2025年主要节假日数据
HOLIDAYS_2025 = {
    "中国": [
        {"date": "2025-01-01", "name": "元旦", "type": "public"},
        {"date": "2025-01-28", "name": "春节", "type": "public", "duration": 7},
        {"date": "2025-04-04", "name": "清明节", "type": "public"},
        {"date": "2025-05-01", "name": "劳动节", "type": "public", "duration": 5},
        {"date": "2025-05-31", "name": "端午节", "type": "public"},
        {"date": "2025-10-01", "name": "国庆节", "type": "public", "duration": 7},
        {"date": "2025-10-06", "name": "中秋节", "type": "public"},
    ],
    "日本": [
        {"date": "2025-01-01", "name": "元日", "type": "public"},
        {"date": "2025-01-13", "name": "成人の日", "type": "public"},
        {"date": "2025-02-11", "name": "建国記念の日", "type": "public"},
        {"date": "2025-02-23", "name": "天皇誕生日", "type": "public"},
        {"date": "2025-03-20", "name": "春分の日", "type": "public"},
        {"date": "2025-04-29", "name": "昭和の日", "type": "public"},
        {"date": "2025-05-03", "name": "憲法記念日", "type": "public"},
        {"date": "2025-05-04", "name": "みどりの日", "type": "public"},
        {"date": "2025-05-05", "name": "こどもの日", "type": "public"},
        {"date": "2025-07-21", "name": "海の日", "type": "public"},
        {"date": "2025-08-11", "name": "山の日", "type": "public"},
        {"date": "2025-09-15", "name": "敬老の日", "type": "public"},
        {"date": "2025-09-23", "name": "秋分の日", "type": "public"},
        {"date": "2025-10-13", "name": "スポーツの日", "type": "public"},
        {"date": "2025-11-03", "name": "文化の日", "type": "public"},
        {"date": "2025-11-23", "name": "勤労感謝の日", "type": "public"},
    ],
    "美国": [
        {"date": "2025-01-01", "name": "New Year's Day", "type": "public"},
        {"date": "2025-01-20", "name": "MLK Day", "type": "public"},
        {"date": "2025-02-17", "name": "Presidents' Day", "type": "public"},
        {"date": "2025-05-26", "name": "Memorial Day", "type": "public"},
        {"date": "2025-07-04", "name": "Independence Day", "type": "public"},
        {"date": "2025-09-01", "name": "Labor Day", "type": "public"},
        {"date": "2025-10-13", "name": "Columbus Day", "type": "public"},
        {"date": "2025-11-11", "name": "Veterans Day", "type": "public"},
        {"date": "2025-11-27", "name": "Thanksgiving", "type": "public"},
        {"date": "2025-12-25", "name": "Christmas", "type": "public"},
    ],
    "英国": [
        {"date": "2025-01-01", "name": "New Year's Day", "type": "public"},
        {"date": "2025-04-18", "name": "Good Friday", "type": "public"},
        {"date": "2025-04-21", "name": "Easter Monday", "type": "public"},
        {"date": "2025-05-05", "name": "Early May Bank Holiday", "type": "public"},
        {"date": "2025-05-26", "name": "Spring Bank Holiday", "type": "public"},
        {"date": "2025-08-25", "name": "Summer Bank Holiday", "type": "public"},
        {"date": "2025-12-25", "name": "Christmas Day", "type": "public"},
        {"date": "2025-12-26", "name": "Boxing Day", "type": "public"},
    ],
    "香港": [
        {"date": "2025-01-01", "name": "元旦", "type": "public"},
        {"date": "2025-01-29", "name": "农历年初一", "type": "public", "duration": 3},
        {"date": "2025-04-04", "name": "清明节", "type": "public"},
        {"date": "2025-04-18", "name": "耶稣受难节", "type": "public"},
        {"date": "2025-05-01", "name": "劳动节", "type": "public"},
        {"date": "2025-05-05", "name": "佛诞", "type": "public"},
        {"date": "2025-05-31", "name": "端午节", "type": "public"},
        {"date": "2025-07-01", "name": "香港特别行政区成立纪念日", "type": "public"},
        {"date": "2025-10-01", "name": "国庆日", "type": "public"},
        {"date": "2025-10-07", "name": "中秋节翌日", "type": "public"},
        {"date": "2025-10-29", "name": "重阳节", "type": "public"},
        {"date": "2025-12-25", "name": "圣诞节", "type": "public"},
        {"date": "2025-12-26", "name": "圣诞节后第一个周日", "type": "public"},
    ],
    "新加坡": [
        {"date": "2025-01-01", "name": "New Year's Day", "type": "public"},
        {"date": "2025-01-29", "name": "Chinese New Year", "type": "public", "duration": 2},
        {"date": "2025-03-31", "name": "Hari Raya Puasa", "type": "public"},
        {"date": "2025-04-18", "name": "Good Friday", "type": "public"},
        {"date": "2025-05-01", "name": "Labour Day", "type": "public"},
        {"date": "2025-05-12", "name": "Vesak Day", "type": "public"},
        {"date": "2025-06-07", "name": "Hari Raya Haji", "type": "public"},
        {"date": "2025-08-09", "name": "National Day", "type": "public"},
        {"date": "2025-10-20", "name": "Deepavali", "type": "public"},
        {"date": "2025-12-25", "name": "Christmas Day", "type": "public"},
    ],
}

# 城市到国家/地区映射
CITY_TO_COUNTRY = {
    "东京": "日本", "tokyo": "日本",
    "北京": "中国", "beijing": "中国",
    "上海": "中国", "shanghai": "中国",
    "香港": "香港", "hongkong": "香港",
    "新加坡": "新加坡", "singapore": "新加坡",
    "纽约": "美国", "newyork": "美国", "new york": "美国",
    "洛杉矶": "美国", "losangeles": "美国", "los angeles": "美国",
    "伦敦": "英国", "london": "英国",
    "巴黎": "英国", "paris": "英国",  # 简化处理，实际法国节假日不同
    "悉尼": "美国", "sydney": "美国",  # 简化处理
    "首尔": "日本", "seoul": "日本",  # 简化处理，韩国节假日类似
}


def get_holidays(
    city: str,
    start_date: str = None,
    end_date: str = None
) -> Dict:
    """
    获取城市所在国家/地区的节假日

    Args:
        city: 城市名称
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        节假日列表
    """
    city_lower = city.lower().replace(" ", "")
    country = None

    for name, c in CITY_TO_COUNTRY.items():
        if name.lower().replace(" ", "") == city_lower:
            country = c
            break

    if not country:
        country = "中国"  # 默认

    holidays = HOLIDAYS_2025.get(country, [])

    # 如果指定了日期范围，过滤
    if start_date or end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else date(2025, 1, 1)
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else date(2025, 12, 31)

        filtered = []
        for h in holidays:
            h_date = datetime.strptime(h["date"], "%Y-%m-%d").date()
            if start <= h_date <= end:
                filtered.append(h)
        holidays = filtered

    return {
        "city": city,
        "country": country,
        "holidays": holidays,
        "count": len(holidays)
    }


def check_business_days(
    city: str,
    start_date: str,
    end_date: str
) -> Dict:
    """
    检查日期范围内的工作日情况

    Args:
        city: 城市名称
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        工作日分析
    """
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    # 获取节假日
    holidays_data = get_holidays(city, start_date, end_date)
    holiday_dates = set()

    for h in holidays_data["holidays"]:
        h_date = datetime.strptime(h["date"], "%Y-%m-%d").date()
        duration = h.get("duration", 1)
        for i in range(duration):
            holiday_dates.add(h_date + timedelta(days=i))

    # 统计
    total_days = (end - start).days + 1
    business_days = 0
    weekend_days = 0
    holiday_days = 0

    current = start
    day_details = []

    while current <= end:
        is_weekend = current.weekday() >= 5
        is_holiday = current in holiday_dates

        day_type = "工作日"
        if is_weekend:
            day_type = "周末"
            weekend_days += 1
        elif is_holiday:
            day_type = "节假日"
            holiday_days += 1
        else:
            business_days += 1

        day_details.append({
            "date": current.strftime("%Y-%m-%d"),
            "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][current.weekday()],
            "type": day_type
        })

        current += timedelta(days=1)

    # 判断是否有问题
    warnings = []
    if holiday_days > 0:
        warnings.append(f"行程包含 {holiday_days} 天节假日，部分商业活动可能受限")
    if weekend_days > total_days * 0.5:
        warnings.append("行程大部分在周末，请确认会议安排")

    return {
        "city": city,
        "period": f"{start_date} 至 {end_date}",
        "total_days": total_days,
        "business_days": business_days,
        "weekend_days": weekend_days,
        "holiday_days": holiday_days,
        "business_day_ratio": round(business_days / total_days * 100, 1),
        "day_details": day_details,
        "holidays_in_period": holidays_data["holidays"],
        "warnings": warnings,
        "is_good_for_business": business_days >= total_days * 0.5
    }


def get_upcoming_holidays(city: str, days: int = 30) -> List[Dict]:
    """
    获取未来N天内的节假日

    Args:
        city: 城市名称
        days: 未来天数

    Returns:
        即将到来的节假日
    """
    today = date.today()
    end = today + timedelta(days=days)

    holidays_data = get_holidays(
        city,
        today.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d")
    )

    upcoming = []
    for h in holidays_data["holidays"]:
        h_date = datetime.strptime(h["date"], "%Y-%m-%d").date()
        days_until = (h_date - today).days
        upcoming.append({
            **h,
            "days_until": days_until,
            "countdown": f"{days_until}天后" if days_until > 0 else "今天"
        })

    return upcoming
