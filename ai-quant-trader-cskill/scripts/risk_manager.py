"""
Risk Manager - 风险管理模块
仓位管理、止损止盈、组合风险分析
"""

import math
from datetime import datetime
from typing import Dict, List, Optional

from .market_analyzer import MarketAnalyzer, calculate_sma


class RiskManager:
    """风险管理器"""

    def __init__(self):
        self.analyzer = MarketAnalyzer()


def calculate_position_size(
    capital: float,
    risk_per_trade: float = 0.02,
    entry_price: float = 0,
    stop_loss: float = 0
) -> Dict:
    """
    计算最优仓位大小

    Args:
        capital: 总资金
        risk_per_trade: 单笔风险比例 (默认2%)
        entry_price: 入场价格
        stop_loss: 止损价格

    Returns:
        仓位建议
    """
    if entry_price <= 0 or stop_loss <= 0:
        return {"error": "请提供有效的入场价和止损价"}

    if stop_loss >= entry_price:
        return {"error": "止损价应低于入场价（做多情况）"}

    # 计算每股风险
    risk_per_share = entry_price - stop_loss
    risk_percent = risk_per_share / entry_price * 100

    # 计算最大可承受亏损
    max_loss = capital * risk_per_trade

    # 计算股数
    shares = int(max_loss / risk_per_share)

    # 计算所需资金
    position_value = shares * entry_price
    position_percent = position_value / capital * 100

    # 凯利公式优化（假设胜率55%，盈亏比2:1）
    win_rate = 0.55
    win_loss_ratio = 2.0
    kelly_fraction = win_rate - (1 - win_rate) / win_loss_ratio
    kelly_position = capital * kelly_fraction

    # 半凯利（更保守）
    half_kelly_shares = int(kelly_position * 0.5 / entry_price)

    return {
        "recommended_shares": shares,
        "position_value": round(position_value, 2),
        "position_percent": round(position_percent, 1),
        "risk_per_share": round(risk_per_share, 2),
        "risk_percent": round(risk_percent, 2),
        "max_loss": round(max_loss, 2),
        "kelly_analysis": {
            "full_kelly_shares": int(kelly_position / entry_price),
            "half_kelly_shares": half_kelly_shares,
            "kelly_fraction": round(kelly_fraction, 3)
        },
        "recommendations": [
            f"建议买入 {shares} 股",
            f"仓位占比 {position_percent:.1f}%",
            f"最大亏损 ${max_loss:,.0f} ({risk_per_trade*100:.1f}%)",
            f"保守建议（半凯利）: {half_kelly_shares} 股"
        ]
    }


def calculate_var(
    holdings: List[Dict],
    confidence: float = 0.95,
    days: int = 1
) -> Dict:
    """
    计算投资组合VaR (Value at Risk)

    Args:
        holdings: 持仓列表 [{"symbol": "AAPL", "shares": 100, "price": 150}, ...]
        confidence: 置信度 (默认95%)
        days: 持有天数

    Returns:
        VaR分析结果
    """
    if not holdings:
        return {"error": "请提供持仓信息"}

    analyzer = MarketAnalyzer()

    # 计算组合价值和各资产波动率
    total_value = 0
    asset_data = []

    for h in holdings:
        symbol = h.get("symbol", "")
        shares = h.get("shares", 0)
        price = h.get("price", 0)

        if not price:
            data = analyzer.get_stock_data(symbol)
            price = data.get("price", 100) if data else 100

        value = shares * price
        total_value += value

        # 获取历史数据计算波动率
        data = analyzer.get_stock_data(symbol)
        if data and "history" in data:
            prices = data["history"]["close"]
            if len(prices) >= 20:
                returns = [(prices[i] / prices[i-1] - 1) for i in range(1, len(prices))]
                volatility = (sum(r**2 for r in returns) / len(returns)) ** 0.5 * math.sqrt(252)
            else:
                volatility = 0.25  # 默认25%年化波动率
        else:
            volatility = 0.25

        asset_data.append({
            "symbol": symbol,
            "value": value,
            "weight": 0,  # 稍后计算
            "volatility": volatility
        })

    # 计算权重
    for a in asset_data:
        a["weight"] = a["value"] / total_value if total_value > 0 else 0

    # 计算组合波动率（简化：假设资产不相关）
    portfolio_var = sum(a["weight"]**2 * a["volatility"]**2 for a in asset_data)
    portfolio_volatility = math.sqrt(portfolio_var)

    # Z值
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
    z = z_scores.get(confidence, 1.65)

    # 日度VaR
    daily_var = total_value * portfolio_volatility * z / math.sqrt(252)

    # N天VaR
    n_day_var = daily_var * math.sqrt(days)

    # VaR百分比
    var_percent = n_day_var / total_value * 100

    return {
        "total_value": round(total_value, 2),
        "confidence": confidence,
        "holding_days": days,
        "var_value": round(n_day_var, 2),
        "var_percent": round(var_percent, 2),
        "daily_var": round(daily_var, 2),
        "portfolio_volatility": round(portfolio_volatility * 100, 2),
        "asset_breakdown": [
            {
                "symbol": a["symbol"],
                "weight": round(a["weight"] * 100, 1),
                "volatility": round(a["volatility"] * 100, 1)
            }
            for a in asset_data
        ],
        "interpretation": _get_var_interpretation(var_percent, confidence),
        "recommendations": _get_var_recommendations(var_percent)
    }


