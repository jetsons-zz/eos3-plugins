"""
Calendar Digest Module - 日历摘要模块
经济日历、财报日历、重要事件
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 经济日历数据
ECONOMIC_CALENDAR = [
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "09:30",
        "country": "中国",
        "event": "官方制造业PMI",
        "importance": "high",
        "previous": "50.1",
        "forecast": "50.3",
        "impact": "利好/利空人民币及A股"
    },
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "21:30",
        "country": "美国",
        "event": "非农就业数据",
        "importance": "high",
        "previous": "150K",
        "forecast": "180K",
        "impact": "影响美联储利率决策"
    },
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "17:00",
        "country": "欧元区",
        "event": "CPI (同比)",
        "importance": "medium",
        "previous": "2.3%",
        "forecast": "2.4%",
        "impact": "影响欧央行政策"
    },
    {
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "03:00",
        "country": "美国",
        "event": "FOMC会议纪要",
        "importance": "high",
        "previous": "-",
        "forecast": "-",
        "impact": "关注利率路径指引"
    }
]

# 财报日历
EARNINGS_CALENDAR = [
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "company": "苹果",
        "symbol": "AAPL",
        "timing": "盘后",
        "expected_eps": "$2.35",
        "expected_revenue": "$124B"
    },
    {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "company": "微软",
        "symbol": "MSFT",
        "timing": "盘后",
        "expected_eps": "$3.10",
        "expected_revenue": "$68B"
    },
    {
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "company": "亚马逊",
        "symbol": "AMZN",
        "timing": "盘后",
        "expected_eps": "$1.45",
        "expected_revenue": "$187B"
    },
    {
        "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "company": "英伟达",
        "symbol": "NVDA",
        "timing": "盘后",
        "expected_eps": "$0.75",
        "expected_revenue": "$38B"
    }
]

# 市场交易时间
MARKET_HOURS = {
    "中国A股": {
        "open": "09:30",
        "close": "15:00",
        "timezone": "CST",
        "lunch_break": "11:30-13:00",
        "trading_days": "周一至周五"
    },
    "港股": {
        "open": "09:30",
        "close": "16:00",
        "timezone": "HKT",
        "lunch_break": "12:00-13:00",
        "trading_days": "周一至周五"
    },
    "美股": {
        "open": "09:30",
        "close": "16:00",
        "timezone": "EST",
        "lunch_break": "无",
        "trading_days": "周一至周五",
        "pre_market": "04:00-09:30",
        "after_hours": "16:00-20:00"
    },
    "日本股市": {
        "open": "09:00",
        "close": "15:00",
        "timezone": "JST",
        "lunch_break": "11:30-12:30",
        "trading_days": "周一至周五"
    },
    "欧洲股市": {
        "open": "08:00",
        "close": "16:30",
        "timezone": "CET",
        "lunch_break": "无",
        "trading_days": "周一至周五"
    },
    "加密货币": {
        "open": "00:00",
        "close": "24:00",
        "timezone": "UTC",
        "lunch_break": "无",
        "trading_days": "全年无休"
    }
}


def get_economic_calendar(days: int = 7) -> Dict:
    """
    获取经济日历

    Args:
        days: 查看未来天数

    Returns:
        经济日历数据
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=days)

    events = []
    for event in ECONOMIC_CALENDAR:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        if today <= event_date <= end_date:
            importance = event.get("importance", "low")
            emoji = "🔴" if importance == "high" else "🟡" if importance == "medium" else "🟢"
            events.append({
                **event,
                "emoji": emoji
            })

    # 按日期和时间排序
    events = sorted(events, key=lambda x: (x["date"], x["time"]))

    # 按日期分组
    by_date = {}
    for event in events:
        date = event["date"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(event)

    return {
        "status": "success",
        "date_range": f"{today} 至 {end_date}",
        "total_events": len(events),
        "high_importance": len([e for e in events if e.get("importance") == "high"]),
        "events_by_date": by_date,
        "events": events,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_earnings_calendar(days: int = 7, symbols: List[str] = None) -> Dict:
    """
    获取财报日历

    Args:
        days: 查看未来天数
        symbols: 关注的股票代码列表

    Returns:
        财报日历数据
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=days)

    earnings = []
    for report in EARNINGS_CALENDAR:
        report_date = datetime.strptime(report["date"], "%Y-%m-%d").date()
        if today <= report_date <= end_date:
            if symbols is None or report["symbol"] in symbols:
                earnings.append(report)

    # 按日期排序
    earnings = sorted(earnings, key=lambda x: x["date"])

    # 今日财报
    today_str = today.strftime("%Y-%m-%d")
    today_earnings = [e for e in earnings if e["date"] == today_str]

    return {
        "status": "success",
        "date_range": f"{today} 至 {end_date}",
        "total_reports": len(earnings),
        "today_reports": len(today_earnings),
        "today_earnings": today_earnings,
        "earnings": earnings,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_personal_highlights(events: List[Dict] = None, portfolio_symbols: List[str] = None) -> Dict:
    """
    获取个人关注的重要事件

    Args:
        events: 个人日程事件
        portfolio_symbols: 持仓股票代码

    Returns:
        个人重要事件
    """
    highlights = []

    # 检查持仓股票的财报
    if portfolio_symbols:
        earnings = get_earnings_calendar(days=7, symbols=portfolio_symbols)
        for report in earnings.get("earnings", []):
            highlights.append({
                "type": "earnings",
                "date": report["date"],
                "title": f"{report['company']} 财报发布",
                "detail": f"预期 EPS: {report['expected_eps']}",
                "importance": "high"
            })

    # 添加重要经济数据
    econ = get_economic_calendar(days=3)
    for event in econ.get("events", []):
        if event.get("importance") == "high":
            highlights.append({
                "type": "economic",
                "date": event["date"],
                "time": event["time"],
                "title": f"{event['country']} {event['event']}",
                "detail": f"预期: {event.get('forecast', 'N/A')}",
                "importance": "high"
            })

    # 按日期排序
    highlights = sorted(highlights, key=lambda x: x.get("date", ""))

    return {
        "status": "success",
        "highlight_count": len(highlights),
        "highlights": highlights,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_market_hours(market: str = None) -> Dict:
    """
    获取市场交易时间

    Args:
        market: 市场名称，None返回所有

    Returns:
        交易时间信息
    """
    if market:
        # 模糊匹配
        for key, value in MARKET_HOURS.items():
            if market.lower() in key.lower() or key.lower() in market.lower():
                return {
                    "status": "success",
                    "market": key,
                    "hours": value
                }

        return {
            "status": "not_found",
            "message": f"未找到 {market} 的交易时间",
            "available_markets": list(MARKET_HOURS.keys())
        }

    return {
        "status": "success",
        "markets": MARKET_HOURS
    }


def is_market_open(market: str) -> Dict:
    """
    检查市场是否开盘

    Args:
        market: 市场名称

    Returns:
        开盘状态
    """
    hours = get_market_hours(market)

    if hours.get("status") != "success":
        return hours

    market_info = hours.get("hours", {})
    open_time = market_info.get("open", "09:00")
    close_time = market_info.get("close", "16:00")
    lunch = market_info.get("lunch_break", "")

    # 简化判断（不考虑时区转换）
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    weekday = now.weekday()

    # 周末判断
    if weekday >= 5 and market != "加密货币":
        return {
            "status": "success",
            "market": market,
            "is_open": False,
            "reason": "周末休市",
            "next_open": "下周一"
        }

    # 交易时间判断
    if open_time <= current_time <= close_time:
        # 检查午休
        if lunch and "-" in lunch:
            lunch_start, lunch_end = lunch.split("-")
            if lunch_start <= current_time <= lunch_end:
                return {
                    "status": "success",
                    "market": market,
                    "is_open": False,
                    "reason": "午休时间",
                    "resume_at": lunch_end
                }

        return {
            "status": "success",
            "market": market,
            "is_open": True,
            "close_at": close_time
        }
    else:
        return {
            "status": "success",
            "market": market,
            "is_open": False,
            "reason": "非交易时间",
            "next_open": f"明日 {open_time}" if current_time > close_time else f"今日 {open_time}"
        }
