"""
Briefing Generator Module - 简报生成模块
生成个性化财富简报
"""

from datetime import datetime
from typing import Dict, List, Optional
from .market_pulse import get_market_overview
from .portfolio_snapshot import get_portfolio_summary, get_alerts
from .news_curator import get_top_headlines, curate_for_interests
from .calendar_digest import get_economic_calendar, get_earnings_calendar, get_personal_highlights


def generate_morning_brief(
    portfolio: Dict = None,
    interests: List[str] = None,
    user_name: str = "您"
) -> str:
    """
    生成早间简报

    Args:
        portfolio: 投资组合数据
        interests: 兴趣标签
        user_name: 用户名称

    Returns:
        格式化的早间简报
    """
    if interests is None:
        interests = ["AI", "科技", "加密货币"]

    now = datetime.now()
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    lines = []

    # 标题
    lines.append("╔" + "═" * 60 + "╗")
    lines.append("║" + f"☀️ 早安, {user_name}".center(56) + "║")
    lines.append("║" + f"{now.strftime('%Y年%m月%d日')} {weekday_names[now.weekday()]}".center(58) + "║")
    lines.append("╚" + "═" * 60 + "╝")
    lines.append("")

    # 市场概览
    market = get_market_overview()
    lines.append("┌─ 🌍 全球市场概览 ────────────────────────────────────┐")

    sentiment = market.get("market_sentiment", "")
    lines.append(f"│  市场情绪: {sentiment:50} │")
    lines.append("│                                                          │")

    # 指数
    for idx in market.get("indices", [])[:4]:
        name = idx.get("name", "")[:8]
        price = idx.get("price", 0)
        change = idx.get("change_percent", 0)
        emoji = idx.get("emoji", "")
        lines.append(f"│  {emoji} {name:8} {price:>10,.2f}  ({change:+.2f}%)            │")

    lines.append("│                                                          │")

    # 加密货币
    for crypto in market.get("crypto", [])[:2]:
        name = crypto.get("name", "")[:8]
        price = crypto.get("price", 0)
        change = crypto.get("change_percent", 0)
        emoji = crypto.get("emoji", "")
        lines.append(f"│  {emoji} {name:8} ${price:>10,.2f}  ({change:+.2f}%)           │")

    lines.append("└──────────────────────────────────────────────────────────┘")
    lines.append("")

    # 投资组合
    portfolio_data = get_portfolio_summary(portfolio)
    summary = portfolio_data.get("summary", {})

    lines.append("┌─ 💰 投资组合 ──────────────────────────────────────────┐")
    total_value = summary.get("total_value", 0)
    total_gain = summary.get("total_gain", 0)
    total_gain_pct = summary.get("total_gain_percent", 0)
    status_emoji = summary.get("status_emoji", "")

    lines.append(f"│  总资产: ${total_value:,.2f}                              │"[:62] + "│")
    lines.append(f"│  {status_emoji} 总盈亏: ${total_gain:+,.2f} ({total_gain_pct:+.2f}%)               │"[:62] + "│")

    # 表现最佳
    top_gainers = portfolio_data.get("top_gainers", [])
    if top_gainers:
        best = top_gainers[0]
        lines.append(f"│  📈 最佳: {best.get('name', '')} ({best.get('gain_percent', 0):+.1f}%)                        │"[:62] + "│")

    # 警报
    alerts = get_alerts(portfolio)
    if alerts.get("has_critical"):
        lines.append(f"│  ⚠️  有{alerts.get('alert_count', 0)}条警报需要关注                              │"[:62] + "│")

    lines.append("└──────────────────────────────────────────────────────────┘")
    lines.append("")

    # 今日要闻
    headlines = get_top_headlines(3)
    lines.append("┌─ 📰 今日要闻 ──────────────────────────────────────────┐")

    for news in headlines.get("headlines", [])[:3]:
        importance = news.get("importance", "low")
        emoji = "🔴" if importance == "high" else "🟡"
        title = news.get("title", "")[:45]
        lines.append(f"│  {emoji} {title:50} │")

    lines.append("└──────────────────────────────────────────────────────────┘")
    lines.append("")

    # 今日日程
    econ = get_economic_calendar(days=1)
    earnings = get_earnings_calendar(days=1)

    lines.append("┌─ 📅 今日重要事件 ────────────────────────────────────┐")

    today_econ = [e for e in econ.get("events", []) if e.get("importance") == "high"]
    for event in today_econ[:2]:
        time = event.get("time", "")
        title = f"{event.get('country', '')} {event.get('event', '')}"[:40]
        lines.append(f"│  🕐 {time} {title:45} │")

    today_earnings = earnings.get("today_earnings", [])
    for report in today_earnings[:2]:
        company = report.get("company", "")
        timing = report.get("timing", "")
        lines.append(f"│  📊 {company} 财报 ({timing})                              │"[:62] + "│")

    if not today_econ and not today_earnings:
        lines.append("│  今日无重大事件                                           │")

    lines.append("└──────────────────────────────────────────────────────────┘")
    lines.append("")

    # 底部
    lines.append("─" * 62)
    lines.append(f"简报生成于 {now.strftime('%H:%M')} | 祝您投资顺利!")

    return "\n".join(lines)