def _get_var_interpretation(var_percent: float, confidence: float) -> str:
    """VaR解读"""
    return (
        f"在{confidence*100:.0f}%置信度下，预计最大损失为投资组合价值的{var_percent:.1f}%。"
        f"即有{(1-confidence)*100:.0f}%的概率损失会超过这个数值。"
    )


def _get_var_recommendations(var_percent: float) -> List[str]:
    """VaR建议"""
    recommendations = []

    if var_percent > 10:
        recommendations.append("VaR较高，建议降低仓位或增加对冲")
        recommendations.append("考虑增加低波动资产配置")
    elif var_percent > 5:
        recommendations.append("VaR处于中等水平，注意风险控制")
    else:
        recommendations.append("VaR较低，风险可控")

    return recommendations


def set_stop_loss(
    symbol: str,
    entry_price: float,
    method: str = "atr"
) -> Dict:
    """
    智能止损建议

    Args:
        symbol: 股票代码
        entry_price: 入场价格
        method: 止损方法 (atr/percent/support)

    Returns:
        止损建议
    """
    analyzer = MarketAnalyzer()
    data = analyzer.get_stock_data(symbol)

    if not data or "history" not in data:
        return {"error": f"无法获取 {symbol} 数据"}

    prices = data["history"]["close"]
    highs = data["history"]["high"]
    lows = data["history"]["low"]

    stop_prices = {}
    recommendations = []

    # 1. ATR止损
    if len(prices) >= 14:
        tr_list = []
        for i in range(1, len(prices)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - prices[i-1]),
                abs(lows[i] - prices[i-1])
            )
            tr_list.append(tr)

        atr = sum(tr_list[-14:]) / 14
        atr_stop = entry_price - 2 * atr  # 2倍ATR止损

        stop_prices["atr"] = round(atr_stop, 2)
        recommendations.append(f"ATR止损: ${atr_stop:.2f} (2倍ATR)")

    # 2. 百分比止损
    percent_stops = {
        "conservative": entry_price * 0.95,  # 5%
        "moderate": entry_price * 0.92,      # 8%
        "aggressive": entry_price * 0.90     # 10%
    }
    stop_prices["percent"] = {k: round(v, 2) for k, v in percent_stops.items()}
    recommendations.append(f"百分比止损: 保守${percent_stops['conservative']:.2f}(5%), "
                          f"中等${percent_stops['moderate']:.2f}(8%), "
                          f"激进${percent_stops['aggressive']:.2f}(10%)")

    # 3. 支撑位止损
    if len(lows) >= 20:
        recent_lows = sorted(lows[-20:])[:3]
        support_levels = [l for l in recent_lows if l < entry_price]
        if support_levels:
            support_stop = max(support_levels) * 0.99  # 支撑位下方1%
            stop_prices["support"] = round(support_stop, 2)
            recommendations.append(f"支撑位止损: ${support_stop:.2f}")

    # 选择推荐止损
    if method == "atr" and "atr" in stop_prices:
        recommended = stop_prices["atr"]
    elif method == "percent":
        recommended = stop_prices["percent"]["moderate"]
    elif method == "support" and "support" in stop_prices:
        recommended = stop_prices["support"]
    else:
        recommended = stop_prices.get("atr", entry_price * 0.92)

    # 计算风险回报比
    risk = entry_price - recommended
    risk_percent = risk / entry_price * 100

    return {
        "symbol": symbol,
        "entry_price": entry_price,
        "stop_price": recommended,
        "method": method,
        "risk_amount": round(risk, 2),
        "risk_percent": round(risk_percent, 2),
        "all_stop_levels": stop_prices,
        "recommendations": recommendations,
        "take_profit_suggestions": {
            "1_to_1": round(entry_price + risk, 2),
            "2_to_1": round(entry_price + 2 * risk, 2),
            "3_to_1": round(entry_price + 3 * risk, 2)
        }
    }


