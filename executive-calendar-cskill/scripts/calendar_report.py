"""
Calendar Report Module - 日历报告模块
生成日程报告、时间分析
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .calendar_manager import get_today_agenda, get_week_agenda, get_free_slots
from .meeting_scheduler import calculate_meeting_fatigue
from .timezone_manager import get_world_clock


def generate_daily_schedule(date: str = None) -> str:
    """
    生成每日日程表

    Args:
        date: 日期，默认今天

    Returns:
        格式化的日程表
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    agenda = get_today_agenda()
    events = agenda.get("events", [])
    fatigue = calculate_meeting_fatigue(events)

    lines = []
    lines.append("=" * 55)
    lines.append(f"📅 日程表 - {agenda.get('date_formatted', date)}")
    lines.append("=" * 55)
    lines.append("")

    # 日程概览
    lines.append(f"📊 今日概览")
    lines.append(f"  • 会议数量: {agenda.get('event_count', 0)}个")
    lines.append(f"  • 会议时长: {agenda.get('total_hours', 0)}小时")
    lines.append(f"  • 空闲时间: {agenda.get('free_time_hours', 8)}小时")
    lines.append(f"  • 疲劳指数: {fatigue.get('fatigue_level', '🟢 轻松')}")
    lines.append("")

    # 时间线
    lines.append("📋 时间线")
    lines.append("-" * 55)

    if not events:
        lines.append("  今天没有安排会议")
    else:
        for event in events:
            start = event.get("start", "")
            end = event.get("end", "")
            title = event.get("title", "")
            location = event.get("location", "")
            priority = event.get("priority", "normal")
            event_type = event.get("type", "general")

            # 图标
            if priority == "high":
                icon = "🔴"
            elif event_type == "external":
                icon = "🤝"
            elif event_type == "internal":
                icon = "👥"
            else:
                icon = "📌"

            # 格式化输出
            time_str = f"{start}-{end}"
            loc_str = f" ({location})" if location else ""
            lines.append(f"  {icon} {time_str:11} {title}{loc_str}")

    lines.append("-" * 55)
    lines.append("")

    # 空闲时段
    free = get_free_slots(date)
    free_slots = free.get("free_slots", [])

    if free_slots:
        lines.append("🆓 空闲时段")
        for slot in free_slots:
            quality = slot.get("quality", "")
            start = slot.get("start", "")
            end = slot.get("end", "")
            duration = slot.get("duration_minutes", 0)
            lines.append(f"  {quality} {start}-{end} ({duration}分钟)")
    else:
        lines.append("🆓 今日没有大块空闲时间")

    lines.append("")
    lines.append("=" * 55)

    return "\n".join(lines)


