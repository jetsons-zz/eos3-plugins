"""
Market Analyzer - 市场分析模块
提供市场情绪分析、板块表现、涨跌幅排行等
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .market_client import MarketClient, MAJOR_INDICES


def analyze_market_sentiment(indices_data: Dict[str, List[Dict]]) -> Dict:
    """
    分析全球市场情绪

    Args:
        indices_data: 按地区分组的指数数据

    Returns:
        市场情绪分析结果
    """
    all_indices = []
    for region, indices in indices_data.items():
        all_indices.extend(indices)

    if not all_indices:
        return {"sentiment": "unknown", "message": "无法获取市场数据"}

    # 计算上涨/下跌比例
    up_count = sum(1 for idx in all_indices if idx.get('direction') == 'up')
    down_count = sum(1 for idx in all_indices if idx.get('direction') == 'down')
    total = len(all_indices)

    up_ratio = up_count / total if total > 0 else 0

    # 计算平均涨跌幅
    changes = [idx.get('change_percent', 0) for idx in all_indices]
    avg_change = sum(changes) / len(changes) if changes else 0

    # 检查VIX恐慌指数
    vix_data = None
    for idx in all_indices:
        if idx.get('symbol') == '^VIX':
            vix_data = idx
            break

    # 确定市场情绪
    if up_ratio >= 0.7 and avg_change > 0.5:
        sentiment = "bullish"
        sentiment_cn = "看涨"
        emoji = "📈"
        description = "全球市场普遍上涨，投资者情绪乐观"
    elif up_ratio >= 0.6:
        sentiment = "slightly_bullish"
        sentiment_cn = "偏多"
        emoji = "📊"
        description = "市场整体偏强，多数指数收涨"
    elif up_ratio <= 0.3 and avg_change < -0.5:
        sentiment = "bearish"
        sentiment_cn = "看跌"
        emoji = "📉"
        description = "全球市场普遍下跌，避险情绪升温"
    elif up_ratio <= 0.4:
        sentiment = "slightly_bearish"
        sentiment_cn = "偏空"
        emoji = "⚠️"
        description = "市场整体偏弱，谨慎观望为宜"
    else:
        sentiment = "neutral"
        sentiment_cn = "中性"
        emoji = "➡️"
        description = "市场涨跌互现，方向不明确"

    # VIX 分析
    vix_analysis = None
    if vix_data and 'price' in vix_data:
        vix_level = vix_data['price']
        if vix_level < 15:
            vix_analysis = {"level": "低", "description": "市场平静，波动性极低"}
        elif vix_level < 20:
            vix_analysis = {"level": "正常", "description": "市场波动性处于正常水平"}
        elif vix_level < 30:
            vix_analysis = {"level": "偏高", "description": "市场存在一定不确定性"}
        else:
            vix_analysis = {"level": "高", "description": "市场恐慌情绪明显，波动加剧"}
        vix_analysis["value"] = vix_level

    return {
        "sentiment": sentiment,
        "sentiment_cn": sentiment_cn,
        "emoji": emoji,
        "description": description,
        "statistics": {
            "total_indices": total,
            "up_count": up_count,
            "down_count": down_count,
            "flat_count": total - up_count - down_count,
            "up_ratio": round(up_ratio * 100, 1),
            "avg_change_percent": round(avg_change, 2)
        },
        "vix": vix_analysis,
        "analyzed_at": datetime.now().isoformat()
    }


def get_sector_performance(indices_data: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """
    按地区分析表现

    Args:
        indices_data: 按地区分组的指数数据

    Returns:
        各地区表现分析
    """
    region_performance = {}

    for region, indices in indices_data.items():
        if not indices:
            continue

        changes = [idx.get('change_percent', 0) for idx in indices]
        avg_change = sum(changes) / len(changes)

        # 找出该地区最强和最弱
        sorted_indices = sorted(indices, key=lambda x: x.get('change_percent', 0), reverse=True)
        best = sorted_indices[0] if sorted_indices else None
        worst = sorted_indices[-1] if sorted_indices else None

        region_performance[region] = {
            "avg_change_percent": round(avg_change, 2),
            "direction": "up" if avg_change > 0 else ("down" if avg_change < 0 else "flat"),
            "indices_count": len(indices),
            "best_performer": {
                "name": best.get('name'),
                "change_percent": best.get('change_percent')
            } if best else None,
            "worst_performer": {
                "name": worst.get('name'),
                "change_percent": worst.get('change_percent')
            } if worst else None
        }

    # 按表现排序
    sorted_regions = sorted(
        region_performance.items(),
        key=lambda x: x[1]['avg_change_percent'],
        reverse=True
    )

    return {
        "by_region": region_performance,
        "ranking": [r[0] for r in sorted_regions],
        "best_region": sorted_regions[0][0] if sorted_regions else None,
        "worst_region": sorted_regions[-1][0] if sorted_regions else None
    }


def get_market_movers(indices_data: Dict[str, List[Dict]], top_n: int = 5) -> Dict:
    """
    获取涨跌幅排行

    Args:
        indices_data: 按地区分组的指数数据
        top_n: 返回前N个

    Returns:
        涨幅榜和跌幅榜
    """
    all_indices = []
    for region, indices in indices_data.items():
        all_indices.extend(indices)

    # 过滤掉VIX（因为VIX上涨代表恐慌而非利好）
    tradeable = [idx for idx in all_indices if idx.get('symbol') != '^VIX']

    # 按涨跌幅排序
    sorted_by_change = sorted(
        tradeable,
        key=lambda x: x.get('change_percent', 0),
        reverse=True
    )

    gainers = sorted_by_change[:top_n]
    losers = sorted_by_change[-top_n:][::-1]  # 跌幅最大的

    return {
        "top_gainers": [
            {
                "name": g.get('name'),
                "region": g.get('region'),
                "change_percent": g.get('change_percent'),
                "price": g.get('price')
            } for g in gainers
        ],
        "top_losers": [
            {
                "name": l.get('name'),
                "region": l.get('region'),
                "change_percent": l.get('change_percent'),
                "price": l.get('price')
            } for l in losers
        ],
        "generated_at": datetime.now().isoformat()
    }


def compare_indices(symbols: List[str], period: str = "1mo") -> Dict:
    """
    比较多个指数的历史表现

    Args:
        symbols: 指数代码列表
        period: 时间周期 (1d, 5d, 1mo, 3mo, 6mo, 1y)

    Returns:
        比较结果
    """
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance not installed"}

    results = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                continue

            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            high = hist['High'].max()
            low = hist['Low'].min()

            period_return = ((end_price - start_price) / start_price) * 100

            meta = MAJOR_INDICES.get(symbol, {})

            results.append({
                "symbol": symbol,
                "name": meta.get("name", symbol),
                "period": period,
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "period_high": round(high, 2),
                "period_low": round(low, 2),
                "period_return_percent": round(period_return, 2),
                "volatility": round((high - low) / start_price * 100, 2)
            })
        except:
            pass

    # 按收益率排序
    results.sort(key=lambda x: x.get('period_return_percent', 0), reverse=True)

    return {
        "period": period,
        "comparison": results,
        "best_performer": results[0] if results else None,
        "worst_performer": results[-1] if results else None,
        "generated_at": datetime.now().isoformat()
    }


def get_quick_analysis() -> Dict:
    """
    快速市场分析（一站式接口）

    Returns:
        完整的市场分析报告数据
    """
    client = MarketClient()

    # 获取所有数据
    indices = client.get_all_major_indices()
    currencies = client.get_currencies()
    commodities = client.get_commodities()
    crypto = client.get_crypto()
    market_status = client.get_market_hours_status()

    # 分析
    sentiment = analyze_market_sentiment(indices)
    sector_perf = get_sector_performance(indices)
    movers = get_market_movers(indices)

    return {
        "market_status": market_status,
        "sentiment": sentiment,
        "sector_performance": sector_perf,
        "movers": movers,
        "indices": indices,
        "currencies": currencies,
        "commodities": commodities,
        "crypto": crypto,
        "generated_at": datetime.now().isoformat()
    }
