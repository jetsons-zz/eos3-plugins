"""
Market Client - 全球股市数据客户端
使用 yfinance 获取全球主要股指和市场数据
无需 API Key，2000请求/小时
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings

# 忽略 yfinance 的一些警告
warnings.filterwarnings('ignore', category=FutureWarning)

try:
    import yfinance as yf
except ImportError:
    yf = None
    print("Warning: yfinance not installed. Run: pip install yfinance")


# 全球主要股指代码
MAJOR_INDICES = {
    # 美国
    "^GSPC": {"name": "标普500", "region": "美国", "currency": "USD"},
    "^DJI": {"name": "道琼斯工业", "region": "美国", "currency": "USD"},
    "^IXIC": {"name": "纳斯达克综合", "region": "美国", "currency": "USD"},
    "^VIX": {"name": "恐慌指数VIX", "region": "美国", "currency": "USD"},

    # 欧洲
    "^FTSE": {"name": "富时100", "region": "英国", "currency": "GBP"},
    "^GDAXI": {"name": "德国DAX", "region": "德国", "currency": "EUR"},
    "^FCHI": {"name": "法国CAC40", "region": "法国", "currency": "EUR"},

    # 亚太
    "^N225": {"name": "日经225", "region": "日本", "currency": "JPY"},
    "^HSI": {"name": "恒生指数", "region": "香港", "currency": "HKD"},
    "000001.SS": {"name": "上证综指", "region": "中国", "currency": "CNY"},
    "399001.SZ": {"name": "深证成指", "region": "中国", "currency": "CNY"},
    "^KS11": {"name": "韩国KOSPI", "region": "韩国", "currency": "KRW"},
    "^AXJO": {"name": "澳洲ASX200", "region": "澳大利亚", "currency": "AUD"},
    "^BSESN": {"name": "印度孟买", "region": "印度", "currency": "INR"},
}

# 主要货币对
MAJOR_CURRENCIES = {
    "EURUSD=X": {"name": "欧元/美元", "base": "EUR", "quote": "USD"},
    "GBPUSD=X": {"name": "英镑/美元", "base": "GBP", "quote": "USD"},
    "USDJPY=X": {"name": "美元/日元", "base": "USD", "quote": "JPY"},
    "USDCNY=X": {"name": "美元/人民币", "base": "USD", "quote": "CNY"},
    "USDHKD=X": {"name": "美元/港币", "base": "USD", "quote": "HKD"},
}

# 大宗商品
COMMODITIES = {
    "GC=F": {"name": "黄金", "unit": "美元/盎司"},
    "SI=F": {"name": "白银", "unit": "美元/盎司"},
    "CL=F": {"name": "WTI原油", "unit": "美元/桶"},
    "BZ=F": {"name": "布伦特原油", "unit": "美元/桶"},
}

# 加密货币
CRYPTO = {
    "BTC-USD": {"name": "比特币", "symbol": "BTC"},
    "ETH-USD": {"name": "以太坊", "symbol": "ETH"},
}


class MarketClient:
    """全球市场数据客户端"""

    def __init__(self):
        if yf is None:
            raise ImportError("yfinance is required. Install with: pip install yfinance")
        self._cache = {}
        self._cache_ttl = 60  # 缓存60秒

    def _is_cache_valid(self, key: str) -> bool:
        """检查缓存是否有效"""
        if key not in self._cache:
            return False
        cached_time = self._cache[key].get('_cached_at', 0)
        return (datetime.now().timestamp() - cached_time) < self._cache_ttl

    def get_index_quote(self, symbol: str) -> Optional[Dict]:
        """
        获取单个指数行情

        Args:
            symbol: 指数代码，如 "^GSPC" (标普500)

        Returns:
            Dict with price, change, change_percent, etc.
        """
        cache_key = f"quote_{symbol}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info

            # 获取基本信息
            current_price = getattr(info, 'last_price', None)
            previous_close = getattr(info, 'previous_close', None)

            if current_price is None:
                # 尝试从历史数据获取
                hist = ticker.history(period="2d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    if len(hist) > 1:
                        previous_close = hist['Close'].iloc[-2]

            if current_price is None:
                return None

            change = current_price - previous_close if previous_close else 0
            change_pct = (change / previous_close * 100) if previous_close else 0

            # 获取指数元信息
            meta = MAJOR_INDICES.get(symbol, {})

            result = {
                "symbol": symbol,
                "name": meta.get("name", symbol),
                "region": meta.get("region", "未知"),
                "currency": meta.get("currency", "USD"),
                "price": round(current_price, 2),
                "previous_close": round(previous_close, 2) if previous_close else None,
                "change": round(change, 2),
                "change_percent": round(change_pct, 2),
                "direction": "up" if change > 0 else ("down" if change < 0 else "flat"),
                "updated_at": datetime.now().isoformat(),
                "_cached_at": datetime.now().timestamp()
            }

            self._cache[cache_key] = result
            return result

        except Exception as e:
            return {"symbol": symbol, "error": str(e)}

    def get_multiple_quotes(self, symbols: List[str]) -> List[Dict]:
        """批量获取多个标的行情"""
        results = []
        for symbol in symbols:
            quote = self.get_index_quote(symbol)
            if quote:
                results.append(quote)
        return results

    def get_all_major_indices(self) -> Dict[str, List[Dict]]:
        """获取所有主要股指，按地区分组"""
        quotes = self.get_multiple_quotes(list(MAJOR_INDICES.keys()))

        # 按地区分组
        by_region = {}
        for quote in quotes:
            if 'error' not in quote:
                region = quote.get('region', '其他')
                if region not in by_region:
                    by_region[region] = []
                by_region[region].append(quote)

        return by_region

    def get_currencies(self) -> List[Dict]:
        """获取主要货币汇率"""
        results = []
        for symbol, meta in MAJOR_CURRENCIES.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = current - previous
                    change_pct = (change / previous * 100) if previous else 0

                    results.append({
                        "symbol": symbol,
                        "name": meta["name"],
                        "rate": round(current, 4),
                        "change": round(change, 4),
                        "change_percent": round(change_pct, 2),
                        "direction": "up" if change > 0 else ("down" if change < 0 else "flat")
                    })
            except:
                pass
        return results

    def get_commodities(self) -> List[Dict]:
        """获取大宗商品价格"""
        results = []
        for symbol, meta in COMMODITIES.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = current - previous
                    change_pct = (change / previous * 100) if previous else 0

                    results.append({
                        "symbol": symbol,
                        "name": meta["name"],
                        "price": round(current, 2),
                        "unit": meta["unit"],
                        "change": round(change, 2),
                        "change_percent": round(change_pct, 2),
                        "direction": "up" if change > 0 else ("down" if change < 0 else "flat")
                    })
            except:
                pass
        return results

    def get_crypto(self) -> List[Dict]:
        """获取加密货币价格"""
        results = []
        for symbol, meta in CRYPTO.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = current - previous
                    change_pct = (change / previous * 100) if previous else 0

                    results.append({
                        "symbol": meta["symbol"],
                        "name": meta["name"],
                        "price": round(current, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_pct, 2),
                        "direction": "up" if change > 0 else ("down" if change < 0 else "flat")
                    })
            except:
                pass
        return results

    def get_market_hours_status(self) -> Dict[str, str]:
        """获取各市场开盘状态"""
        now = datetime.utcnow()
        hour = now.hour
        weekday = now.weekday()

        # 简化的市场时间判断 (UTC)
        status = {}

        # 周末全部休市
        if weekday >= 5:
            return {
                "美国": "休市",
                "欧洲": "休市",
                "亚太": "休市",
                "总结": "周末休市"
            }

        # 美国: 14:30-21:00 UTC (9:30-16:00 EST)
        if 14 <= hour < 21:
            status["美国"] = "交易中"
        elif 13 <= hour < 14:
            status["美国"] = "盘前"
        elif 21 <= hour < 22:
            status["美国"] = "盘后"
        else:
            status["美国"] = "休市"

        # 欧洲: 08:00-16:30 UTC
        if 8 <= hour < 16:
            status["欧洲"] = "交易中"
        else:
            status["欧洲"] = "休市"

        # 亚太: 00:00-07:00 UTC (中国 08:00-15:00)
        if 1 <= hour < 7:
            status["亚太"] = "交易中"
        else:
            status["亚太"] = "休市"

        # 总结
        trading = [k for k, v in status.items() if v == "交易中"]
        if trading:
            status["总结"] = f"{', '.join(trading)}交易中"
        else:
            status["总结"] = "全球主要市场休市"

        return status


def get_market_summary() -> Dict:
    """
    获取全球市场概览

    Returns:
        Dict containing indices by region, currencies, commodities, crypto
    """
    client = MarketClient()

    return {
        "indices": client.get_all_major_indices(),
        "currencies": client.get_currencies(),
        "commodities": client.get_commodities(),
        "crypto": client.get_crypto(),
        "market_status": client.get_market_hours_status(),
        "generated_at": datetime.now().isoformat()
    }


def get_index_quote(symbol: str) -> Optional[Dict]:
    """
    获取单个指数行情的便捷函数

    Args:
        symbol: 指数代码

    Returns:
        Quote data or None
    """
    client = MarketClient()
    return client.get_index_quote(symbol)


# 便捷常量导出
SYMBOLS = {
    "indices": MAJOR_INDICES,
    "currencies": MAJOR_CURRENCIES,
    "commodities": COMMODITIES,
    "crypto": CRYPTO
}
