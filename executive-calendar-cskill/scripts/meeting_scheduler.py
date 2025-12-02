"""
Meeting Scheduler Module - 会议安排模块
智能会议时间安排、疲劳度计算
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from .timezone_manager import get_city_time, get_business_hours_overlap, CITY_TIMEZONES


def find_optimal_meeting_time(
    participants: List[Dict],
    duration_minutes: int = 60,
    prefer_morning: bool = True
) -> Dict:
    """
    找出最佳会议时间

    Args:
        participants: 参与者列表 [{"name": "张三", "city": "北京"}, ...]
        duration_minutes: 会议时长（分钟）
        prefer_morning: 是否优先上午

    Returns:
        最佳会议时间建议
    """
    if not participants:
        return {"status": "error", "message": "请提供参与者信息"}

    cities = [p.get("city", "北京") for p in participants]
    unique_cities = list(set(cities))

    # 获取工作时间重叠
    overlap = get_business_hours_overlap(unique_cities)

    if not overlap.get("has_overlap", False):
        # 没有完美重叠，找妥协方案
        return find_compromise_time(participants, duration_minutes)

    # 有重叠，在重叠时间内找最佳时段
    overlap_by_city = overlap.get("overlap_by_city", {})

    # 解析重叠时间
    first_city = unique_cities[0]
    time_range = overlap_by_city.get(first_city, "09:00 - 18:00")
    start_str, end_str = time_range.split(" - ")
    start_hour = int(start_str.split(":")[0])
    end_hour = int(end_str.split(":")[0])

    # 选择最佳时段
    if prefer_morning and start_hour < 12:
        suggested_hour = max(start_hour, 9)
    else:
        suggested_hour = start_hour + (end_hour - start_hour) // 2

    # 生成各城市的时间
    meeting_times = {}
    base_offset = CITY_TIMEZONES.get(first_city.lower(), 8)

    for city in unique_cities:
        city_offset = None
        for c, o in CITY_TIMEZONES.items():
            if city.lower() == c.lower() or city.lower() in c.lower():
                city_offset = o
                break
        if city_offset is not None:
            local_hour = suggested_hour + (city_offset - base_offset)
            if local_hour >= 24:
                local_hour -= 24
                day_note = " (次日)"
            elif local_hour < 0:
                local_hour += 24
                day_note = " (前一天)"
            else:
                day_note = ""
            meeting_times[city] = f"{int(local_hour):02d}:00{day_note}"

    # 评估这个时间的适合度
    scores = []
    for city, time_str in meeting_times.items():
        hour = int(time_str.split(":")[0])
        if 9 <= hour <= 11:
            scores.append(100)  # 最佳
        elif 14 <= hour <= 16:
            scores.append(90)  # 很好
        elif 8 <= hour <= 18:
            scores.append(70)  # 可接受
        elif 7 <= hour <= 20:
            scores.append(50)  # 勉强
        else:
            scores.append(20)  # 不便

    avg_score = sum(scores) / len(scores) if scores else 50

    return {
        "status": "success",
        "participants": [p.get("name", "未知") for p in participants],
        "cities_involved": unique_cities,
        "suggested_time": {
            "primary_city": first_city,
            "time": f"{suggested_hour:02d}:00",
            "all_cities": meeting_times
        },
        "duration": f"{duration_minutes}分钟",
        "convenience_score": round(avg_score, 1),
        "score_interpretation": interpret_score(avg_score),
        "overlap_hours": overlap.get("overlap_hours", 0),
        "recommendation": generate_recommendation(avg_score, meeting_times)
    }


def interpret_score(score: float) -> str:
    """解释便利度评分"""
    if score >= 90:
        return "🟢 非常便利"
    elif score >= 70:
        return "🟡 比较便利"
    elif score >= 50:
        return "🟠 需要妥协"
    else:
        return "🔴 不太方便"


def generate_recommendation(score: float, meeting_times: Dict) -> str:
    """生成建议"""
    if score >= 80:
        return "这个时间对所有参与者都很友好"
    elif score >= 60:
        return "部分参与者可能需要稍早或稍晚参加"
    else:
        inconvenient = []
        for city, time_str in meeting_times.items():
            hour = int(time_str.split(":")[0])
            if hour < 8 or hour > 19:
                inconvenient.append(city)
        if inconvenient:
            return f"对 {', '.join(inconvenient)} 的参与者不太方便，建议轮流调整"
        return "建议考虑异步沟通或录制会议"


def find_compromise_time(participants: List[Dict], duration_minutes: int) -> Dict:
    """寻找妥协时间方案"""
    cities = list(set([p.get("city", "北京") for p in participants]))

    # 找出时差最大的城市对
    offsets = {}
    for city in cities:
        for c, o in CITY_TIMEZONES.items():
            if city.lower() == c.lower() or city.lower() in c.lower():
                offsets[city] = o
                break

    if len(offsets) < 2:
        return {"status": "error", "message": "城市信息不足"}

    # 计算折中时间
    min_offset_city = min(offsets, key=offsets.get)
    max_offset_city = max(offsets, key=offsets.get)
    offset_diff = offsets[max_offset_city] - offsets[min_offset_city]

    # 建议两个方案：偏向早起和偏向晚归
    proposals = []

    # 方案1：让东边的城市早起（8:00开始）
    proposal1 = {}
    base_hour = 8
    for city, offset in offsets.items():
        local = base_hour + (offset - offsets[max_offset_city])
        proposal1[city] = f"{int(local):02d}:00" if 0 <= local < 24 else f"{int(local % 24):02d}:00"

    # 方案2：让西边的城市晚归（20:00结束）
    proposal2 = {}
    base_hour = 19
    for city, offset in offsets.items():
        local = base_hour + (offset - offsets[min_offset_city])
        proposal2[city] = f"{int(local):02d}:00" if 0 <= local < 24 else f"{int(local % 24):02d}:00"

    return {
        "status": "success",
        "has_overlap": False,
        "time_difference": f"{offset_diff}小时",
        "cities": cities,
        "proposals": [
            {
                "name": "早起方案",
                "description": f"{max_offset_city} 早8点开始",
                "times": proposal1
            },
            {
                "name": "晚归方案",
                "description": f"{min_offset_city} 晚7点开始",
                "times": proposal2
            }
        ],
        "recommendation": "建议轮流使用两个方案，公平分担不便"
    }


def suggest_meeting_slots(
    date: str,
    participants: List[Dict],
    existing_meetings: List[Dict] = None,
    slot_duration: int = 60
) -> Dict:
    """
    推荐可用会议时段

    Args:
        date: 日期 (YYYY-MM-DD)
        participants: 参与者列表
        existing_meetings: 已有会议列表
        slot_duration: 时段长度（分钟）

    Returns:
        可用时段列表
    """
    if existing_meetings is None:
        existing_meetings = []

    # 获取重叠工作时间
    cities = list(set([p.get("city", "北京") for p in participants]))
    overlap = get_business_hours_overlap(cities)

    if not overlap.get("has_overlap"):
        return {
            "status": "warning",
            "message": "参与者城市没有工作时间重叠",
            "suggestion": "考虑异步沟通或轮流牺牲"
        }

    # 假设使用第一个城市的时间
    first_city = cities[0]
    time_range = overlap.get("overlap_by_city", {}).get(first_city, "09:00 - 18:00")
    start_str, end_str = time_range.split(" - ")
    start_hour = int(start_str.split(":")[0])
    end_hour = int(end_str.split(":")[0])

    # 生成可用时段
    slots = []
    current_hour = start_hour

    while current_hour + (slot_duration / 60) <= end_hour:
        slot_start = f"{current_hour:02d}:00"
        slot_end = f"{current_hour + slot_duration // 60:02d}:{slot_duration % 60:02d}"

        # 检查是否与现有会议冲突
        is_available = True
        for meeting in existing_meetings:
            # 简单的冲突检测
            if meeting.get("date") == date:
                m_start = int(meeting.get("start", "00:00").split(":")[0])
                m_end = int(meeting.get("end", "00:00").split(":")[0])
                if m_start <= current_hour < m_end:
                    is_available = False
                    break

        if is_available:
            # 评估这个时段的质量
            if 9 <= current_hour <= 11:
                quality = "⭐⭐⭐ 最佳"
            elif 14 <= current_hour <= 16:
                quality = "⭐⭐ 很好"
            else:
                quality = "⭐ 可用"

            slots.append({
                "start": slot_start,
                "end": slot_end,
                "quality": quality,
                "available": True
            })

        current_hour += 1

    return {
        "status": "success",
        "date": date,
        "reference_city": first_city,
        "available_slots": slots,
        "slot_count": len(slots),
        "recommendation": slots[0] if slots else None
    }


def calculate_meeting_fatigue(meetings: List[Dict]) -> Dict:
    """
    计算会议疲劳度

    Args:
        meetings: 当日会议列表

    Returns:
        疲劳度分析
    """
    if not meetings:
        return {
            "status": "success",
            "fatigue_score": 0,
            "fatigue_level": "🟢 轻松",
            "total_meeting_hours": 0,
            "meeting_count": 0,
            "recommendation": "今天没有会议，可以专注于深度工作"
        }

    total_minutes = 0
    meeting_count = len(meetings)
    back_to_back = 0

    # 按开始时间排序
    sorted_meetings = sorted(meetings, key=lambda x: x.get("start", "00:00"))

    for i, meeting in enumerate(sorted_meetings):
        # 计算时长
        start = meeting.get("start", "09:00")
        end = meeting.get("end", "10:00")

        start_hour, start_min = map(int, start.split(":"))
        end_hour, end_min = map(int, end.split(":"))

        duration = (end_hour * 60 + end_min) - (start_hour * 60 + start_min)
        total_minutes += duration

        # 检查是否背靠背
        if i > 0:
            prev_end = sorted_meetings[i-1].get("end", "00:00")
            prev_hour, prev_min = map(int, prev_end.split(":"))
            gap = (start_hour * 60 + start_min) - (prev_hour * 60 + prev_min)
            if gap < 15:  # 少于15分钟间隔
                back_to_back += 1

    total_hours = total_minutes / 60

    # 计算疲劳度评分 (0-100)
    fatigue_score = min(100, (
        total_hours * 10 +  # 每小时10分
        meeting_count * 5 +  # 每个会议5分
        back_to_back * 15    # 背靠背会议额外15分
    ))

    # 疲劳等级
    if fatigue_score < 30:
        fatigue_level = "🟢 轻松"
        recommendation = "会议负担合理，有足够的专注时间"
    elif fatigue_score < 50:
        fatigue_level = "🟡 适中"
        recommendation = "会议较多，注意保留休息时间"
    elif fatigue_score < 70:
        fatigue_level = "🟠 较重"
        recommendation = "会议负担较重，建议推迟非紧急会议"
    else:
        fatigue_level = "🔴 过重"
        recommendation = "会议过多，强烈建议取消或推迟部分会议"

    return {
        "status": "success",
        "fatigue_score": round(fatigue_score, 1),
        "fatigue_level": fatigue_level,
        "total_meeting_hours": round(total_hours, 1),
        "meeting_count": meeting_count,
        "back_to_back_count": back_to_back,
        "recommendation": recommendation,
        "breakdown": {
            "time_factor": f"{total_hours:.1f}小时会议",
            "count_factor": f"{meeting_count}个会议",
            "density_factor": f"{back_to_back}个背靠背"
        }
    }


def get_meeting_recommendations(meetings: List[Dict], preferences: Dict = None) -> Dict:
    """
    获取会议优化建议

    Args:
        meetings: 会议列表
        preferences: 用户偏好

    Returns:
        优化建议
    """
    if preferences is None:
        preferences = {
            "focus_time_hours": 3,  # 期望的专注时间
            "max_daily_meetings": 5,
            "prefer_morning": True
        }

    fatigue = calculate_meeting_fatigue(meetings)

    recommendations = []

    # 检查会议数量
    if len(meetings) > preferences.get("max_daily_meetings", 5):
        recommendations.append({
            "priority": "high",
            "type": "reduce",
            "suggestion": f"会议数量({len(meetings)})超过建议上限({preferences['max_daily_meetings']})"
        })

    # 检查专注时间
    meeting_hours = fatigue.get("total_meeting_hours", 0)
    available_focus = 8 - meeting_hours  # 假设8小时工作日

    if available_focus < preferences.get("focus_time_hours", 3):
        recommendations.append({
            "priority": "medium",
            "type": "reschedule",
            "suggestion": f"专注时间不足，建议推迟部分会议以保证{preferences['focus_time_hours']}小时专注时间"
        })

    # 检查背靠背
    if fatigue.get("back_to_back_count", 0) > 2:
        recommendations.append({
            "priority": "medium",
            "type": "spacing",
            "suggestion": "背靠背会议过多，建议每个会议后留15分钟缓冲"
        })

    # 检查午餐时间
    lunch_blocked = any(
        11 <= int(m.get("start", "00:00").split(":")[0]) <= 13
        for m in meetings
    )
    if lunch_blocked:
        recommendations.append({
            "priority": "low",
            "type": "wellness",
            "suggestion": "午餐时间被占用，建议保护12:00-13:00"
        })

    return {
        "status": "success",
        "current_state": fatigue,
        "recommendations": recommendations,
        "recommendation_count": len(recommendations),
        "overall_health": "健康" if len(recommendations) == 0 else "需要优化" if len(recommendations) < 3 else "亟需调整"
    }
