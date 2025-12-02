"""
Report Generator - 报告生成器
交易报告、AI建议、研报生成
"""

from datetime import datetime
from typing import Dict, List, Optional

from .market_analyzer import analyze_stock, calculate_technical_indicators, detect_patterns, analyze_trend
from .sentiment_analyzer import analyze_news_sentiment, get_market_sentiment, get_analyst_ratings
from .alpha_generator import run_factor_model
from .risk_manager import analyze_portfolio_risk


def generate_trading_report(symbol: str) -> str:
    """
    生成综合交易报告

    Args:
        symbol: 股票代码

    Returns:
        Markdown格式报告
    """
    # 获取各项分析
    stock = analyze_stock(symbol)
    if "error" in stock:
        return f"# {symbol} 分析报告\n\n❌ 无法获取数据: {stock['error']}"

    indicators = calculate_technical_indicators(symbol)
    patterns = detect_patterns(symbol)
    trend = analyze_trend(symbol)
    sentiment = analyze_news_sentiment(symbol)
    ratings = get_analyst_ratings(symbol)

    # 构建报告
    report = []

    # 标题
    report.append(f"# {stock['name']} ({symbol}) 综合分析报告")
    report.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    # 核心评分
    report.append("## 📊 核心评分")
    score = stock['overall_score']
    signal = stock['signal_cn']
    score_bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))

    report.append(f"**综合评分**: {score}/100 [{score_bar}]")
    report.append(f"**交易信号**: **{signal}**")
    report.append(f"**当前价格**: ${stock['price']:.2f}\n")

    # 技术分析
    report.append("## 📈 技术分析")

    if "indicators" in indicators:
        ind = indicators["indicators"]

        if "RSI" in ind:
            rsi = ind["RSI"]
            report.append(f"- **RSI({14})**: {rsi['value']} - {rsi.get('interpretation', '')}")

        if "MACD" in ind:
            macd = ind["MACD"]
            report.append(f"- **MACD**: {macd.get('interpretation', '')}")
            if macd.get("cross") != "none":
                cross_cn = "金叉" if macd["cross"] == "golden_cross" else "死叉"
                report.append(f"  - ⚡ 信号: **{cross_cn}**")

        if "BBANDS" in ind:
            bb = ind["BBANDS"]
            report.append(f"- **布林带**: {bb.get('interpretation', '')}")

        if "KDJ" in ind:
            kdj = ind["KDJ"]
            report.append(f"- **KDJ**: K={kdj['k']}, D={kdj['d']}, J={kdj['j']}")

    report.append("")

    # 趋势分析
    report.append("## 📉 趋势分析")
    trend_cn = {"uptrend": "上涨", "downtrend": "下跌", "sideways": "横盘"}.get(trend["trend"], trend["trend"])
    report.append(f"- **当前趋势**: {trend_cn}")
    report.append(f"- **趋势强度**: {trend['strength']:.0f}%")
    report.append(f"- **5日动量**: {trend['momentum']:+.2f}%")
    report.append(f"- **解读**: {trend.get('interpretation', '')}\n")

    # 形态识别
    if patterns.get("signals"):
        report.append("## 🎯 形态信号")
        for sig in patterns["signals"]:
            type_emoji = "🟢" if sig["type"] == "bullish" else "🔴"
            report.append(f"- {type_emoji} **{sig['pattern']}** ({sig['strength']})")
        report.append("")

    # 支撑阻力
    sr = patterns.get("support_resistance", {})
    if sr.get("nearest_support") or sr.get("nearest_resistance"):
        report.append("## 🎚️ 关键价位")
        if sr.get("nearest_resistance"):
            report.append(f"- **最近阻力位**: ${sr['nearest_resistance']}")
        if sr.get("nearest_support"):
            report.append(f"- **最近支撑位**: ${sr['nearest_support']}")
        report.append("")

    # 情绪分析
    report.append("## 💬 情绪分析")
    report.append(f"- **新闻情绪**: {sentiment['rating_cn']} (评分: {sentiment['score']:.2f})")
    report.append(f"- **情绪趋势**: {sentiment['trend']}")
    report.append(f"- **分析师共识**: {ratings['consensus']['rating_cn']}")
    report.append(f"- **目标价**: ${ratings['price_targets']['mean']:.2f} "
                 f"(上涨空间: {ratings['price_targets']['upside_percent']:+.1f}%)\n")

    # 基本面
    report.append("## 📋 基本面")
    fund = stock.get("fundamentals", {})
    if fund.get("market_cap"):
        report.append(f"- **市值**: ${fund['market_cap']/1e9:.1f}B")
    if fund.get("pe_ratio"):
        report.append(f"- **市盈率**: {fund['pe_ratio']:.1f}")
    if fund.get("eps"):
        report.append(f"- **每股收益**: ${fund['eps']:.2f}")
    if fund.get("beta"):
        report.append(f"- **Beta**: {fund['beta']:.2f}")
    if fund.get("sector"):
        report.append(f"- **行业**: {fund['sector']}")
    report.append("")

    # 投资建议
    report.append("## 💡 投资建议")
    report.append(f"基于以上分析，{symbol} 当前评分 **{score}/100**，建议 **{signal}**。\n")

    # 风险提示
    report.append("---")
    report.append("*免责声明: 本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。*")

    return "\n".join(report)


