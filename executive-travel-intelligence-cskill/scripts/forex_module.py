"""
Forex Module - 汇率模块
使用 yfinance 获取汇率数据
"""

from datetime import datetime
from typing import Dict, List, Optional

try:
    import yfinance as yf
except ImportError:
    yf = None

# 货币信息
CURRENCY_INFO = {
    "CNY": {"name": "人民币", "symbol": "¥", "locale": "中国"},
    "USD": {"name": "美元", "symbol": "$", "locale": "美国"},
    "EUR": {"name": "欧元", "symbol": "€", "locale": "欧元区"},
    "GBP": {"name": "英镑", "symbol": "£", "locale": "英国"},
    "JPY": {"name": "日元", "symbol": "¥", "locale": "日本"},
    "HKD": {"name": "港币", "symbol": "HK$", "locale": "香港"},
    "SGD": {"name": "新加坡元", "symbol": "S$", "locale": "新加坡"},
    "KRW": {"name": "韩元", "symbol": "₩", "locale": "韩国"},
    "AUD": {"name": "澳元", "symbol": "A$", "locale": "澳大利亚"},
    "CAD": {"name": "加元", "symbol": "C$", "locale": "加拿大"},
    "CHF": {"name": "瑞士法郎", "symbol": "CHF", "locale": "瑞士"},
    "AED": {"name": "迪拉姆", "symbol": "د.إ", "locale": "阿联酋"},
}

# 日均消费参考 (USD)
DAILY_COST_REFERENCE = {
    "东京": {"budget": 150, "mid": 300, "luxury": 600},
    "北京": {"budget": 80, "mid": 150, "luxury": 350},
    "上海": {"budget": 90, "mid": 180, "luxury": 400},
    "香港": {"budget": 120, "mid": 250, "luxury": 500},
    "新加坡": {"budget": 130, "mid": 280, "luxury": 550},
    "首尔": {"budget": 100, "mid": 200, "luxury": 450},
    "伦敦": {"budget": 180, "mid": 350, "luxury": 700},
    "巴黎": {"budget": 160, "mid": 320, "luxury": 650},
    "纽约": {"budget": 200, "mid": 400, "luxury": 800},
    "洛杉矶": {"budget": 150, "mid": 300, "luxury": 600},
    "悉尼": {"budget": 140, "mid": 280, "luxury": 550},
    "迪拜": {"budget": 150, "mid": 350, "luxury": 800},
}


def get_exchange_rate(from_currency: str, to_currency: str) -> Dict:
    """
    获取汇率

    Args:
        from_currency: 源货币代码
        to_currency: 目标货币代码

    Returns:
        汇率信息
    """
    if yf is None:
        return {"error": "yfinance not installed"}

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return {
            "from": from_currency,
            "to": to_currency,
            "rate": 1.0,
            "inverse_rate": 1.0
        }

    try:
        # 尝试直接获取汇率对
        symbol = f"{from_currency}{to_currency}=X"
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")

        if hist.empty:
            # 尝试通过 USD 中转
            if from_currency != "USD" and to_currency != "USD":
                from_usd = get_exchange_rate(from_currency, "USD")
                usd_to = get_exchange_rate("USD", to_currency)
                if "error" not in from_usd and "error" not in usd_to:
                    rate = from_usd["rate"] * usd_to["rate"]
                    return {
                        "from": from_currency,
                        "to": to_currency,
                        "rate": round(rate, 4),
                        "inverse_rate": round(1/rate, 4),
                        "from_info": CURRENCY_INFO.get(from_currency, {}),
                        "to_info": CURRENCY_INFO.get(to_currency, {})
                    }
            return {"error": f"无法获取 {from_currency}/{to_currency} 汇率"}

        rate = hist["Close"].iloc[-1]
        prev_rate = hist["Close"].iloc[-2] if len(hist) > 1 else rate
        change = rate - prev_rate
        change_pct = (change / prev_rate * 100) if prev_rate else 0

        return {
            "from": from_currency,
            "to": to_currency,
            "rate": round(rate, 4),
            "inverse_rate": round(1/rate, 6),
            "change": round(change, 4),
            "change_percent": round(change_pct, 2),
            "from_info": CURRENCY_INFO.get(from_currency, {}),
            "to_info": CURRENCY_INFO.get(to_currency, {}),
            "updated_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {"error": str(e)}


def get_budget_estimate(
    city: str,
    days: int,
    level: str = "mid",
    home_currency: str = "CNY"
) -> Dict:
    """
    估算出行预算

    Args:
        city: 目的地城市
        days: 出行天数
        level: 消费水平 (budget/mid/luxury)
        home_currency: 本国货币

    Returns:
        预算估算
    """
    # 获取城市消费参考
    costs = DAILY_COST_REFERENCE.get(city)
    if not costs:
        # 使用默认值
        costs = {"budget": 120, "mid": 250, "luxury": 500}

    daily_usd = costs.get(level, costs["mid"])
    total_usd = daily_usd * days

    # 获取汇率
    rate_info = get_exchange_rate("USD", home_currency)
    if "error" in rate_info:
        rate = 7.0 if home_currency == "CNY" else 1.0
    else:
        rate = rate_info["rate"]

    daily_local = daily_usd * rate
    total_local = total_usd * rate

    currency_info = CURRENCY_INFO.get(home_currency, {"symbol": home_currency})

    return {
        "city": city,
        "days": days,
        "level": level,
        "level_cn": {"budget": "经济", "mid": "舒适", "luxury": "豪华"}.get(level, "舒适"),
        "daily_budget": {
            "usd": daily_usd,
            "local": round(daily_local, 0),
            "local_currency": home_currency,
            "formatted": f"{currency_info.get('symbol', '')}{round(daily_local):,}"
        },
        "total_budget": {
            "usd": total_usd,
            "local": round(total_local, 0),
            "local_currency": home_currency,
            "formatted": f"{currency_info.get('symbol', '')}{round(total_local):,}"
        },
        "exchange_rate": rate,
        "tips": _get_budget_tips(city, level)
    }


def _get_budget_tips(city: str, level: str) -> List[str]:
    """获取预算建议"""
    tips = []

    if level == "budget":
        tips.append("选择地铁/公交出行")
        tips.append("提前预订住宿获取优惠")
    elif level == "luxury":
        tips.append("考虑包车服务提高效率")
        tips.append("高端酒店通常含早餐")

    # 城市特定建议
    city_tips = {
        "东京": "建议购买交通一日券",
        "伦敦": "使用 Oyster 卡乘坐地铁更划算",
        "纽约": "提前购买景点通票可省钱",
        "新加坡": "办理 EZ-Link 卡方便出行",
        "香港": "八达通卡必备",
    }

    if city in city_tips:
        tips.append(city_tips[city])

    return tips


def format_currency(amount: float, currency: str) -> str:
    """格式化货币显示"""
    info = CURRENCY_INFO.get(currency, {"symbol": currency})
    symbol = info.get("symbol", currency)

    if currency in ["JPY", "KRW"]:
        return f"{symbol}{int(amount):,}"
    else:
        return f"{symbol}{amount:,.2f}"