def generate_week_overview() -> str:
    """
    生成本周概览

    Returns:
        格式化的周概览
    """
    week = get_week_agenda()
    daily_stats = week.get("daily_breakdown", [])

    lines = []
    lines.append("=" * 60)
    lines.append(f"📅 本周概览 - {week.get('week_range', '')}")
    lines.append("=" * 60)
    lines.append("")

    # 周统计
    lines.append(f"📊 本周统计")
    lines.append(f"  • 总会议数: {week.get('total_events', 0)}个")
    lines.append(f"  • 最忙碌: {week.get('busiest_day', 'N/A')}")
    lines.append(f"  • 最轻松: {week.get('lightest_day', 'N/A')}")
    lines.append("")

    # 每日分布
    lines.append("📋 每日分布")
    lines.append("-" * 60)
    lines.append(f"{'日期':12} {'星期':6} {'会议':6} {'时长':8} {'忙碌度'}")
    lines.append("-" * 60)

    for day in daily_stats:
        date = day.get("date", "")
        weekday = day.get("weekday", "")
        count = day.get("event_count", 0)
        hours = day.get("meeting_hours", 0)
        busy = day.get("busy_level", "🟢")

        # 生成柱状图
        bar_length = min(int(hours * 2), 20)
        bar = "█" * bar_length + "░" * (10 - bar_length)

        lines.append(f"{date:12} {weekday:6} {count:4}个 {hours:5.1f}h  {busy} {bar}")

    lines.append("-" * 60)
    lines.append("")

    # 建议
    total_hours = sum(d.get("meeting_hours", 0) for d in daily_stats)
    avg_hours = total_hours / 7 if daily_stats else 0

    lines.append("💡 建议")
    if avg_hours > 5:
        lines.append("  ⚠️ 本周会议密度较高，建议适当减少会议")
    elif avg_hours > 3:
        lines.append("  🟡 会议负担适中，注意保留专注时间")
    else:
        lines.append("  🟢 会议节奏良好，有充足的专注时间")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_meeting_summary(events: List[Dict]) -> str:
    """
    生成会议总结

    Args:
        events: 事件列表

    Returns:
        会议总结
    """
    if not events:
        return "没有会议数据"

    lines = []
    lines.append("=" * 50)
    lines.append("📊 会议总结")
    lines.append("=" * 50)
    lines.append("")

    # 统计
    total = len(events)
    by_type = {}
    by_priority = {}
    total_minutes = 0

    for e in events:
        # 按类型统计
        etype = e.get("type", "general")
        by_type[etype] = by_type.get(etype, 0) + 1

        # 按优先级统计
        priority = e.get("priority", "normal")
        by_priority[priority] = by_priority.get(priority, 0) + 1

        # 计算时长
        start = e.get("start", "09:00")
        end = e.get("end", "10:00")
        start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
        end_min = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
        total_minutes += (end_min - start_min)

    # 基本统计
    lines.append(f"📌 总计: {total}个会议, {total_minutes//60}小时{total_minutes%60}分钟")
    lines.append("")

    # 按类型分布
    lines.append("📁 按类型分布")
    type_names = {"internal": "内部会议", "external": "外部会议", "personal": "个人事项", "general": "其他"}
    for t, count in by_type.items():
        name = type_names.get(t, t)
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines.append(f"  {name:8} {bar} {count}个 ({pct:.0f}%)")
    lines.append("")

    # 按优先级分布
    lines.append("🎯 按优先级分布")
    priority_names = {"high": "🔴 高", "normal": "🟡 中", "low": "🟢 低"}
    for p, count in sorted(by_priority.items(), key=lambda x: ["high", "normal", "low"].index(x[0]) if x[0] in ["high", "normal", "low"] else 3):
        name = priority_names.get(p, p)
        lines.append(f"  {name}: {count}个")
    lines.append("")

    lines.append("=" * 50)

    return "\n".join(lines)


def analyze_time_allocation(events: List[Dict], period_days: int = 7) -> Dict:
    """
    分析时间分配

    Args:
        events: 事件列表
        period_days: 分析周期天数

    Returns:
        时间分配分析
    """
    if not events:
        return {
            "status": "success",
            "message": "没有数据进行分析",
            "total_meetings": 0
        }

    # 计算总时间
    total_minutes = 0
    by_type = {}
    by_participant_type = {"solo": 0, "small": 0, "large": 0}

    for e in events:
        # 时长
        start = e.get("start", "09:00")
        end = e.get("end", "10:00")
        start_min = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
        end_min = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
        duration = end_min - start_min
        total_minutes += duration

        # 按类型
        etype = e.get("type", "general")
        by_type[etype] = by_type.get(etype, 0) + duration

        # 按参与人数
        participants = e.get("participants", [])
        if len(participants) <= 1:
            by_participant_type["solo"] += duration
        elif len(participants) <= 4:
            by_participant_type["small"] += duration
        else:
            by_participant_type["large"] += duration

    # 计算工作时间占比
    work_minutes_per_day = 8 * 60
    total_work_minutes = work_minutes_per_day * period_days
    meeting_percentage = (total_minutes / total_work_minutes * 100) if total_work_minutes else 0

    # 健康评估
    if meeting_percentage < 30:
        health = "🟢 健康"
        advice = "会议时间占比合理，有充足的专注时间"
    elif meeting_percentage < 50:
        health = "🟡 适中"
        advice = "会议时间略多，注意保护专注时间"
    else:
        health = "🔴 过重"
        advice = "会议时间过多，建议减少不必要的会议"

    return {
        "status": "success",
        "period_days": period_days,
        "total_meetings": len(events),
        "total_meeting_hours": round(total_minutes / 60, 1),
        "avg_meeting_hours_per_day": round(total_minutes / 60 / period_days, 1),
        "meeting_time_percentage": round(meeting_percentage, 1),
        "time_by_type": {
            k: round(v / 60, 1) for k, v in by_type.items()
        },
        "time_by_size": {
            "个人/1对1": round(by_participant_type["solo"] / 60, 1),
            "小型(2-4人)": round(by_participant_type["small"] / 60, 1),
            "大型(5人+)": round(by_participant_type["large"] / 60, 1)
        },
        "health_assessment": health,
        "advice": advice
    }


