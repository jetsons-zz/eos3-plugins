"""
Sentiment Analyzer - 情绪分析引擎
新闻情绪、市场情绪指标、分析师评级
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Try to import requests for API calls
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class SentimentAnalyzer:
    """情绪分析引擎"""

    def __init__(self):
        self.cache = {}

    def analyze_text_sentiment(self, text: str) -> Dict:
        """
        分析文本情绪

        Args:
            text: 文本内容

        Returns:
            情绪分析结果
        """
        # 简单的关键词情绪分析
        positive_words = [
            'bullish', 'surge', 'gain', 'rise', 'up', 'growth', 'strong',
            'beat', 'exceed', 'outperform', 'rally', 'breakout', 'buy',
            'upgrade', 'positive', 'profit', 'success', 'increase', 'high',
            '上涨', '突破', '强势', '买入', '增长', '利好', '盈利', '涨停'
        ]

        negative_words = [
            'bearish', 'crash', 'loss', 'fall', 'down', 'decline', 'weak',
            'miss', 'underperform', 'selloff', 'breakdown', 'sell',
            'downgrade', 'negative', 'risk', 'warning', 'decrease', 'low',
            '下跌', '暴跌', '弱势', '卖出', '下降', '利空', '亏损', '跌停'
        ]

        text_lower = text.lower()

        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        total = pos_count + neg_count
        if total == 0:
            score = 0
        else:
            score = (pos_count - neg_count) / total

        if score > 0.3:
            sentiment = "positive"
        elif score < -0.3:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "score": round(score, 3),
            "sentiment": sentiment,
            "positive_signals": pos_count,
            "negative_signals": neg_count
        }


def analyze_news_sentiment(symbol: str, days: int = 7) -> Dict:
    """
    分析股票相关新闻情绪

    Args:
        symbol: 股票代码
        days: 分析天数

    Returns:
        新闻情绪分析结果
    """
    # 模拟新闻数据（实际应用中应接入新闻API）
    random.seed(hash(symbol + str(days)) % 1000)

    news_items = []
    sentiment_scores = []

    headlines = [
        f"{symbol} beats earnings expectations, stock surges",
        f"{symbol} announces new product line",
        f"Analysts upgrade {symbol} to buy rating",
        f"{symbol} faces regulatory challenges",
        f"Market uncertainty affects {symbol} outlook",
        f"{symbol} expands into new markets",
        f"CEO of {symbol} discusses growth strategy",
        f"{symbol} reports strong quarterly results"
    ]

    for i in range(min(days * 2, 10)):
        headline = random.choice(headlines)
        sentiment = random.uniform(-1, 1)
        sentiment_scores.append(sentiment)

        date = datetime.now() - timedelta(days=random.randint(0, days))

        news_items.append({
            "headline": headline,
            "date": date.strftime('%Y-%m-%d'),
            "sentiment": round(sentiment, 2),
            "source": random.choice(["Reuters", "Bloomberg", "CNBC", "WSJ", "MarketWatch"])
        })

    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    # 计算趋势
    recent = sentiment_scores[:len(sentiment_scores)//2] if len(sentiment_scores) > 1 else sentiment_scores
    older = sentiment_scores[len(sentiment_scores)//2:] if len(sentiment_scores) > 1 else sentiment_scores

    avg_recent = sum(recent) / len(recent) if recent else 0
    avg_older = sum(older) / len(older) if older else 0

    if avg_recent > avg_older + 0.1:
        trend = "improving"
    elif avg_recent < avg_older - 0.1:
        trend = "deteriorating"
    else:
        trend = "stable"

    # 情绪评级
    if avg_sentiment > 0.5:
        rating = "very_positive"
        rating_cn = "非常乐观"
    elif avg_sentiment > 0.2:
        rating = "positive"
        rating_cn = "乐观"
    elif avg_sentiment > -0.2:
        rating = "neutral"
        rating_cn = "中性"
    elif avg_sentiment > -0.5:
        rating = "negative"
        rating_cn = "悲观"
    else:
        rating = "very_negative"
        rating_cn = "非常悲观"

    return {
        "symbol": symbol,
        "period_days": days,
        "score": round(avg_sentiment, 3),
        "rating": rating,
        "rating_cn": rating_cn,
        "trend": trend,
        "news_count": len(news_items),
        "news_items": sorted(news_items, key=lambda x: x["date"], reverse=True)[:5],
        "analysis": _generate_sentiment_analysis(symbol, avg_sentiment, trend),
        "timestamp": datetime.now().isoformat()
    }


def _generate_sentiment_analysis(symbol: str, score: float, trend: str) -> str:
    """生成情绪分析文字"""
    if score > 0.5:
        base = f"{symbol} 近期新闻情绪非常积极，市场对该股票前景看好。"
    elif score > 0.2:
        base = f"{symbol} 近期新闻情绪偏正面，整体舆论环境较好。"
    elif score > -0.2:
        base = f"{symbol} 近期新闻情绪中性，市场关注度一般。"
    elif score > -0.5:
        base = f"{symbol} 近期新闻情绪偏负面，需关注潜在风险。"
    else:
        base = f"{symbol} 近期新闻情绪非常消极，市场担忧情绪明显。"

    if trend == "improving":
        base += "情绪趋势正在改善。"
    elif trend == "deteriorating":
        base += "情绪趋势正在恶化。"

    return base


def get_market_sentiment(market: str = "US") -> Dict:
    """
    获取整体市场情绪指标

    Args:
        market: 市场代码

    Returns:
        市场情绪数据
    """
    # 模拟恐惧贪婪指数（实际应用中应接入真实数据）
    random.seed(int(datetime.now().timestamp()) // 3600)  # 每小时变化

    fear_greed = random.randint(20, 80)
    vix = 15 + random.uniform(0, 20)

    # 根据恐惧贪婪指数判断
    if fear_greed >= 75:
        fg_level = "extreme_greed"
        fg_level_cn = "极度贪婪"
        fg_interpretation = "市场过度乐观，可能存在回调风险"
    elif fear_greed >= 55:
        fg_level = "greed"
        fg_level_cn = "贪婪"
        fg_interpretation = "市场情绪偏乐观，多头占优"
    elif fear_greed >= 45:
        fg_level = "neutral"
        fg_level_cn = "中性"
        fg_interpretation = "市场情绪均衡，观望为主"
    elif fear_greed >= 25:
        fg_level = "fear"
        fg_level_cn = "恐惧"
        fg_interpretation = "市场情绪偏悲观，空头占优"
    else:
        fg_level = "extreme_fear"
        fg_level_cn = "极度恐惧"
        fg_interpretation = "市场过度悲观，可能存在抄底机会"

    # VIX 解读
    if vix < 15:
        vix_level = "low"
        vix_interpretation = "市场波动性低，投资者情绪平稳"
    elif vix < 20:
        vix_level = "normal"
        vix_interpretation = "市场波动性正常"
    elif vix < 30:
        vix_level = "elevated"
        vix_interpretation = "市场波动性上升，注意风险"
    else:
        vix_level = "high"
        vix_interpretation = "市场波动性高，恐慌情绪蔓延"

    # 市场宽度指标
    advance_decline = random.uniform(-2, 2)
    new_highs = random.randint(50, 300)
    new_lows = random.randint(20, 200)

    return {
        "market": market,
        "fear_greed_index": {
            "value": fear_greed,
            "level": fg_level,
            "level_cn": fg_level_cn,
            "interpretation": fg_interpretation
        },
        "vix": {
            "value": round(vix, 2),
            "level": vix_level,
            "interpretation": vix_interpretation
        },
        "market_breadth": {
            "advance_decline_ratio": round(advance_decline, 2),
            "new_52w_highs": new_highs,
            "new_52w_lows": new_lows,
            "ratio": round(new_highs / new_lows, 2) if new_lows > 0 else 999
        },
        "overall_sentiment": fg_level,
        "recommendation": _get_sentiment_recommendation(fear_greed, vix),
        "timestamp": datetime.now().isoformat()
    }


def _get_sentiment_recommendation(fear_greed: int, vix: float) -> str:
    """根据情绪指标给出建议"""
    if fear_greed < 25 and vix > 25:
        return "极度恐慌，考虑分批建仓优质资产"
    elif fear_greed > 75 and vix < 15:
        return "极度贪婪，考虑获利了结或减仓"
    elif fear_greed < 40:
        return "市场偏恐惧，可关注超跌反弹机会"
    elif fear_greed > 60:
        return "市场偏贪婪，控制仓位，谨慎追高"
    else:
        return "市场情绪中性，按计划操作"


def analyze_insider_activity(symbol: str) -> Dict:
    """
    分析内部人交易活动

    Args:
        symbol: 股票代码

    Returns:
        内部人交易分析
    """
    random.seed(hash(symbol + "insider") % 1000)

    # 模拟内部人交易数据
    transactions = []
    buy_count = 0
    sell_count = 0
    buy_value = 0
    sell_value = 0

    for i in range(random.randint(3, 10)):
        is_buy = random.random() > 0.4

        shares = random.randint(1000, 100000)
        price = 50 + random.random() * 150
        value = shares * price

        transaction = {
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            "insider": random.choice(["CEO", "CFO", "COO", "Director", "VP"]),
            "type": "Buy" if is_buy else "Sell",
            "shares": shares,
            "price": round(price, 2),
            "value": round(value, 0)
        }
        transactions.append(transaction)

        if is_buy:
            buy_count += 1
            buy_value += value
        else:
            sell_count += 1
            sell_value += value

    # 计算买卖比率
    total_count = buy_count + sell_count
    buy_ratio = buy_count / total_count if total_count > 0 else 0.5

    # 判断信号
    if buy_ratio > 0.7:
        signal = "strong_buy"
        signal_cn = "强烈买入信号"
        interpretation = "内部人大量买入，看好公司前景"
    elif buy_ratio > 0.5:
        signal = "buy"
        signal_cn = "买入信号"
        interpretation = "内部人买入多于卖出"
    elif buy_ratio > 0.3:
        signal = "neutral"
        signal_cn = "中性"
        interpretation = "内部人交易偏均衡"
    else:
        signal = "sell"
        signal_cn = "卖出信号"
        interpretation = "内部人卖出较多，需关注"

    return {
        "symbol": symbol,
        "period": "90 days",
        "summary": {
            "buy_count": buy_count,
            "sell_count": sell_count,
            "buy_value": round(buy_value, 0),
            "sell_value": round(sell_value, 0),
            "buy_ratio": round(buy_ratio, 2)
        },
        "signal": signal,
        "signal_cn": signal_cn,
        "interpretation": interpretation,
        "recent_transactions": sorted(transactions, key=lambda x: x["date"], reverse=True)[:5],
        "timestamp": datetime.now().isoformat()
    }


def get_analyst_ratings(symbol: str) -> Dict:
    """
    获取分析师评级汇总

    Args:
        symbol: 股票代码

    Returns:
        分析师评级数据
    """
    random.seed(hash(symbol + "analyst") % 1000)

    # 模拟分析师评级
    total_analysts = random.randint(10, 30)

    strong_buy = random.randint(0, total_analysts // 3)
    remaining = total_analysts - strong_buy

    buy = random.randint(0, remaining // 2)
    remaining -= buy

    hold = random.randint(0, remaining)
    remaining -= hold

    sell = random.randint(0, remaining)
    strong_sell = remaining - sell

    # 计算共识评级
    score = (
        strong_buy * 5 +
        buy * 4 +
        hold * 3 +
        sell * 2 +
        strong_sell * 1
    ) / total_analysts if total_analysts > 0 else 3

    if score >= 4.5:
        consensus = "Strong Buy"
        consensus_cn = "强烈买入"
    elif score >= 3.5:
        consensus = "Buy"
        consensus_cn = "买入"
    elif score >= 2.5:
        consensus = "Hold"
        consensus_cn = "持有"
    elif score >= 1.5:
        consensus = "Sell"
        consensus_cn = "卖出"
    else:
        consensus = "Strong Sell"
        consensus_cn = "强烈卖出"

    # 模拟目标价
    current_price = 100 + random.random() * 200
    target_high = current_price * (1 + random.uniform(0.1, 0.5))
    target_low = current_price * (1 - random.uniform(0.1, 0.3))
    target_mean = (target_high + target_low) / 2

    upside = (target_mean - current_price) / current_price * 100

    return {
        "symbol": symbol,
        "total_analysts": total_analysts,
        "ratings": {
            "strong_buy": strong_buy,
            "buy": buy,
            "hold": hold,
            "sell": sell,
            "strong_sell": strong_sell
        },
        "consensus": {
            "rating": consensus,
            "rating_cn": consensus_cn,
            "score": round(score, 2)
        },
        "price_targets": {
            "current": round(current_price, 2),
            "mean": round(target_mean, 2),
            "high": round(target_high, 2),
            "low": round(target_low, 2),
            "upside_percent": round(upside, 1)
        },
        "recent_changes": _generate_recent_rating_changes(symbol),
        "interpretation": _get_rating_interpretation(consensus, upside),
        "timestamp": datetime.now().isoformat()
    }


def _generate_recent_rating_changes(symbol: str) -> List[Dict]:
    """生成近期评级变动"""
    random.seed(hash(symbol + "changes") % 1000)

    firms = ["Goldman Sachs", "Morgan Stanley", "JP Morgan", "Citi", "BofA",
             "Deutsche Bank", "UBS", "Credit Suisse", "Barclays", "Wells Fargo"]

    changes = []
    for i in range(random.randint(2, 5)):
        old_rating = random.choice(["Hold", "Buy", "Sell"])
        new_rating = random.choice(["Buy", "Strong Buy", "Hold", "Sell"])

        changes.append({
            "firm": random.choice(firms),
            "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            "old_rating": old_rating,
            "new_rating": new_rating,
            "action": "upgrade" if new_rating in ["Buy", "Strong Buy"] and old_rating in ["Hold", "Sell"] else "downgrade" if new_rating in ["Hold", "Sell"] and old_rating in ["Buy", "Strong Buy"] else "maintain"
        })

    return sorted(changes, key=lambda x: x["date"], reverse=True)


def _get_rating_interpretation(consensus: str, upside: float) -> str:
    """评级解读"""
    if consensus in ["Strong Buy", "Buy"]:
        if upside > 20:
            return f"分析师普遍看好，目标上涨空间{upside:.0f}%，可积极关注"
        else:
            return f"分析师偏看好，但目标价上涨空间有限({upside:.0f}%)"
    elif consensus == "Hold":
        return f"分析师评级中性，建议持有观望，预期上涨{upside:.0f}%"
    else:
        return f"分析师评级偏负面，建议谨慎，目标价显示{upside:.0f}%空间"