def generate_watchlist_report(symbols: List[str]) -> str:
    """
    生成自选股监控报告

    Args:
        symbols: 自选股列表

    Returns:
        监控报告
    """
    report = []
    report.append("# 📋 自选股监控报告")
    report.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    # 市场情绪
    market = get_market_sentiment()
    report.append("## 🌍 市场情绪")
    report.append(f"恐惧贪婪指数: **{market['fear_greed_index']['value']}** ({market['fear_greed_index']['level_cn']})")
    report.append(f"VIX: **{market['vix']['value']:.1f}**\n")

    # 股票列表
    report.append("## 📊 股票概览")
    report.append("| 代码 | 价格 | 评分 | 信号 | RSI | 趋势 |")
    report.append("|------|------|------|------|-----|------|")

    for symbol in symbols:
        try:
            stock = analyze_stock(symbol)
            if "error" in stock:
                continue

            indicators = stock.get("technical_indicators", {})
            rsi_val = indicators.get("RSI", {}).get("value", "-")
            trend_info = stock.get("trend_analysis", {})
            trend_cn = {"uptrend": "↑", "downtrend": "↓", "sideways": "→"}.get(
                trend_info.get("trend", ""), "-"
            )

            report.append(
                f"| {symbol} | ${stock['price']:.2f} | "
                f"{stock['overall_score']:.0f} | {stock['signal_cn']} | "
                f"{rsi_val} | {trend_cn} |"
            )
        except Exception:
            continue

    report.append("")

    # 需要关注的股票
    report.append("## ⚡ 信号提醒")

    for symbol in symbols:
        try:
            stock = analyze_stock(symbol)
            if "error" in stock:
                continue

            signals = []

            # 检查RSI
            indicators = stock.get("technical_indicators", {})
            rsi = indicators.get("RSI", {})
            if rsi.get("oversold"):
                signals.append("RSI超卖")
            elif rsi.get("overbought"):
                signals.append("RSI超买")

            # 检查MACD
            macd = indicators.get("MACD", {})
            if macd.get("cross") == "golden_cross":
                signals.append("MACD金叉")
            elif macd.get("cross") == "death_cross":
                signals.append("MACD死叉")

            if signals:
                report.append(f"- **{symbol}**: {', '.join(signals)}")

        except Exception:
            continue

    return "\n".join(report)


def generate_portfolio_report(holdings: List[Dict]) -> str:
    """
    生成投资组合报告

    Args:
        holdings: 持仓列表

    Returns:
        组合报告
    """
    report = []
    report.append("# 💼 投资组合分析报告")
    report.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    # 风险分析
    risk = analyze_portfolio_risk(holdings)

    if "error" in risk:
        return f"# 投资组合分析报告\n\n❌ {risk['error']}"

    report.append("## 📊 组合概览")
    report.append(f"- **总市值**: ${risk['total_value']:,.2f}")
    report.append(f"- **风险等级**: {risk['risk_level_cn']} ({risk['risk_score']:.0f}/100)")
    report.append(f"- **组合Beta**: {risk['portfolio_beta']:.2f}")
    report.append(f"- **持仓数量**: {len(risk['holdings'])} 只\n")

    # 持仓明细
    report.append("## 📋 持仓明细")
    report.append("| 代码 | 权重 | 行业 | Beta |")
    report.append("|------|------|------|------|")

    for h in risk["holdings"]:
        report.append(f"| {h['symbol']} | {h['weight']:.1f}% | {h['sector']} | {h['beta']:.2f} |")

    report.append("")

    # 行业分布
    report.append("## 🏭 行业分布")
    for sector, weight in risk["sector_distribution"].items():
        bar = "█" * int(weight / 5)
        report.append(f"- {sector}: {bar} {weight:.1f}%")
    report.append("")

    # 风险指标
    report.append("## ⚠️ 风险指标")
    conc = risk["concentration"]
    report.append(f"- **集中度风险**: {conc['risk_level']}")
    report.append(f"- **最大单仓占比**: {conc['max_single_weight']:.1f}%")
    report.append(f"- **HHI指数**: {conc['herfindahl_index']:.3f}\n")

    # 建议
    report.append("## 💡 优化建议")
    for rec in risk["recommendations"]:
        report.append(f"- {rec}")

    return "\n".join(report)


