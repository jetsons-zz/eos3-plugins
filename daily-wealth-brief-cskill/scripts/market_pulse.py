"""
Market Pulse Module - 市场脉搏模块
实时市场数据概览
"""

from datetime import datetime
from typing import Dict, List, Optional

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


# 主要市场指数
INDICES = {
    "上证指数": "000001.SS",
    "深证成指": "399001.SZ",
    "恒生指数": "^HSI",
    "日经225": "^N225",
    "标普500": "^GSPC",
    "纳斯达克": "^IXIC",
    "道琼斯": "^DJI",
    "富时100": "^FTSE",
    "DAX": "^GDAXI"
}

# 加密货币
CRYPTOS = {
    "比特币": "BTC-USD",
    "以太坊": "ETH-USD",
    "BNB": "BNB-USD",
    "Solana": "SOL-USD",
    "XRP": "XRP-USD"
}

# 大宗商品
COMMODITIES = {
    "黄金": "GC=F",
    "白银": "SI=F",
    "原油WTI": "CL=F",
    "布伦特原油": "BZ=F",
    "天然气": "NG=F",
    "铜": "HG=F"
}

# 主要货币对
FOREX = {
    "美元/人民币": "USDCNY=X",
    "欧元/美元": "EURUSD=X",
    "美元/日元": "USDJPY=X",
    "英镑/美元": "GBPUSD=X",
    "美元指数": "DX-Y.NYB"
}


