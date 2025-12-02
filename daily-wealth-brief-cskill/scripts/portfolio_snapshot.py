"""
Portfolio Snapshot Module - 投资组合快照模块
投资组合每日表现快照
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


# 示例投资组合
SAMPLE_PORTFOLIO = {
    "name": "高管投资组合",
    "holdings": [
        {"symbol": "AAPL", "name": "苹果", "shares": 100, "cost_basis": 150.00},
        {"symbol": "MSFT", "name": "微软", "shares": 50, "cost_basis": 320.00},
        {"symbol": "GOOGL", "name": "谷歌", "shares": 30, "cost_basis": 140.00},
        {"symbol": "NVDA", "name": "英伟达", "shares": 40, "cost_basis": 400.00},
        {"symbol": "BTC-USD", "name": "比特币", "shares": 0.5, "cost_basis": 45000.00},
        {"symbol": "ETH-USD", "name": "以太坊", "shares": 5, "cost_basis": 2500.00},
        {"symbol": "GC=F", "name": "黄金", "shares": 2, "cost_basis": 1900.00}
    ]
}


def get_portfolio_summary(portfolio: Dict = None) -> Dict:
    """
    获取投资组合摘要

    Args:
        portfolio: 投资组合数据，默认使用示例

    Returns:
        投资组合摘要
    """
    if portfolio is None:
        portfolio = SAMPLE_PORTFOLIO

    holdings = portfolio.get("holdings", [])
    total_value = 0
    total_cost = 0
    positions = []

    for holding in holdings:
        symbol = holding.get("symbol", "")
        name = holding.get("name", symbol)
        shares = holding.get("shares", 0)
        cost_basis = holding.get("cost_basis", 0)

        # 获取当前价格
        if HAS_YFINANCE:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                current_price = info.get("regularMarketPrice") or info.get("previousClose", cost_basis)
            except:
                current_price = cost_basis
        else:
            current_price = cost_basis * 1.1  # 模拟10%涨幅

        position_value = current_price * shares
        position_cost = cost_basis * shares
        position_gain = position_value - position_cost
        position_gain_pct = (position_gain / position_cost * 100) if position_cost else 0

        total_value += position_value
        total_cost += position_cost

        positions.append({
            "symbol": symbol,
            "name": name,
            "shares": shares,
            "current_price": round(current_price, 2),
            "cost_basis": cost_basis,
            "value": round(position_value, 2),
            "gain": round(position_gain, 2),
            "gain_percent": round(position_gain_pct, 2),
            "weight": 0  # 稍后计算
        })

    # 计算权重
    for pos in positions:
        pos["weight"] = round(pos["value"] / total_value * 100, 1) if total_value else 0

    total_gain = total_value - total_cost
    total_gain_pct = (total_gain / total_cost * 100) if total_cost else 0

    # 排序：按价值降序
    positions = sorted(positions, key=lambda x: x["value"], reverse=True)

    # 确定整体状态
    if total_gain_pct > 5:
        status_emoji = "📈"
        status_text = "表现优异"
    elif total_gain_pct > 0:
        status_emoji = "🟢"
        status_text = "盈利中"
    elif total_gain_pct > -5:
        status_emoji = "🟡"
        status_text = "小幅亏损"
    else:
        status_emoji = "🔴"
        status_text = "需要关注"

    return {
        "status": "success",
        "portfolio_name": portfolio.get("name", "我的投资组合"),
        "summary": {
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain": round(total_gain, 2),
            "total_gain_percent": round(total_gain_pct, 2),
            "position_count": len(positions),
            "status_emoji": status_emoji,
            "status_text": status_text
        },
        "positions": positions,
        "top_gainers": [p for p in positions if p["gain_percent"] > 0][:3],
        "top_losers": [p for p in positions if p["gain_percent"] < 0][:3],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_holdings_performance(portfolio: Dict = None, period: str = "1d") -> Dict:
    """
    获取持仓表现

    Args:
        portfolio: 投资组合
        period: 时间周期 (1d/1w/1m/ytd)

    Returns:
        持仓表现数据
    """
    if portfolio is None:
        portfolio = SAMPLE_PORTFOLIO

    holdings = portfolio.get("holdings", [])
    performances = []

    period_names = {
        "1d": "今日",
        "1w": "本周",
        "1m": "本月",
        "ytd": "今年"
    }

    for holding in holdings:
        symbol = holding.get("symbol", "")
        name = holding.get("name", symbol)

        # 获取历史数据计算涨跌
        if HAS_YFINANCE:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period if period != "ytd" else "1y")
                if len(hist) >= 2:
                    if period == "ytd":
                        # 年初至今
                        year_start = hist[hist.index.year == datetime.now().year].iloc[0]["Close"]
                        current = hist.iloc[-1]["Close"]
                    else:
                        year_start = hist.iloc[0]["Close"]
                        current = hist.iloc[-1]["Close"]
                    change_pct = (current - year_start) / year_start * 100
                else:
                    change_pct = 0
            except:
                change_pct = 0
        else:
            # 模拟数据
            import random
            change_pct = random.uniform(-5, 10)

        direction = "up" if change_pct > 0 else "down" if change_pct < 0 else "flat"
        emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"

        performances.append({
            "symbol": symbol,
            "name": name,
            "change_percent": round(change_pct, 2),
            "direction": direction,
            "emoji": emoji
        })

    # 排序
    performances = sorted(performances, key=lambda x: x["change_percent"], reverse=True)

    return {
        "status": "success",
        "period": period,
        "period_name": period_names.get(period, period),
        "performances": performances,
        "best_performer": performances[0] if performances else None,
        "worst_performer": performances[-1] if performances else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_alerts(portfolio: Dict = None) -> Dict:
    """
    获取投资组合警报

    Args:
        portfolio: 投资组合

    Returns:
        警报列表
    """
    if portfolio is None:
        portfolio = SAMPLE_PORTFOLIO

    summary = get_portfolio_summary(portfolio)
    positions = summary.get("positions", [])

    alerts = []

    for pos in positions:
        symbol = pos.get("symbol", "")
        name = pos.get("name", symbol)
        gain_pct = pos.get("gain_percent", 0)
        weight = pos.get("weight", 0)

        # 大幅亏损警报
        if gain_pct < -10:
            alerts.append({
                "type": "loss",
                "severity": "high",
                "symbol": symbol,
                "name": name,
                "message": f"🔴 {name} 亏损 {abs(gain_pct):.1f}%，建议评估是否止损"
            })
        elif gain_pct < -5:
            alerts.append({
                "type": "loss",
                "severity": "medium",
                "symbol": symbol,
                "name": name,
                "message": f"🟡 {name} 亏损 {abs(gain_pct):.1f}%，建议关注"
            })

        # 大幅盈利提醒
        if gain_pct > 50:
            alerts.append({
                "type": "profit",
                "severity": "info",
                "symbol": symbol,
                "name": name,
                "message": f"📈 {name} 盈利 {gain_pct:.1f}%，可考虑部分止盈"
            })

        # 集中度警报
        if weight > 30:
            alerts.append({
                "type": "concentration",
                "severity": "medium",
                "symbol": symbol,
                "name": name,
                "message": f"⚠️ {name} 占比 {weight:.1f}%，集中度较高"
            })

    # 按严重程度排序
    severity_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    alerts = sorted(alerts, key=lambda x: severity_order.get(x.get("severity", "info"), 3))

    return {
        "status": "success",
        "alert_count": len(alerts),
        "has_critical": any(a.get("severity") == "high" for a in alerts),
        "alerts": alerts,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_dividend_calendar(portfolio: Dict = None, days_ahead: int = 30) -> Dict:
    """
    获取分红日历

    Args:
        portfolio: 投资组合
        days_ahead: 查看未来天数

    Returns:
        分红日历
    """
    if portfolio is None:
        portfolio = SAMPLE_PORTFOLIO

    holdings = portfolio.get("holdings", [])
    dividends = []

    for holding in holdings:
        symbol = holding.get("symbol", "")
        name = holding.get("name", symbol)
        shares = holding.get("shares", 0)

        # 获取分红信息
        if HAS_YFINANCE:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info

                div_yield = info.get("dividendYield", 0)
                div_rate = info.get("dividendRate", 0)

                if div_rate and div_rate > 0:
                    annual_div = div_rate * shares
                    dividends.append({
                        "symbol": symbol,
                        "name": name,
                        "dividend_yield": f"{div_yield*100:.2f}%" if div_yield else "N/A",
                        "annual_dividend": round(annual_div, 2),
                        "next_date": "待公布"  # 实际需要获取具体日期
                    })
            except:
                pass

    total_annual = sum(d.get("annual_dividend", 0) for d in dividends)

    return {
        "status": "success",
        "dividend_stocks": len(dividends),
        "total_annual_dividend": round(total_annual, 2),
        "dividends": dividends,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
