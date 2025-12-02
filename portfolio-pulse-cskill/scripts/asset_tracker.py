"""
Asset Tracker - 资产追踪模块
追踪股票、加密货币、大宗商品价格
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

try:
    import yfinance as yf
except ImportError:
    yf = None

# 资产类型定义
ASSET_TYPES = {
    "stock": "股票",
    "crypto": "加密货币",
    "commodity": "大宗商品",
    "forex": "外汇",
    "index": "指数"
}

# 常见股票代码映射
STOCK_SYMBOLS = {
    # 美股
    "苹果": "AAPL", "apple": "AAPL",
    "微软": "MSFT", "microsoft": "MSFT",
    "谷歌": "GOOGL", "google": "GOOGL",
    "亚马逊": "AMZN", "amazon": "AMZN",
    "特斯拉": "TSLA", "tesla": "TSLA",
    "英伟达": "NVDA", "nvidia": "NVDA",
    "脸书": "META", "meta": "META",
    # 港股
    "腾讯": "0700.HK",
    "阿里巴巴": "9988.HK", "阿里": "9988.HK",
    "美团": "3690.HK",
    "小米": "1810.HK",
}

# 加密货币代码
CRYPTO_SYMBOLS = {
    "比特币": "BTC-USD", "btc": "BTC-USD", "bitcoin": "BTC-USD",
    "以太坊": "ETH-USD", "eth": "ETH-USD", "ethereum": "ETH-USD",
    "狗狗币": "DOGE-USD", "doge": "DOGE-USD",
    "瑞波币": "XRP-USD", "xrp": "XRP-USD",
    "莱特币": "LTC-USD", "ltc": "LTC-USD",
}

# 大宗商品代码
COMMODITY_SYMBOLS = {
    "黄金": "GC=F", "gold": "GC=F",
    "白银": "SI=F", "silver": "SI=F",
    "原油": "CL=F", "oil": "CL=F", "wti": "CL=F",
    "布伦特原油": "BZ=F", "brent": "BZ=F",
    "天然气": "NG=F", "natural gas": "NG=F",
    "铜": "HG=F", "copper": "HG=F",
}


def _get_symbol(name: str, asset_type: str = None) -> Optional[str]:
    """获取资产代码"""
    name_lower = name.lower()

    # 如果已经是代码格式，直接返回
    if name.isupper() or "=" in name or "-" in name or "." in name:
        return name

    # 查找映射
    if asset_type == "crypto" or name_lower in CRYPTO_SYMBOLS:
        return CRYPTO_SYMBOLS.get(name_lower, f"{name.upper()}-USD")
    elif asset_type == "commodity" or name_lower in COMMODITY_SYMBOLS:
        return COMMODITY_SYMBOLS.get(name_lower)
    else:
        return STOCK_SYMBOLS.get(name_lower, name.upper())


def get_stock_price(symbol: str) -> Dict:
    """
    获取股票价格

    Args:
        symbol: 股票代码或名称

    Returns:
        价格信息
    """
    if yf is None:
        return {"error": "yfinance not installed"}

    actual_symbol = _get_symbol(symbol, "stock")

    try:
        ticker = yf.Ticker(actual_symbol)
        hist = ticker.history(period="5d")

        if hist.empty:
            return {"error": f"无法获取 {symbol} 数据"}

        current = hist['Close'].iloc[-1]
        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
        change = current - previous
        change_pct = (change / previous * 100) if previous else 0

        # 获取更多信息
        info = ticker.fast_info

        return {
            "symbol": actual_symbol,
            "name": symbol,
            "type": "stock",
            "price": round(current, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "direction": "up" if change > 0 else ("down" if change < 0 else "flat"),
            "currency": getattr(info, 'currency', 'USD'),
            "market_cap": getattr(info, 'market_cap', None),
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_crypto_price(symbol: str) -> Dict:
    """
    获取加密货币价格

    Args:
        symbol: 加密货币代码或名称

    Returns:
        价格信息
    """
    if yf is None:
        return {"error": "yfinance not installed"}

    actual_symbol = _get_symbol(symbol, "crypto")

    try:
        ticker = yf.Ticker(actual_symbol)
        hist = ticker.history(period="5d")

        if hist.empty:
            return {"error": f"无法获取 {symbol} 数据"}

        current = hist['Close'].iloc[-1]
        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
        change = current - previous
        change_pct = (change / previous * 100) if previous else 0

        # 24小时变化
        hist_24h = ticker.history(period="1d", interval="1h")
        if not hist_24h.empty and len(hist_24h) > 1:
            change_24h = current - hist_24h['Close'].iloc[0]
            change_24h_pct = (change_24h / hist_24h['Close'].iloc[0] * 100)
        else:
            change_24h = change
            change_24h_pct = change_pct

        return {
            "symbol": actual_symbol.replace("-USD", ""),
            "name": symbol,
            "type": "crypto",
            "price": round(current, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "change_24h": round(change_24h, 2),
            "change_24h_percent": round(change_24h_pct, 2),
            "direction": "up" if change > 0 else ("down" if change < 0 else "flat"),
            "currency": "USD",
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_commodity_price(symbol: str) -> Dict:
    """
    获取大宗商品价格

    Args:
        symbol: 商品代码或名称

    Returns:
        价格信息
    """
    if yf is None:
        return {"error": "yfinance not installed"}

    actual_symbol = _get_symbol(symbol, "commodity")
    if not actual_symbol:
        return {"error": f"未知商品: {symbol}"}

    try:
        ticker = yf.Ticker(actual_symbol)
        hist = ticker.history(period="5d")

        if hist.empty:
            return {"error": f"无法获取 {symbol} 数据"}

        current = hist['Close'].iloc[-1]
        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
        change = current - previous
        change_pct = (change / previous * 100) if previous else 0

        # 商品单位
        units = {
            "GC=F": "美元/盎司",
            "SI=F": "美元/盎司",
            "CL=F": "美元/桶",
            "BZ=F": "美元/桶",
            "NG=F": "美元/百万BTU",
            "HG=F": "美元/磅"
        }

        return {
            "symbol": actual_symbol,
            "name": symbol,
            "type": "commodity",
            "price": round(current, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "direction": "up" if change > 0 else ("down" if change < 0 else "flat"),
            "unit": units.get(actual_symbol, "USD"),
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_multi_asset_prices(assets: List[Dict]) -> List[Dict]:
    """
    批量获取多个资产价格

    Args:
        assets: 资产列表 [{"symbol": "AAPL", "type": "stock"}, ...]

    Returns:
        价格列表
    """
    results = []

    for asset in assets:
        symbol = asset.get("symbol", "")
        asset_type = asset.get("type", "stock")

        if asset_type == "crypto":
            price_data = get_crypto_price(symbol)
        elif asset_type == "commodity":
            price_data = get_commodity_price(symbol)
        else:
            price_data = get_stock_price(symbol)

        # 添加持仓信息
        if "quantity" in asset:
            price_data["quantity"] = asset["quantity"]
            if "price" in price_data:
                price_data["value"] = round(price_data["price"] * asset["quantity"], 2)

        if "cost_basis" in asset:
            price_data["cost_basis"] = asset["cost_basis"]
            if "value" in price_data:
                price_data["profit_loss"] = round(price_data["value"] - asset["cost_basis"], 2)
                price_data["profit_loss_percent"] = round(
                    (price_data["profit_loss"] / asset["cost_basis"]) * 100, 2
                ) if asset["cost_basis"] else 0

        results.append(price_data)

    return results


def get_market_overview() -> Dict:
    """获取市场概览"""
    overview = {
        "indices": [],
        "commodities": [],
        "crypto": []
    }

    # 主要指数
    for symbol, name in [("^GSPC", "标普500"), ("^DJI", "道琼斯"), ("^IXIC", "纳斯达克")]:
        data = get_stock_price(symbol)
        if "error" not in data:
            data["name"] = name
            overview["indices"].append(data)

    # 主要商品
    for name in ["黄金", "原油"]:
        data = get_commodity_price(name)
        if "error" not in data:
            overview["commodities"].append(data)

    # 主要加密货币
    for name in ["比特币", "以太坊"]:
        data = get_crypto_price(name)
        if "error" not in data:
            overview["crypto"].append(data)

    return overview