def generate_world_time_widget(cities: List[str] = None) -> str:
    """
    生成世界时钟小部件

    Args:
        cities: 城市列表

    Returns:
        格式化的世界时钟
    """
    return get_world_clock(cities)


def generate_executive_briefing() -> str:
    """
    生成高管每日简报

    Returns:
        格式化的高管简报
    """
    now = datetime.now()
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    lines = []
    lines.append("╔" + "═" * 58 + "╗")
    lines.append("║" + "🌅 高管每日简报".center(54) + "║")
    lines.append("║" + f"{now.strftime('%Y年%m月%d日')} {weekday_names[now.weekday()]}".center(56) + "║")
    lines.append("╚" + "═" * 58 + "╝")
    lines.append("")

    # 今日日程
    agenda = get_today_agenda()
    events = agenda.get("events", [])

    lines.append("┌─ 📅 今日日程 ────────────────────────────────────┐")
    if not events:
        lines.append("│  今天没有安排会议，适合专注深度工作                   │")
    else:
        lines.append(f"│  共{len(events)}个会议，{agenda.get('total_hours', 0):.1f}小时                                    │")
        for e in events[:5]:
            title = e.get("title", "")[:20]
            time_str = f"{e.get('start', '')}-{e.get('end', '')}"
            priority = "🔴" if e.get("priority") == "high" else "  "
            lines.append(f"│  {priority} {time_str:11} {title:22}  │")
        if len(events) > 5:
            lines.append(f"│  ... 还有{len(events)-5}个会议                                   │")
    lines.append("└─────────────────────────────────────────────────────┘")
    lines.append("")

    # 世界时钟
    lines.append("┌─ 🌍 主要城市时间 ────────────────────────────────┐")
    cities = ["北京", "东京", "新加坡", "伦敦", "纽约"]
    from .timezone_manager import get_city_time
    for city in cities:
        result = get_city_time(city)
        if result.get("status") == "success":
            emoji = result.get("emoji", "")
            time_str = result.get("time_formatted", "")
            weekday = result.get("weekday", "")
            biz = "🏢" if result.get("is_business_hours") else "🌙"
            lines.append(f"│  {emoji} {city:8} {time_str} {weekday} {biz}                    │")
    lines.append("└─────────────────────────────────────────────────────┘")
    lines.append("")

    # 疲劳度
    fatigue = calculate_meeting_fatigue(events)
    lines.append("┌─ 💪 今日状态 ────────────────────────────────────┐")
    lines.append(f"│  疲劳指数: {fatigue.get('fatigue_level', '🟢 轻松'):20}              │")
    lines.append(f"│  {fatigue.get('recommendation', ''):51} │"[:55] + "│")
    lines.append("└─────────────────────────────────────────────────────┘")

    return "\n".join(lines)