def analyze_portfolio_risk(holdings: List[Dict]) -> Dict:
    """
    分析投资组合风险

    Args:
        holdings: 持仓列表

    Returns:
        风险分析结果
    """
    if not holdings:
        return {"error": "请提供持仓信息"}

    analyzer = MarketAnalyzer()

    # 收集数据
    total_value = 0
    assets = []
    sectors = {}
    betas = []

    for h in holdings:
        symbol = h.get("symbol", "")
        shares = h.get("shares", 0)
        price = h.get("price", 0)

        data = analyzer.get_stock_data(symbol)
        if data:
            if not price:
                price = data.get("price", 100)

            value = shares * price
            total_value += value

            sector = data.get("sector", "Unknown")
            beta = data.get("beta", 1.0)

            assets.append({
                "symbol": symbol,
                "value": value,
                "sector": sector,
                "beta": beta
            })

            sectors[sector] = sectors.get(sector, 0) + value
            betas.append((beta, value))

    if not assets:
        return {"error": "无法获取持仓数据"}

    # 计算权重和集中度
    for a in assets:
        a["weight"] = a["value"] / total_value * 100

    # 计算组合Beta
    portfolio_beta = sum(b * v for b, v in betas) / total_value if total_value > 0 else 1.0

    # 计算集中度（Herfindahl指数）
    weights = [a["weight"] / 100 for a in assets]
    herfindahl = sum(w**2 for w in weights)
    concentration_risk = "high" if herfindahl > 0.3 else "medium" if herfindahl > 0.15 else "low"

    # 行业分布
    sector_distribution = {k: round(v / total_value * 100, 1) for k, v in sectors.items()}

    # 最大持仓占比
    max_weight = max(a["weight"] for a in assets)
    single_stock_risk = "high" if max_weight > 30 else "medium" if max_weight > 20 else "low"

    # 风险评分
    risk_score = 50

    # Beta风险
    if portfolio_beta > 1.5:
        risk_score += 20
    elif portfolio_beta > 1.2:
        risk_score += 10
    elif portfolio_beta < 0.8:
        risk_score -= 10

    # 集中度风险
    if concentration_risk == "high":
        risk_score += 15
    elif concentration_risk == "medium":
        risk_score += 5

    # 单一股票风险
    if single_stock_risk == "high":
        risk_score += 15

    risk_score = min(100, max(0, risk_score))

    # 风险等级
    if risk_score >= 70:
        risk_level = "high"
        risk_level_cn = "高风险"
    elif risk_score >= 40:
        risk_level = "medium"
        risk_level_cn = "中等风险"
    else:
        risk_level = "low"
        risk_level_cn = "低风险"

    return {
        "total_value": round(total_value, 2),
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "risk_level_cn": risk_level_cn,
        "portfolio_beta": round(portfolio_beta, 2),
        "concentration": {
            "herfindahl_index": round(herfindahl, 3),
            "risk_level": concentration_risk,
            "max_single_weight": round(max_weight, 1)
        },
        "sector_distribution": sector_distribution,
        "holdings": [
            {
                "symbol": a["symbol"],
                "weight": round(a["weight"], 1),
                "sector": a["sector"],
                "beta": a["beta"]
            }
            for a in sorted(assets, key=lambda x: x["weight"], reverse=True)
        ],
        "recommendations": _generate_risk_recommendations(
            portfolio_beta, concentration_risk, single_stock_risk, sector_distribution
        )
    }


def _generate_risk_recommendations(
    beta: float,
    concentration: str,
    single_stock: str,
    sectors: Dict
) -> List[str]:
    """生成风险建议"""
    recommendations = []

    if beta > 1.3:
        recommendations.append("组合Beta较高，市场下跌时波动会放大，考虑增加低Beta资产")
    elif beta < 0.7:
        recommendations.append("组合Beta较低，牛市可能跑输大盘，可适当增加成长股")

    if concentration == "high":
        recommendations.append("持仓集中度过高，建议增加持仓数量以分散风险")

    if single_stock == "high":
        recommendations.append("单一股票占比过高，建议减仓至20%以下")

    # 行业集中度
    if sectors:
        max_sector = max(sectors.values())
        if max_sector > 50:
            recommendations.append(f"行业集中度过高（{max_sector:.0f}%），建议增加其他行业配置")

    if not recommendations:
        recommendations.append("当前组合风险配置较为合理")

    return recommendations
