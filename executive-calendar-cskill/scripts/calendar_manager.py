"""
Calendar Manager Module - 日历管理模块
日程管理、冲突检测、空闲时段查找
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 模拟日历存储
CALENDAR_STORE = {
    "events": []
}

# 示例日程数据
SAMPLE_EVENTS = [
    {
        "id": "evt_001",
        "title": "团队周会",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start": "09:00",
        "end": "10:00",
        "type": "internal",
        "location": "会议室A",
        "participants": ["团队成员"],
        "recurring": "weekly"
    },
    {
        "id": "evt_002",
        "title": "投资人电话会",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start": "14:00",
        "end": "15:00",
        "type": "external",
        "location": "Zoom",
        "participants": ["红杉资本 张总"],
        "priority": "high"
    },
    {
        "id": "evt_003",
        "title": "产品评审",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start": "16:00",
        "end": "17:30",
        "type": "internal",
        "location": "大会议室",
        "participants": ["产品团队", "研发团队"]
    },
    {
        "id": "evt_004",
        "title": "晚餐会 - 客户招待",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start": "19:00",
        "end": "21:00",
        "type": "external",
        "location": "外滩某酒店",
        "participants": ["腾讯 王总"],
        "priority": "high"
    }
]


def initialize_calendar():
    """初始化日历数据"""
    if not CALENDAR_STORE["events"]:
        CALENDAR_STORE["events"] = SAMPLE_EVENTS.copy()


def add_event(
    title: str,
    date: str,
    start: str,
    end: str,
    event_type: str = "general",
    location: str = "",
    participants: List[str] = None,
    priority: str = "normal"
) -> Dict:
    """
    添加日程事件

    Args:
        title: 事件标题
        date: 日期 (YYYY-MM-DD)
        start: 开始时间 (HH:MM)
        end: 结束时间 (HH:MM)
        event_type: 事件类型 (internal/external/personal)
        location: 地点
        participants: 参与者列表
        priority: 优先级 (low/normal/high)

    Returns:
        创建结果
    """
    initialize_calendar()

    if participants is None:
        participants = []

    # 检查冲突
    conflicts = check_conflicts(date, start, end)
    if conflicts.get("has_conflict"):
        return {
            "status": "warning",
            "message": "存在时间冲突",
            "conflicts": conflicts.get("conflicting_events", []),
            "suggestion": "请选择其他时间或处理冲突"
        }

    # 生成事件ID
    event_id = f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    event = {
        "id": event_id,
        "title": title,
        "date": date,
        "start": start,
        "end": end,
        "type": event_type,
        "location": location,
        "participants": participants,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    CALENDAR_STORE["events"].append(event)

    return {
        "status": "success",
        "message": f"已添加: {title}",
        "event": event
    }


def get_today_agenda() -> Dict:
    """
    获取今日日程

    Returns:
        今日日程列表
    """
    initialize_calendar()

    today = datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in CALENDAR_STORE["events"] if e.get("date") == today]

    # 按开始时间排序
    sorted_events = sorted(today_events, key=lambda x: x.get("start", "00:00"))

    # 计算统计
    total_minutes = 0
    for e in sorted_events:
        start = e.get("start", "00:00")
        end = e.get("end", "00:00")
        start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
        end_min = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
        total_minutes += (end_min - start_min)

    return {
        "status": "success",
        "date": today,
        "date_formatted": datetime.now().strftime("%Y年%m月%d日 %A"),
        "event_count": len(sorted_events),
        "total_hours": round(total_minutes / 60, 1),
        "events": sorted_events,
        "next_event": sorted_events[0] if sorted_events else None,
        "free_time_hours": round(8 - total_minutes / 60, 1)  # 假设8小时工作日
    }


def get_week_agenda(start_date: str = None) -> Dict:
    """
    获取本周日程

    Args:
        start_date: 起始日期，默认为今天

    Returns:
        本周日程
    """
    initialize_calendar()

    if start_date is None:
        start = datetime.now()
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")

    # 计算本周范围
    week_start = start - timedelta(days=start.weekday())
    week_end = week_start + timedelta(days=6)

    week_events = {}
    daily_stats = []

    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_events = [e for e in CALENDAR_STORE["events"] if e.get("date") == day_str]
        week_events[day_str] = sorted(day_events, key=lambda x: x.get("start", "00:00"))

        # 计算每日统计
        total_minutes = 0
        for e in day_events:
            start_time = e.get("start", "00:00")
            end_time = e.get("end", "00:00")
            start_min = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])
            end_min = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])
            total_minutes += (end_min - start_min)

        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        daily_stats.append({
            "date": day_str,
            "weekday": weekday_names[i],
            "event_count": len(day_events),
            "meeting_hours": round(total_minutes / 60, 1),
            "busy_level": "🔴" if total_minutes > 360 else "🟡" if total_minutes > 180 else "🟢"
        })

    total_events = sum(len(events) for events in week_events.values())

    return {
        "status": "success",
        "week_range": f"{week_start.strftime('%Y-%m-%d')} 至 {week_end.strftime('%Y-%m-%d')}",
        "total_events": total_events,
        "daily_breakdown": daily_stats,
        "events_by_day": week_events,
        "busiest_day": max(daily_stats, key=lambda x: x["meeting_hours"])["weekday"] if daily_stats else None,
        "lightest_day": min(daily_stats, key=lambda x: x["meeting_hours"])["weekday"] if daily_stats else None
    }


def check_conflicts(date: str, start: str, end: str) -> Dict:
    """
    检查时间冲突

    Args:
        date: 日期
        start: 开始时间
        end: 结束时间

    Returns:
        冲突检查结果
    """
    initialize_calendar()

    start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
    end_min = int(end.split(":")[0]) * 60 + int(end.split(":")[1])

    conflicts = []

    for event in CALENDAR_STORE["events"]:
        if event.get("date") != date:
            continue

        e_start = event.get("start", "00:00")
        e_end = event.get("end", "00:00")
        e_start_min = int(e_start.split(":")[0]) * 60 + int(e_start.split(":")[1])
        e_end_min = int(e_end.split(":")[0]) * 60 + int(e_end.split(":")[1])

        # 检查重叠
        if not (end_min <= e_start_min or start_min >= e_end_min):
            conflicts.append(event)

    return {
        "status": "success",
        "has_conflict": len(conflicts) > 0,
        "conflict_count": len(conflicts),
        "conflicting_events": conflicts
    }


def get_free_slots(date: str, min_duration: int = 30) -> Dict:
    """
    获取空闲时段

    Args:
        date: 日期
        min_duration: 最小时段长度（分钟）

    Returns:
        空闲时段列表
    """
    initialize_calendar()

    # 工作时间范围
    work_start = 9 * 60  # 9:00
    work_end = 18 * 60   # 18:00

    # 获取当天所有事件
    day_events = [e for e in CALENDAR_STORE["events"] if e.get("date") == date]
    sorted_events = sorted(day_events, key=lambda x: x.get("start", "00:00"))

    # 找出空闲时段
    free_slots = []
    current_time = work_start

    for event in sorted_events:
        e_start = event.get("start", "09:00")
        e_end = event.get("end", "09:00")
        e_start_min = int(e_start.split(":")[0]) * 60 + int(e_start.split(":")[1])
        e_end_min = int(e_end.split(":")[0]) * 60 + int(e_end.split(":")[1])

        if e_start_min > current_time:
            gap = e_start_min - current_time
            if gap >= min_duration:
                free_slots.append({
                    "start": f"{current_time // 60:02d}:{current_time % 60:02d}",
                    "end": f"{e_start_min // 60:02d}:{e_start_min % 60:02d}",
                    "duration_minutes": gap,
                    "quality": "⭐⭐⭐" if gap >= 120 else "⭐⭐" if gap >= 60 else "⭐"
                })

        current_time = max(current_time, e_end_min)

    # 检查工作日结束前的时间
    if current_time < work_end:
        gap = work_end - current_time
        if gap >= min_duration:
            free_slots.append({
                "start": f"{current_time // 60:02d}:{current_time % 60:02d}",
                "end": f"{work_end // 60:02d}:{work_end % 60:02d}",
                "duration_minutes": gap,
                "quality": "⭐⭐⭐" if gap >= 120 else "⭐⭐" if gap >= 60 else "⭐"
            })

    total_free = sum(s["duration_minutes"] for s in free_slots)

    return {
        "status": "success",
        "date": date,
        "free_slots": free_slots,
        "slot_count": len(free_slots),
        "total_free_minutes": total_free,
        "total_free_hours": round(total_free / 60, 1),
        "longest_slot": max(free_slots, key=lambda x: x["duration_minutes"]) if free_slots else None
    }


def clear_calendar():
    """清空日历（用于测试）"""
    CALENDAR_STORE["events"] = []
    return {"status": "success", "message": "日历已清空"}


def delete_event(event_id: str) -> Dict:
    """
    删除事件

    Args:
        event_id: 事件ID

    Returns:
        删除结果
    """
    initialize_calendar()

    for i, event in enumerate(CALENDAR_STORE["events"]):
        if event.get("id") == event_id:
            deleted = CALENDAR_STORE["events"].pop(i)
            return {
                "status": "success",
                "message": f"已删除: {deleted.get('title', '未知事件')}",
                "deleted_event": deleted
            }

    return {
        "status": "error",
        "message": f"未找到事件: {event_id}"
    }


def update_event(event_id: str, updates: Dict) -> Dict:
    """
    更新事件

    Args:
        event_id: 事件ID
        updates: 更新内容

    Returns:
        更新结果
    """
    initialize_calendar()

    for event in CALENDAR_STORE["events"]:
        if event.get("id") == event_id:
            # 如果更新了时间，检查冲突
            if "start" in updates or "end" in updates or "date" in updates:
                new_date = updates.get("date", event.get("date"))
                new_start = updates.get("start", event.get("start"))
                new_end = updates.get("end", event.get("end"))

                # 临时移除当前事件再检查
                temp_events = [e for e in CALENDAR_STORE["events"] if e.get("id") != event_id]
                original_events = CALENDAR_STORE["events"]
                CALENDAR_STORE["events"] = temp_events

                conflicts = check_conflicts(new_date, new_start, new_end)

                CALENDAR_STORE["events"] = original_events

                if conflicts.get("has_conflict"):
                    return {
                        "status": "warning",
                        "message": "更新后存在时间冲突",
                        "conflicts": conflicts.get("conflicting_events", [])
                    }

            # 应用更新
            event.update(updates)
            event["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return {
                "status": "success",
                "message": "事件已更新",
                "event": event
            }

    return {
        "status": "error",
        "message": f"未找到事件: {event_id}"
    }