def get_ai_recommendation(symbol: str, investment_style: str = "balanced") -> Dict:
    """
    获取AI综合投资建议

    Args:
        symbol: 股票代码
        investment_style: 投资风格 (aggressive/balanced/conservative)

    Returns:
        AI建议
    """
    # 获取综合分析
    stock = analyze_stock(symbol)
    if "error" in stock:
        return {"error": stock["error"]}

    sentiment = analyze_news_sentiment(symbol)
    ratings = get_analyst_ratings(symbol)

    # 综合评分
    score = stock["overall_score"]
    news_score = (sentiment["score"] + 1) * 50  # 转换到0-100
    analyst_score = ratings["consensus"]["score"] * 20  # 1-5 转换到 20-100

    # 根据投资风格调整权重
    if investment_style == "aggressive":
        weights = {"technical": 0.5, "news": 0.3, "analyst": 0.2}
        risk_tolerance = "high"
    elif investment_style == "conservative":
        weights = {"technical": 0.3, "news": 0.2, "analyst": 0.5}
        risk_tolerance = "low"
    else:  # balanced
        weights = {"technical": 0.4, "news": 0.3, "analyst": 0.3}
        risk_tolerance = "medium"

    final_score = (
        score * weights["technical"] +
        news_score * weights["news"] +
        analyst_score * weights["analyst"]
    )

    # 生成建议
    if final_score >= 75:
        action = "STRONG_BUY"
        action_cn = "强烈买入"
        confidence = "high"
    elif final_score >= 60:
        action = "BUY"
        action_cn = "买入"
        confidence = "medium-high"
    elif final_score >= 45:
        action = "HOLD"
        action_cn = "持有"
        confidence = "medium"
    elif final_score >= 30:
        action = "SELL"
        action_cn = "卖出"
        confidence = "medium"
    else:
        action = "STRONG_SELL"
        action_cn = "强烈卖出"
        confidence = "high"

    # 目标价
    current_price = stock["price"]
    analyst_target = ratings["price_targets"]["mean"]

    if action in ["STRONG_BUY", "BUY"]:
        target_price = max(current_price * 1.15, analyst_target)
        stop_loss = current_price * 0.92
    elif action in ["STRONG_SELL", "SELL"]:
        target_price = min(current_price * 0.85, analyst_target)
        stop_loss = current_price * 1.05
    else:
        target_price = analyst_target
        stop_loss = current_price * 0.95

    # 风险评估
    beta = stock.get("fundamentals", {}).get("beta", 1.0)
    if beta > 1.5:
        risk_level = "high"
        risk_level_cn = "高风险"
    elif beta > 1.0:
        risk_level = "medium"
        risk_level_cn = "中等风险"
    else:
        risk_level = "low"
        risk_level_cn = "低风险"

    # 生成分析理由
    reasoning = []

    if score >= 60:
        reasoning.append(f"技术面评分{score:.0f}分，显示积极信号")
    elif score <= 40:
        reasoning.append(f"技术面评分{score:.0f}分，显示消极信号")

    if sentiment["score"] > 0.3:
        reasoning.append("新闻情绪偏正面，市场关注度良好")
    elif sentiment["score"] < -0.3:
        reasoning.append("新闻情绪偏负面，需关注潜在风险")

    if ratings["consensus"]["score"] >= 4:
        reasoning.append(f"分析师普遍看好，共识评级{ratings['consensus']['rating_cn']}")
    elif ratings["consensus"]["score"] <= 2:
        reasoning.append(f"分析师评级偏谨慎，共识{ratings['consensus']['rating_cn']}")

    return {
        "symbol": symbol,
        "name": stock["name"],
        "current_price": current_price,
        "action": action,
        "action_cn": action_cn,
        "confidence": confidence,
        "target_price": round(target_price, 2),
        "stop_loss": round(stop_loss, 2),
        "upside_potential": round((target_price / current_price - 1) * 100, 1),
        "risk_level": risk_level,
        "risk_level_cn": risk_level_cn,
        "investment_style": investment_style,
        "scores": {
            "overall": round(final_score, 1),
            "technical": round(score, 1),
            "sentiment": round(news_score, 1),
            "analyst": round(analyst_score, 1)
        },
        "reasoning": reasoning,
        "analyst_consensus": ratings["consensus"]["rating_cn"],
        "analyst_target": analyst_target,
        "generated_at": datetime.now().isoformat()
    }
