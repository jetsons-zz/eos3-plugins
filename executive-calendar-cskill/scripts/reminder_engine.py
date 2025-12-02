"""
Reminder Engine Module - 提醒引擎模块
智能会议提醒、准备事项、时差提醒
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .timezone_manager import get_city_time, get_time_difference


def generate_meeting_prep(meeting: Dict) -> Dict:
    """
    生成会议准备事项

    Args:
        meeting: 会议信息

    Returns:
        准备事项清单
    """
    title = meeting.get("title", "会议")
    meeting_type = meeting.get("type", "general")
    participants = meeting.get("participants", [])
    location = meeting.get("location", "")
    priority = meeting.get("priority", "normal")

    prep_items = []

    # 基础准备
    prep_items.append({
        "category": "基础",
        "item": "确认会议议程和目标",
        "priority": "high"
    })

    # 根据参与者准备
    if participants:
        prep_items.append({
            "category": "人员",
            "item": f"了解参与者背景: {', '.join(participants[:3])}",
            "priority": "medium"
        })

    # 根据会议类型准备
    if meeting_type == "external":
        prep_items.extend([
            {"category": "材料", "item": "准备公司介绍/产品资料", "priority": "high"},
            {"category": "着装", "item": "商务正装", "priority": "medium"},
            {"category": "礼仪", "item": "准备名片", "priority": "low"}
        ])
    elif meeting_type == "internal":
        prep_items.extend([
            {"category": "材料", "item": "更新项目进展文档", "priority": "medium"},
            {"category": "数据", "item": "准备关键指标数据", "priority": "medium"}
        ])

    # 根据地点准备
    if location:
        if "zoom" in location.lower() or "teams" in location.lower() or "腾讯会议" in location:
            prep_items.extend([
                {"category": "技术", "item": "测试视频会议软件", "priority": "medium"},
                {"category": "技术", "item": "确保网络稳定", "priority": "medium"},
                {"category": "环境", "item": "选择安静的会议背景", "priority": "low"}
            ])
        elif "酒店" in location or "餐厅" in location:
            prep_items.extend([
                {"category": "交通", "item": f"提前规划前往 {location} 的路线", "priority": "high"},
                {"category": "时间", "item": "预留30分钟交通缓冲时间", "priority": "medium"}
            ])

    # 高优先级会议额外准备
    if priority == "high":
        prep_items.extend([
            {"category": "预演", "item": "提前演练关键发言要点", "priority": "high"},
            {"category": "备份", "item": "准备备选方案/应急预案", "priority": "medium"}
        ])

    # 时间提醒
    start_time = meeting.get("start", "09:00")
    meeting_date = meeting.get("date", datetime.now().strftime("%Y-%m-%d"))

    return {
        "status": "success",
        "meeting": title,
        "date": meeting_date,
        "time": start_time,
        "prep_items": prep_items,
        "item_count": len(prep_items),
        "estimated_prep_time": f"{len(prep_items) * 5}分钟",
        "reminder": f"建议在会议开始前{30 if priority == 'high' else 15}分钟完成准备"
    }


def get_travel_reminder(meeting: Dict, current_location: str = "办公室") -> Dict:
    """
    获取出行提醒

    Args:
        meeting: 会议信息
        current_location: 当前位置

    Returns:
        出行提醒
    """
    location = meeting.get("location", "")
    start_time = meeting.get("start", "09:00")
    title = meeting.get("title", "会议")

    # 估算交通时间（简化版）
    travel_estimates = {
        "同楼层会议室": 5,
        "同园区": 10,
        "市内": 45,
        "线上": 0,
        "外地": 180,  # 需要提前更多准备
    }

    # 判断位置类型
    if "zoom" in location.lower() or "teams" in location.lower() or "腾讯会议" in location:
        location_type = "线上"
        travel_time = 0
        suggestion = "提前5分钟测试设备和网络"
    elif "会议室" in location:
        location_type = "同楼层会议室"
        travel_time = 5
        suggestion = "提前5分钟到达，调试投影/白板"
    elif "酒店" in location or "餐厅" in location or "外滩" in location:
        location_type = "市内"
        travel_time = 45
        suggestion = "建议提前1小时出发，预留堵车时间"
    else:
        location_type = "市内"
        travel_time = 30
        suggestion = "建议提前30分钟出发"

    # 计算建议出发时间
    start_hour, start_min = map(int, start_time.split(":"))
    start_minutes = start_hour * 60 + start_min
    leave_minutes = start_minutes - travel_time - 15  # 额外15分钟缓冲

    leave_hour = leave_minutes // 60
    leave_min = leave_minutes % 60

    return {
        "status": "success",
        "meeting": title,
        "location": location,
        "location_type": location_type,
        "meeting_time": start_time,
        "estimated_travel_time": f"{travel_time}分钟",
        "suggested_leave_time": f"{leave_hour:02d}:{leave_min:02d}",
        "suggestion": suggestion,
        "checklist": [
            "✅ 确认地址和路线" if location_type != "线上" else "✅ 确认会议链接",
            "✅ 带好会议材料",
            "✅ 手机充满电",
            "✅ 准备名片" if location_type == "市内" else "✅ 测试设备"
        ]
    }


def get_timezone_alert(meeting: Dict, participant_cities: List[str]) -> Dict:
    """
    获取时差提醒

    Args:
        meeting: 会议信息
        participant_cities: 参与者城市列表

    Returns:
        时差提醒
    """
    start_time = meeting.get("start", "09:00")
    title = meeting.get("title", "会议")
    base_city = "北京"  # 假设用户在北京

    alerts = []
    local_times = {}

    for city in participant_cities:
        if city.lower() == base_city.lower():
            local_times[city] = start_time
            continue

        diff = get_time_difference(base_city, city)
        if diff.get("status") != "success":
            continue

        hours_diff = diff.get("difference_hours", 0)

        # 计算当地时间
        start_hour, start_min = map(int, start_time.split(":"))
        local_hour = start_hour + hours_diff

        day_note = ""
        if local_hour >= 24:
            local_hour -= 24
            day_note = " (次日)"
        elif local_hour < 0:
            local_hour += 24
            day_note = " (前一天)"

        local_time = f"{int(local_hour):02d}:{start_min:02d}{day_note}"
        local_times[city] = local_time

        # 生成提醒
        if local_hour < 7:
            alerts.append({
                "city": city,
                "local_time": local_time,
                "severity": "high",
                "message": f"⚠️ {city} 参与者需要凌晨参会"
            })
        elif local_hour < 9:
            alerts.append({
                "city": city,
                "local_time": local_time,
                "severity": "medium",
                "message": f"📢 {city} 参与者需要早起参会"
            })
        elif local_hour >= 21:
            alerts.append({
                "city": city,
                "local_time": local_time,
                "severity": "medium",
                "message": f"📢 {city} 参与者需要晚间参会"
            })
        elif local_hour >= 23:
            alerts.append({
                "city": city,
                "local_time": local_time,
                "severity": "high",
                "message": f"⚠️ {city} 参与者需要深夜参会"
            })

    return {
        "status": "success",
        "meeting": title,
        "base_city": base_city,
        "base_time": start_time,
        "local_times": local_times,
        "alerts": alerts,
        "alert_count": len(alerts),
        "has_critical_alerts": any(a.get("severity") == "high" for a in alerts),
        "suggestion": "建议考虑调整会议时间以照顾所有时区" if alerts else "所有参与者都在合理时间参会"
    }


def generate_daily_briefing(events: List[Dict], user_city: str = "北京") -> str:
    """
    生成每日简报

    Args:
        events: 今日事件列表
        user_city: 用户所在城市

    Returns:
        格式化的每日简报
    """
    today = datetime.now()
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    lines = []
    lines.append("=" * 50)
    lines.append(f"📅 每日简报 - {today.strftime('%Y年%m月%d日')} {weekday_names[today.weekday()]}")
    lines.append("=" * 50)
    lines.append("")

    # 今日天气（简化版）
    city_time = get_city_time(user_city)
    if city_time.get("status") == "success":
        lines.append(f"🌍 {user_city} 现在是 {city_time.get('time_of_day', '')} {city_time.get('time_formatted', '')}")
    lines.append("")

    # 今日事件概览
    if not events:
        lines.append("📋 今日日程")
        lines.append("  没有安排会议，适合专注深度工作")
    else:
        lines.append(f"📋 今日日程 ({len(events)}项)")
        lines.append("")

        # 按时间排序
        sorted_events = sorted(events, key=lambda x: x.get("start", "00:00"))

        for i, event in enumerate(sorted_events, 1):
            title = event.get("title", "未命名事件")
            start = event.get("start", "")
            end = event.get("end", "")
            location = event.get("location", "")
            priority = event.get("priority", "normal")

            priority_mark = "🔴" if priority == "high" else ""
            location_mark = f" @ {location}" if location else ""

            lines.append(f"  {i}. {priority_mark}{start}-{end} {title}{location_mark}")

        lines.append("")

        # 计算统计
        total_minutes = 0
        for e in sorted_events:
            start = e.get("start", "09:00")
            end = e.get("end", "10:00")
            start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            end_min = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
            total_minutes += (end_min - start_min)

        hours = total_minutes // 60
        mins = total_minutes % 60
        free_hours = 8 - (total_minutes / 60)

        lines.append(f"⏱️ 会议时长: {hours}小时{mins}分钟")
        lines.append(f"🆓 空闲时间: {free_hours:.1f}小时")

        # 下一个会议
        now_minutes = today.hour * 60 + today.minute
        upcoming = None
        for e in sorted_events:
            start = e.get("start", "00:00")
            start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            if start_min > now_minutes:
                upcoming = e
                break

        if upcoming:
            lines.append("")
            lines.append(f"⏰ 下一个会议: {upcoming.get('title', '')} @ {upcoming.get('start', '')}")

    lines.append("")
    lines.append("=" * 50)
    lines.append("祝您今天工作顺利！")

    return "\n".join(lines)


def get_meeting_countdown(meeting: Dict) -> Dict:
    """
    获取会议倒计时

    Args:
        meeting: 会议信息

    Returns:
        倒计时信息
    """
    now = datetime.now()
    meeting_date = meeting.get("date", now.strftime("%Y-%m-%d"))
    meeting_time = meeting.get("start", "09:00")

    meeting_datetime = datetime.strptime(f"{meeting_date} {meeting_time}", "%Y-%m-%d %H:%M")

    if meeting_datetime < now:
        return {
            "status": "past",
            "message": "会议已开始或已结束"
        }

    diff = meeting_datetime - now
    total_minutes = diff.total_seconds() / 60

    if total_minutes < 60:
        countdown = f"{int(total_minutes)}分钟后"
        urgency = "🔴 即将开始"
    elif total_minutes < 120:
        countdown = f"1小时{int(total_minutes-60)}分钟后"
        urgency = "🟡 即将到来"
    elif total_minutes < 1440:  # 24小时
        hours = int(total_minutes // 60)
        mins = int(total_minutes % 60)
        countdown = f"{hours}小时{mins}分钟后"
        urgency = "🟢 今日"
    else:
        days = int(total_minutes // 1440)
        countdown = f"{days}天后"
        urgency = "📅 未来"

    return {
        "status": "success",
        "meeting": meeting.get("title", "会议"),
        "countdown": countdown,
        "urgency": urgency,
        "meeting_time": f"{meeting_date} {meeting_time}",
        "minutes_until": int(total_minutes)
    }
