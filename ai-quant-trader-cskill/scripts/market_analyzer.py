"""
Market Analyzer - 市场分析引擎
技术指标计算、形态识别、趋势分析
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Try to import yfinance, fallback to mock data
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


class MarketAnalyzer:
    """市场分析引擎"""

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def get_stock_data(self, symbol: str, period: str = "3mo") -> Dict:
        """
        获取股票数据

        Args:
            symbol: 股票代码
            period: 数据周期

        Returns:
            股票数据字典
        """
        cache_key = f"{symbol}_{period}"

        if HAS_YFINANCE:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)

                if hist.empty:
                    return self._get_mock_data(symbol)

                info = ticker.info

                return {
                    "symbol": symbol,
                    "name": info.get("shortName", symbol),
                    "price": hist['Close'].iloc[-1] if len(hist) > 0 else 0,
                    "open": hist['Open'].iloc[-1] if len(hist) > 0 else 0,
                    "high": hist['High'].iloc[-1] if len(hist) > 0 else 0,
                    "low": hist['Low'].iloc[-1] if len(hist) > 0 else 0,
                    "volume": int(hist['Volume'].iloc[-1]) if len(hist) > 0 else 0,
                    "history": {
                        "close": hist['Close'].tolist(),
                        "open": hist['Open'].tolist(),
                        "high": hist['High'].tolist(),
                        "low": hist['Low'].tolist(),
                        "volume": hist['Volume'].tolist(),
                        "dates": [d.strftime('%Y-%m-%d') for d in hist.index]
                    },
                    "market_cap": info.get("marketCap", 0),
                    "pe_ratio": info.get("trailingPE", 0),
                    "eps": info.get("trailingEps", 0),
                    "dividend_yield": info.get("dividendYield", 0),
                    "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
                    "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
                    "avg_volume": info.get("averageVolume", 0),
                    "beta": info.get("beta", 1.0),
                    "sector": info.get("sector", "Unknown"),
                    "industry": info.get("industry", "Unknown")
                }

            except Exception as e:
                return self._get_mock_data(symbol)
        else:
            return self._get_mock_data(symbol)

    def _get_mock_data(self, symbol: str) -> Dict:
        """生成模拟数据用于测试"""
        import random
        random.seed(hash(symbol) % 1000)

        base_price = 100 + random.random() * 200
        prices = []
        current = base_price

        for i in range(60):  # 60 days
            change = (random.random() - 0.5) * 5
            current = max(current + change, 1)
            prices.append(current)

        return {
            "symbol": symbol,
            "name": f"{symbol} Inc.",
            "price": prices[-1],
            "open": prices[-1] * 0.99,
            "high": prices[-1] * 1.02,
            "low": prices[-1] * 0.98,
            "volume": int(random.random() * 10000000),
            "history": {
                "close": prices,
                "open": [p * 0.99 for p in prices],
                "high": [p * 1.02 for p in prices],
                "low": [p * 0.98 for p in prices],
                "volume": [int(random.random() * 10000000) for _ in prices],
                "dates": [(datetime.now() - timedelta(days=60-i)).strftime('%Y-%m-%d') for i in range(60)]
            },
            "market_cap": int(base_price * 1e9),
            "pe_ratio": 15 + random.random() * 20,
            "eps": base_price / (15 + random.random() * 20),
            "dividend_yield": random.random() * 0.03,
            "fifty_two_week_high": max(prices) * 1.1,
            "fifty_two_week_low": min(prices) * 0.9,
            "avg_volume": int(random.random() * 10000000),
            "beta": 0.8 + random.random() * 0.6,
            "sector": "Technology",
            "industry": "Software"
        }


def calculate_sma(prices: List[float], period: int) -> List[float]:
    """计算简单移动平均"""
    if len(prices) < period:
        return [sum(prices) / len(prices)] * len(prices)

    sma = []
    for i in range(len(prices)):
        if i < period - 1:
            sma.append(sum(prices[:i+1]) / (i + 1))
        else:
            sma.append(sum(prices[i-period+1:i+1]) / period)
    return sma


def calculate_ema(prices: List[float], period: int) -> List[float]:
    """计算指数移动平均"""
    if not prices:
        return []

    multiplier = 2 / (period + 1)
    ema = [prices[0]]

    for i in range(1, len(prices)):
        ema.append((prices[i] - ema[-1]) * multiplier + ema[-1])

    return ema


def calculate_rsi(prices: List[float], period: int = 14) -> Dict:
    """
    计算RSI相对强弱指标

    Args:
        prices: 价格列表
        period: 周期

    Returns:
        RSI数据
    """
    if len(prices) < period + 1:
        return {"value": 50, "signal": "neutral", "overbought": False, "oversold": False}

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # 判断信号
    if rsi >= 70:
        signal = "overbought"
    elif rsi <= 30:
        signal = "oversold"
    elif rsi >= 50:
        signal = "bullish"
    else:
        signal = "bearish"

    return {
        "value": round(rsi, 2),
        "signal": signal,
        "overbought": rsi >= 70,
        "oversold": rsi <= 30,
        "interpretation": _get_rsi_interpretation(rsi)
    }


def _get_rsi_interpretation(rsi: float) -> str:
    """RSI解读"""
    if rsi >= 80:
        return "极度超买，强烈卖出信号"
    elif rsi >= 70:
        return "超买区域，考虑获利了结"
    elif rsi >= 60:
        return "偏强，多头占优"
    elif rsi >= 40:
        return "中性区域，观望"
    elif rsi >= 30:
        return "偏弱，空头占优"
    elif rsi >= 20:
        return "超卖区域，考虑买入"
    else:
        return "极度超卖，强烈买入信号"


def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """
    计算MACD指标

    Args:
        prices: 价格列表
        fast: 快线周期
        slow: 慢线周期
        signal: 信号线周期

    Returns:
        MACD数据
    """
    if len(prices) < slow:
        return {"macd": 0, "signal": 0, "histogram": 0, "trend": "neutral"}

    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)

    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = calculate_ema(macd_line, signal)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]

    current_macd = macd_line[-1]
    current_signal = signal_line[-1]
    current_hist = histogram[-1]

    # 判断趋势
    if current_macd > current_signal:
        if current_hist > 0 and (len(histogram) < 2 or histogram[-2] < current_hist):
            trend = "strong_bullish"
        else:
            trend = "bullish"
    else:
        if current_hist < 0 and (len(histogram) < 2 or histogram[-2] > current_hist):
            trend = "strong_bearish"
        else:
            trend = "bearish"

    # 检测金叉死叉
    cross = "none"
    if len(macd_line) >= 2 and len(signal_line) >= 2:
        if macd_line[-2] < signal_line[-2] and current_macd > current_signal:
            cross = "golden_cross"
        elif macd_line[-2] > signal_line[-2] and current_macd < current_signal:
            cross = "death_cross"

    return {
        "macd": round(current_macd, 4),
        "signal": round(current_signal, 4),
        "histogram": round(current_hist, 4),
        "trend": trend,
        "cross": cross,
        "interpretation": _get_macd_interpretation(trend, cross)
    }


def _get_macd_interpretation(trend: str, cross: str) -> str:
    """MACD解读"""
    if cross == "golden_cross":
        return "MACD金叉，买入信号"
    elif cross == "death_cross":
        return "MACD死叉，卖出信号"
    elif trend == "strong_bullish":
        return "强势上涨趋势，继续持有"
    elif trend == "bullish":
        return "上涨趋势，可考虑买入"
    elif trend == "strong_bearish":
        return "强势下跌趋势，建议离场"
    else:
        return "下跌趋势，谨慎观望"


def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict:
    """
    计算布林带

    Args:
        prices: 价格列表
        period: 周期
        std_dev: 标准差倍数

    Returns:
        布林带数据
    """
    if len(prices) < period:
        return {"upper": prices[-1], "middle": prices[-1], "lower": prices[-1], "width": 0}

    sma = calculate_sma(prices, period)
    middle = sma[-1]

    # 计算标准差
    recent_prices = prices[-period:]
    variance = sum((p - middle) ** 2 for p in recent_prices) / period
    std = math.sqrt(variance)

    upper = middle + std_dev * std
    lower = middle - std_dev * std
    width = (upper - lower) / middle * 100  # 百分比宽度

    current_price = prices[-1]

    # 判断位置
    if current_price >= upper:
        position = "above_upper"
        signal = "overbought"
    elif current_price <= lower:
        position = "below_lower"
        signal = "oversold"
    elif current_price > middle:
        position = "upper_half"
        signal = "bullish"
    else:
        position = "lower_half"
        signal = "bearish"

    # 计算%B指标
    percent_b = (current_price - lower) / (upper - lower) if upper != lower else 0.5

    return {
        "upper": round(upper, 2),
        "middle": round(middle, 2),
        "lower": round(lower, 2),
        "width": round(width, 2),
        "position": position,
        "signal": signal,
        "percent_b": round(percent_b, 2),
        "interpretation": _get_bb_interpretation(position, width)
    }


def _get_bb_interpretation(position: str, width: float) -> str:
    """布林带解读"""
    if position == "above_upper":
        return "价格突破上轨，可能超买或强势突破"
    elif position == "below_lower":
        return "价格跌破下轨，可能超卖或弱势下跌"
    elif width < 5:
        return "布林带收窄，可能即将变盘"
    elif width > 15:
        return "布林带扩张，波动加大"
    elif position == "upper_half":
        return "价格在中轨上方，偏强势"
    else:
        return "价格在中轨下方，偏弱势"


def calculate_kdj(prices: List[float], highs: List[float], lows: List[float],
                  n: int = 9, m1: int = 3, m2: int = 3) -> Dict:
    """
    计算KDJ随机指标

    Args:
        prices: 收盘价列表
        highs: 最高价列表
        lows: 最低价列表
        n, m1, m2: KDJ参数

    Returns:
        KDJ数据
    """
    if len(prices) < n:
        return {"k": 50, "d": 50, "j": 50, "signal": "neutral"}

    # 计算RSV
    rsv_list = []
    for i in range(len(prices)):
        if i < n - 1:
            period_high = max(highs[:i+1])
            period_low = min(lows[:i+1])
        else:
            period_high = max(highs[i-n+1:i+1])
            period_low = min(lows[i-n+1:i+1])

        if period_high == period_low:
            rsv = 50
        else:
            rsv = (prices[i] - period_low) / (period_high - period_low) * 100
        rsv_list.append(rsv)

    # 计算K、D、J
    k_list = [50]
    d_list = [50]

    for i in range(1, len(rsv_list)):
        k = (m1 - 1) / m1 * k_list[-1] + 1 / m1 * rsv_list[i]
        d = (m2 - 1) / m2 * d_list[-1] + 1 / m2 * k
        k_list.append(k)
        d_list.append(d)

    k = k_list[-1]
    d = d_list[-1]
    j = 3 * k - 2 * d

    # 判断信号
    if k > d and j > 80:
        signal = "overbought"
    elif k < d and j < 20:
        signal = "oversold"
    elif k > d:
        signal = "bullish"
    else:
        signal = "bearish"

    # 检测金叉死叉
    cross = "none"
    if len(k_list) >= 2 and len(d_list) >= 2:
        if k_list[-2] < d_list[-2] and k > d:
            cross = "golden_cross"
        elif k_list[-2] > d_list[-2] and k < d:
            cross = "death_cross"

    return {
        "k": round(k, 2),
        "d": round(d, 2),
        "j": round(j, 2),
        "signal": signal,
        "cross": cross,
        "interpretation": _get_kdj_interpretation(k, d, j, cross)
    }


def _get_kdj_interpretation(k: float, d: float, j: float, cross: str) -> str:
    """KDJ解读"""
    if cross == "golden_cross":
        return "KDJ金叉，短线买入信号"
    elif cross == "death_cross":
        return "KDJ死叉，短线卖出信号"
    elif j > 100:
        return "J值超100，极度超买，注意回调"
    elif j < 0:
        return "J值负值，极度超卖，可能反弹"
    elif k > 80 and d > 80:
        return "KD高位，超买区域"
    elif k < 20 and d < 20:
        return "KD低位，超卖区域"
    else:
        return "KDJ在正常区域运行"


def calculate_technical_indicators(symbol: str, indicators: List[str] = None) -> Dict:
    """
    计算技术指标

    Args:
        symbol: 股票代码
        indicators: 指标列表，默认计算所有

    Returns:
        技术指标数据
    """
    if indicators is None:
        indicators = ["MA", "EMA", "RSI", "MACD", "BBANDS", "KDJ"]

    analyzer = MarketAnalyzer()
    data = analyzer.get_stock_data(symbol)

    if not data or "history" not in data:
        return {"error": f"无法获取 {symbol} 数据"}

    prices = data["history"]["close"]
    highs = data["history"]["high"]
    lows = data["history"]["low"]

    result = {
        "symbol": symbol,
        "price": data["price"],
        "timestamp": datetime.now().isoformat(),
        "indicators": {}
    }

    for ind in indicators:
        ind_upper = ind.upper()

        if ind_upper == "MA" or ind_upper == "SMA":
            result["indicators"]["MA"] = {
                "MA5": round(calculate_sma(prices, 5)[-1], 2),
                "MA10": round(calculate_sma(prices, 10)[-1], 2),
                "MA20": round(calculate_sma(prices, 20)[-1], 2),
                "MA50": round(calculate_sma(prices, 50)[-1], 2) if len(prices) >= 50 else None,
                "MA200": round(calculate_sma(prices, 200)[-1], 2) if len(prices) >= 200 else None
            }

        elif ind_upper == "EMA":
            result["indicators"]["EMA"] = {
                "EMA12": round(calculate_ema(prices, 12)[-1], 2),
                "EMA26": round(calculate_ema(prices, 26)[-1], 2),
                "EMA50": round(calculate_ema(prices, 50)[-1], 2) if len(prices) >= 50 else None
            }

        elif ind_upper == "RSI":
            result["indicators"]["RSI"] = calculate_rsi(prices)

        elif ind_upper == "MACD":
            result["indicators"]["MACD"] = calculate_macd(prices)

        elif ind_upper == "BBANDS" or ind_upper == "BB":
            result["indicators"]["BBANDS"] = calculate_bollinger_bands(prices)

        elif ind_upper == "KDJ":
            result["indicators"]["KDJ"] = calculate_kdj(prices, highs, lows)

    return result


def detect_patterns(symbol: str, period: str = "1mo") -> Dict:
    """
    检测K线形态

    Args:
        symbol: 股票代码
        period: 数据周期

    Returns:
        形态识别结果
    """
    analyzer = MarketAnalyzer()
    data = analyzer.get_stock_data(symbol, period)

    if not data or "history" not in data:
        return {"error": f"无法获取 {symbol} 数据"}

    prices = data["history"]["close"]
    opens = data["history"]["open"]
    highs = data["history"]["high"]
    lows = data["history"]["low"]

    detected = []
    signals = []

    # 检测常见K线形态
    if len(prices) >= 2:
        # 锤子线/倒锤子
        last_open = opens[-1]
        last_close = prices[-1]
        last_high = highs[-1]
        last_low = lows[-1]
        body = abs(last_close - last_open)
        upper_shadow = last_high - max(last_open, last_close)
        lower_shadow = min(last_open, last_close) - last_low

        if lower_shadow > body * 2 and upper_shadow < body * 0.5:
            detected.append("hammer")
            signals.append({"pattern": "锤子线", "type": "bullish", "strength": "medium"})

        elif upper_shadow > body * 2 and lower_shadow < body * 0.5:
            detected.append("inverted_hammer")
            signals.append({"pattern": "倒锤子", "type": "bearish", "strength": "medium"})

        # 吞没形态
        if len(prices) >= 2:
            prev_open = opens[-2]
            prev_close = prices[-2]

            # 看涨吞没
            if (prev_close < prev_open and  # 前一根阴线
                last_close > last_open and  # 当前阳线
                last_open < prev_close and  # 开盘低于前收
                last_close > prev_open):     # 收盘高于前开
                detected.append("bullish_engulfing")
                signals.append({"pattern": "看涨吞没", "type": "bullish", "strength": "strong"})

            # 看跌吞没
            elif (prev_close > prev_open and  # 前一根阳线
                  last_close < last_open and  # 当前阴线
                  last_open > prev_close and  # 开盘高于前收
                  last_close < prev_open):     # 收盘低于前开
                detected.append("bearish_engulfing")
                signals.append({"pattern": "看跌吞没", "type": "bearish", "strength": "strong"})

    # 检测趋势形态
    if len(prices) >= 20:
        # 简单的双底检测
        min_idx = prices[-20:].index(min(prices[-20:]))
        second_min = float('inf')
        second_idx = -1

        for i, p in enumerate(prices[-20:]):
            if i != min_idx and abs(i - min_idx) > 3:
                if p < second_min:
                    second_min = p
                    second_idx = i

        if second_idx != -1:
            price_diff = abs(min(prices[-20:]) - second_min) / min(prices[-20:])
            if price_diff < 0.05:  # 两个低点相差5%以内
                detected.append("double_bottom")
                signals.append({"pattern": "双底", "type": "bullish", "strength": "strong"})

    # 检测支撑阻力
    support_resistance = _calculate_support_resistance(prices, highs, lows)

    return {
        "symbol": symbol,
        "detected_patterns": detected,
        "signals": signals,
        "pattern_count": len(detected),
        "support_resistance": support_resistance,
        "overall_bias": "bullish" if sum(1 for s in signals if s["type"] == "bullish") > sum(1 for s in signals if s["type"] == "bearish") else "bearish" if signals else "neutral"
    }


def _calculate_support_resistance(prices: List[float], highs: List[float], lows: List[float]) -> Dict:
    """计算支撑阻力位"""
    if len(prices) < 5:
        return {"support": [], "resistance": []}

    current = prices[-1]

    # 简单计算：使用近期高低点
    recent_highs = sorted(highs[-20:], reverse=True)[:3]
    recent_lows = sorted(lows[-20:])[:3]

    resistance = [h for h in recent_highs if h > current]
    support = [l for l in recent_lows if l < current]

    return {
        "support": [round(s, 2) for s in support],
        "resistance": [round(r, 2) for r in resistance],
        "nearest_support": round(support[0], 2) if support else None,
        "nearest_resistance": round(resistance[-1], 2) if resistance else None
    }


def analyze_trend(symbol: str) -> Dict:
    """
    分析趋势

    Args:
        symbol: 股票代码

    Returns:
        趋势分析结果
    """
    analyzer = MarketAnalyzer()
    data = analyzer.get_stock_data(symbol)

    if not data or "history" not in data:
        return {"error": f"无法获取 {symbol} 数据"}

    prices = data["history"]["close"]

    if len(prices) < 20:
        return {"trend": "unknown", "strength": 0}

    # 计算各周期趋势
    ma5 = calculate_sma(prices, 5)[-1]
    ma10 = calculate_sma(prices, 10)[-1]
    ma20 = calculate_sma(prices, 20)[-1]
    current = prices[-1]

    # 判断趋势方向
    bullish_signals = 0
    bearish_signals = 0

    if current > ma5:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if current > ma10:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if current > ma20:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if ma5 > ma10:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if ma10 > ma20:
        bullish_signals += 1
    else:
        bearish_signals += 1

    # 计算趋势强度
    total_signals = bullish_signals + bearish_signals
    if bullish_signals > bearish_signals:
        trend = "uptrend"
        strength = bullish_signals / total_signals * 100
    elif bearish_signals > bullish_signals:
        trend = "downtrend"
        strength = bearish_signals / total_signals * 100
    else:
        trend = "sideways"
        strength = 50

    # 计算动量
    momentum = (current - prices[-5]) / prices[-5] * 100 if prices[-5] != 0 else 0

    return {
        "symbol": symbol,
        "trend": trend,
        "strength": round(strength, 1),
        "momentum": round(momentum, 2),
        "price": round(current, 2),
        "ma5": round(ma5, 2),
        "ma10": round(ma10, 2),
        "ma20": round(ma20, 2),
        "price_vs_ma20": round((current / ma20 - 1) * 100, 2) if ma20 != 0 else 0,
        "interpretation": _get_trend_interpretation(trend, strength, momentum)
    }


def _get_trend_interpretation(trend: str, strength: float, momentum: float) -> str:
    """趋势解读"""
    if trend == "uptrend":
        if strength > 80:
            return "强势上涨趋势，多头主导"
        elif strength > 60:
            return "温和上涨趋势，可继续持有"
        else:
            return "弱势上涨，注意回调风险"
    elif trend == "downtrend":
        if strength > 80:
            return "强势下跌趋势，空头主导"
        elif strength > 60:
            return "温和下跌趋势，建议观望"
        else:
            return "弱势下跌，可能即将企稳"
    else:
        if abs(momentum) < 1:
            return "横盘整理，等待方向选择"
        else:
            return "震荡走势，短线操作为主"


def analyze_stock(symbol: str, market: str = "US") -> Dict:
    """
    综合分析股票

    Args:
        symbol: 股票代码
        market: 市场

    Returns:
        综合分析结果
    """
    # 获取基础数据
    analyzer = MarketAnalyzer()
    data = analyzer.get_stock_data(symbol)

    if not data or "history" not in data:
        return {"error": f"无法获取 {symbol} 数据"}

    # 计算技术指标
    indicators = calculate_technical_indicators(symbol)

    # 分析趋势
    trend = analyze_trend(symbol)

    # 检测形态
    patterns = detect_patterns(symbol)

    # 计算综合评分
    scores = {
        "trend_score": 0,
        "technical_score": 0,
        "pattern_score": 0
    }

    # 趋势评分
    if trend["trend"] == "uptrend":
        scores["trend_score"] = 50 + trend["strength"] / 2
    elif trend["trend"] == "downtrend":
        scores["trend_score"] = 50 - trend["strength"] / 2
    else:
        scores["trend_score"] = 50

    # 技术指标评分
    tech_signals = 0
    total_tech = 0

    if "RSI" in indicators.get("indicators", {}):
        rsi = indicators["indicators"]["RSI"]
        if rsi["signal"] == "oversold":
            tech_signals += 2
        elif rsi["signal"] == "bullish":
            tech_signals += 1
        elif rsi["signal"] == "bearish":
            tech_signals -= 1
        elif rsi["signal"] == "overbought":
            tech_signals -= 2
        total_tech += 2

    if "MACD" in indicators.get("indicators", {}):
        macd = indicators["indicators"]["MACD"]
        if macd["cross"] == "golden_cross":
            tech_signals += 3
        elif macd["cross"] == "death_cross":
            tech_signals -= 3
        elif "bullish" in macd["trend"]:
            tech_signals += 1
        else:
            tech_signals -= 1
        total_tech += 3

    if total_tech > 0:
        scores["technical_score"] = 50 + (tech_signals / total_tech) * 50

    # 形态评分
    if patterns.get("overall_bias") == "bullish":
        scores["pattern_score"] = 60 + len(patterns.get("signals", [])) * 5
    elif patterns.get("overall_bias") == "bearish":
        scores["pattern_score"] = 40 - len(patterns.get("signals", [])) * 5
    else:
        scores["pattern_score"] = 50

    # 综合评分
    overall_score = (
        scores["trend_score"] * 0.4 +
        scores["technical_score"] * 0.4 +
        scores["pattern_score"] * 0.2
    )

    # 生成信号
    if overall_score >= 70:
        signal = "STRONG_BUY"
        signal_cn = "强烈买入"
    elif overall_score >= 60:
        signal = "BUY"
        signal_cn = "买入"
    elif overall_score >= 45:
        signal = "HOLD"
        signal_cn = "持有"
    elif overall_score >= 35:
        signal = "SELL"
        signal_cn = "卖出"
    else:
        signal = "STRONG_SELL"
        signal_cn = "强烈卖出"

    return {
        "symbol": symbol,
        "name": data.get("name", symbol),
        "price": data["price"],
        "market": market,
        "overall_score": round(overall_score, 1),
        "signal": signal,
        "signal_cn": signal_cn,
        "scores": {
            "trend": round(scores["trend_score"], 1),
            "technical": round(scores["technical_score"], 1),
            "pattern": round(scores["pattern_score"], 1)
        },
        "trend_analysis": trend,
        "technical_indicators": indicators.get("indicators", {}),
        "pattern_analysis": patterns,
        "fundamentals": {
            "market_cap": data.get("market_cap", 0),
            "pe_ratio": data.get("pe_ratio", 0),
            "eps": data.get("eps", 0),
            "beta": data.get("beta", 1.0),
            "sector": data.get("sector", "Unknown")
        },
        "timestamp": datetime.now().isoformat()
    }