def get_quote(symbol: str) -> Dict:
    """获取单个标的报价"""
    if not HAS_YFINANCE:
        return {"status": "error", "message": "需要安装 yfinance"}

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        price = info.get("regularMarketPrice") or info.get("previousClose", 0)
        prev_close = info.get("previousClose", price)
        change = price - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0

        return {
            "status": "success",
            "price": price,
            "change": change,
            "change_percent": change_pct,
            "direction": "up" if change > 0 else "down" if change < 0 else "flat"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_market_overview() -> Dict:
    """
    获取市场全景

    Returns:
        市场全景数据
    """
    overview = {
        "status": "success",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "indices": [],
        "crypto": [],
        "commodities": [],
        "forex": [],
        "market_sentiment": ""
    }

    if not HAS_YFINANCE:
        overview["status"] = "limited"
        overview["message"] = "需要安装 yfinance 获取实时数据"
        return overview

    # 获取指数数据
    up_count = 0
    down_count = 0

    for name, symbol in list(INDICES.items())[:5]:  # 只取前5个主要指数
        quote = get_quote(symbol)
        if quote.get("status") == "success":
            direction = quote.get("direction", "flat")
            emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"

            if direction == "up":
                up_count += 1
            elif direction == "down":
                down_count += 1

            overview["indices"].append({
                "name": name,
                "price": quote.get("price", 0),
                "change_percent": round(quote.get("change_percent", 0), 2),
                "direction": direction,
                "emoji": emoji
            })

    # 获取加密货币（只取前3个）
    for name, symbol in list(CRYPTOS.items())[:3]:
        quote = get_quote(symbol)
        if quote.get("status") == "success":
            direction = quote.get("direction", "flat")
            emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"
            overview["crypto"].append({
                "name": name,
                "price": quote.get("price", 0),
                "change_percent": round(quote.get("change_percent", 0), 2),
                "direction": direction,
                "emoji": emoji
            })

    # 获取商品（只取黄金和原油）
    for name in ["黄金", "原油WTI"]:
        symbol = COMMODITIES.get(name)
        if symbol:
            quote = get_quote(symbol)
            if quote.get("status") == "success":
                direction = quote.get("direction", "flat")
                emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"
                overview["commodities"].append({
                    "name": name,
                    "price": quote.get("price", 0),
                    "change_percent": round(quote.get("change_percent", 0), 2),
                    "direction": direction,
                    "emoji": emoji
                })

    # 获取汇率（只取美元/人民币）
    for name in ["美元/人民币"]:
        symbol = FOREX.get(name)
        if symbol:
            quote = get_quote(symbol)
            if quote.get("status") == "success":
                direction = quote.get("direction", "flat")
                emoji = "⬆️" if direction == "up" else "⬇️" if direction == "down" else "➡️"
                overview["forex"].append({
                    "name": name,
                    "price": round(quote.get("price", 0), 4),
                    "change_percent": round(quote.get("change_percent", 0), 2),
                    "direction": direction,
                    "emoji": emoji
                })

    # 市场情绪
    if up_count > down_count:
        overview["market_sentiment"] = "🟢 偏多"
    elif down_count > up_count:
        overview["market_sentiment"] = "🔴 偏空"
    else:
        overview["market_sentiment"] = "⚪ 震荡"

    return overview


def get_index_snapshot(region: str = "all") -> Dict:
    """
    获取指数快照

    Args:
        region: 地区筛选 (asia/us/europe/all)

    Returns:
        指数数据
    """
    region_indices = {
        "asia": ["上证指数", "深证成指", "恒生指数", "日经225"],
        "us": ["标普500", "纳斯达克", "道琼斯"],
        "europe": ["富时100", "DAX"]
    }

    if region == "all":
        selected = list(INDICES.keys())
    else:
        selected = region_indices.get(region, list(INDICES.keys()))

    data = []
    for name in selected:
        symbol = INDICES.get(name)
        if symbol:
            quote = get_quote(symbol)
            if quote.get("status") == "success":
                direction = quote.get("direction", "flat")
                emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"
                data.append({
                    "name": name,
                    "price": quote.get("price", 0),
                    "change": round(quote.get("change", 0), 2),
                    "change_percent": round(quote.get("change_percent", 0), 2),
                    "emoji": emoji
                })

    return {
        "status": "success",
        "region": region,
        "indices": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_crypto_snapshot() -> Dict:
    """获取加密货币快照"""
    data = []
    for name, symbol in CRYPTOS.items():
        quote = get_quote(symbol)
        if quote.get("status") == "success":
            direction = quote.get("direction", "flat")
            emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"
            data.append({
                "name": name,
                "symbol": symbol.replace("-USD", ""),
                "price": quote.get("price", 0),
                "change_percent": round(quote.get("change_percent", 0), 2),
                "emoji": emoji
            })

    return {
        "status": "success",
        "crypto": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_commodity_snapshot() -> Dict:
    """获取商品快照"""
    data = []
    for name, symbol in COMMODITIES.items():
        quote = get_quote(symbol)
        if quote.get("status") == "success":
            direction = quote.get("direction", "flat")
            emoji = "🟢" if direction == "up" else "🔴" if direction == "down" else "⚪"
            data.append({
                "name": name,
                "price": round(quote.get("price", 0), 2),
                "change_percent": round(quote.get("change_percent", 0), 2),
                "emoji": emoji
            })

    return {
        "status": "success",
        "commodities": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_forex_snapshot() -> Dict:
    """获取外汇快照"""
    data = []
    for name, symbol in FOREX.items():
        quote = get_quote(symbol)
        if quote.get("status") == "success":
            direction = quote.get("direction", "flat")
            emoji = "⬆️" if direction == "up" else "⬇️" if direction == "down" else "➡️"
            data.append({
                "name": name,
                "rate": round(quote.get("price", 0), 4),
                "change_percent": round(quote.get("change_percent", 0), 2),
                "emoji": emoji
            })

    return {
        "status": "success",
        "forex": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_market_movers(market: str = "us", limit: int = 5) -> Dict:
    """
    获取涨跌幅榜

    Args:
        market: 市场 (us/hk/cn)
        limit: 返回数量

    Returns:
        涨跌幅榜数据
    """
    # 模拟数据（实际应用需要对接API）
    movers = {
        "us": {
            "gainers": [
                {"symbol": "NVDA", "name": "英伟达", "change_percent": 5.2},
                {"symbol": "TSLA", "name": "特斯拉", "change_percent": 3.8},
                {"symbol": "AMD", "name": "AMD", "change_percent": 2.9}
            ],
            "losers": [
                {"symbol": "INTC", "name": "英特尔", "change_percent": -2.1},
                {"symbol": "WMT", "name": "沃尔玛", "change_percent": -1.5},
                {"symbol": "KO", "name": "可口可乐", "change_percent": -0.9}
            ]
        }
    }

    market_data = movers.get(market, movers["us"])

    return {
        "status": "success",
        "market": market,
        "gainers": market_data["gainers"][:limit],
        "losers": market_data["losers"][:limit],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