def generate_quick_brief() -> str:
    """
    生成快速简报（一句话版本）

    Returns:
        一句话简报
    """
    market = get_market_overview()
    portfolio = get_portfolio_summary()

    sentiment = market.get("market_sentiment", "")

    # 找出涨跌最多的指数
    indices = market.get("indices", [])
    if indices:
        best_idx = max(indices, key=lambda x: x.get("change_percent", 0))
        worst_idx = min(indices, key=lambda x: x.get("change_percent", 0))
    else:
        best_idx = {"name": "N/A", "change_percent": 0}
        worst_idx = {"name": "N/A", "change_percent": 0}

    summary = portfolio.get("summary", {})
    total_gain_pct = summary.get("total_gain_percent", 0)
    status_emoji = summary.get("status_emoji", "")

    return (
        f"{sentiment} | "
        f"📈{best_idx['name']}+{best_idx['change_percent']:.1f}% "
        f"📉{worst_idx['name']}{worst_idx['change_percent']:.1f}% | "
        f"{status_emoji}组合{total_gain_pct:+.1f}%"
    )


def generate_market_alert(alert_type: str, data: Dict) -> str:
    """
    生成市场警报

    Args:
        alert_type: 警报类型 (price_move/news/earnings)
        data: 警报数据

    Returns:
        格式化的警报
    """
    now = datetime.now().strftime("%H:%M")

    if alert_type == "price_move":
        symbol = data.get("symbol", "")
        name = data.get("name", symbol)
        change_pct = data.get("change_percent", 0)
        direction = "上涨" if change_pct > 0 else "下跌"
        emoji = "🚀" if change_pct > 5 else "📈" if change_pct > 0 else "📉" if change_pct > -5 else "💥"

        return f"⏰ {now} | {emoji} {name} {direction} {abs(change_pct):.1f}%"

    elif alert_type == "news":
        title = data.get("title", "")[:50]
        importance = data.get("importance", "medium")
        emoji = "🔴" if importance == "high" else "🟡"

        return f"⏰ {now} | {emoji} 快讯: {title}"

    elif alert_type == "earnings":
        company = data.get("company", "")
        result = data.get("result", "")  # beat/miss/meet
        emoji = "🎉" if result == "beat" else "😔" if result == "miss" else "📊"

        return f"⏰ {now} | {emoji} {company} 财报发布: {result}"

    return f"⏰ {now} | 未知警报类型"


def generate_weekly_review(portfolio: Dict = None) -> str:
    """
    生成周度回顾

    Args:
        portfolio: 投资组合

    Returns:
        格式化的周度回顾
    """
    now = datetime.now()

    lines = []
    lines.append("=" * 60)
    lines.append(f"📊 周度财富回顾")
    lines.append(f"截至 {now.strftime('%Y年%m月%d日')}")
    lines.append("=" * 60)
    lines.append("")

    # 市场回顾
    market = get_market_overview()
    lines.append("## 🌍 本周市场表现")
    lines.append("")

    for idx in market.get("indices", []):
        name = idx.get("name", "")
        change = idx.get("change_percent", 0)
        emoji = idx.get("emoji", "")
        lines.append(f"{emoji} {name}: {change:+.2f}%")

    lines.append("")

    # 组合回顾
    portfolio_data = get_portfolio_summary(portfolio)
    summary = portfolio_data.get("summary", {})

    lines.append("## 💰 投资组合表现")
    lines.append("")
    lines.append(f"总资产: ${summary.get('total_value', 0):,.2f}")
    lines.append(f"本周盈亏: ${summary.get('total_gain', 0):+,.2f} ({summary.get('total_gain_percent', 0):+.2f}%)")
    lines.append("")

    # 表现最佳/最差
    top = portfolio_data.get("top_gainers", [])
    if top:
        lines.append("📈 表现最佳:")
        for p in top[:3]:
            lines.append(f"  • {p.get('name', '')}: {p.get('gain_percent', 0):+.1f}%")

    bottom = portfolio_data.get("top_losers", [])
    if bottom:
        lines.append("📉 表现最差:")
        for p in bottom[:3]:
            lines.append(f"  • {p.get('name', '')}: {p.get('gain_percent', 0):+.1f}%")

    lines.append("")

    # 下周展望
    lines.append("## 📅 下周关注")
    econ = get_economic_calendar(days=7)
    high_impact = [e for e in econ.get("events", []) if e.get("importance") == "high"]

    for event in high_impact[:5]:
        lines.append(f"• {event.get('date', '')} {event.get('country', '')} {event.get('event', '')}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
