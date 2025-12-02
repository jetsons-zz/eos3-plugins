"""
Report Generator - 报告生成模块
生成投资组合报告
"""

from datetime import datetime
from typing import Dict, List
from .asset_tracker import get_multi_asset_prices, get_market_overview
from .portfolio_manager import get_portfolio_value, get_portfolio_performance, SAMPLE_PORTFOLIO
from .risk_analyzer import calculate_portfolio_risk, get_diversification_score, get_rebalance_suggestions


def generate_wealth_snapshot(holdings: List[Dict] = None) -> str:
    """
    生成财富快照（一句话版本）

    Args:
        holdings: 持仓列表

    Returns:
        简洁快照
    """
    if holdings is None:
        holdings = SAMPLE_PORTFOLIO["holdings"]

    values = get_multi_asset_prices(holdings)
    total = sum(v.get("value", 0) for v in values)
    total_cost = sum(v.get("cost_basis", 0) for v in values)
    gain = total - total_cost
    gain_pct = (gain / total_cost * 100) if total_cost else 0

    emoji = "📈" if gain > 0 else "📉" if gain < 0 else "➡️"

    return f"{emoji} 总资产: ¥{total:,.0f} | 盈亏: {gain:+,.0f} ({gain_pct:+.1f}%) | 持仓: {len(holdings)}项"


def generate_performance_summary(holdings: List[Dict] = None, period: str = "1mo") -> str:
    """
    生成表现摘要

    Args:
        holdings: 持仓列表
        period: 时间周期

    Returns:
        表现摘要
    """
    if holdings is None:
        holdings = SAMPLE_PORTFOLIO["holdings"]

    perf = get_portfolio_performance(holdings, period)

    period_names = {
        "1d": "今日", "5d": "本周", "1mo": "本月", "3mo": "本季度", "6mo": "半年", "1y": "今年"
    }

    report = []
    report.append(f"📊 {period_names.get(period, period)}投资表现")
    report.append(f"总收益: {perf['total_return']:+.2f}%")
    report.append(f"盈亏: ¥{perf['total_gain_loss']:+,.0f}")

    if perf.get("top_performers"):
        best = perf["top_performers"][0]
        report.append(f"最佳: {best['symbol']} ({best['period_return']:+.1f}%)")

    return " | ".join(report)


def generate_portfolio_report(holdings: List[Dict] = None) -> str:
    """
    生成完整投资组合报告

    Args:
        holdings: 持仓列表

    Returns:
        Markdown格式报告
    """
    if holdings is None:
        holdings = SAMPLE_PORTFOLIO["holdings"]

    # 获取数据
    values = get_multi_asset_prices(holdings)
    risk = calculate_portfolio_risk(holdings, values)
    diversification = get_diversification_score(holdings)
    suggestions = get_rebalance_suggestions(holdings, values)
    perf = get_portfolio_performance(holdings, "1mo")

    # 计算总值
    total_value = sum(v.get("value", 0) for v in values)
    total_cost = sum(v.get("cost_basis", 0) for v in values)
    total_gain = total_value - total_cost
    total_gain_pct = (total_gain / total_cost * 100) if total_cost else 0

    report = []

    # 标题
    report.append("=" * 50)
    report.append("📊 投资组合分析报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 50)
    report.append("")

    # 总览
    report.append("## 💰 资产总览")
    report.append(f"**总资产**: ¥{total_value:,.2f}")
    report.append(f"**总成本**: ¥{total_cost:,.2f}")

    emoji = "🟢" if total_gain > 0 else "🔴" if total_gain < 0 else "⚪"
    report.append(f"**总盈亏**: {emoji} ¥{total_gain:+,.2f} ({total_gain_pct:+.2f}%)")
    report.append(f"**持仓数量**: {len(holdings)} 项")
    report.append("")

    # 风险评估
    report.append("## 🎯 风险评估")
    report.append(f"**风险等级**: {risk.get('risk_emoji', '')} {risk.get('risk_level', 'N/A')}")
    report.append(f"**综合评分**: {risk.get('overall_score', 0)}/100")
    report.append(f"**集中度风险**: {risk.get('concentration', {}).get('risk', 'N/A')}")
    report.append(f"**分散度评分**: {diversification.get('score', 0)}/100 ({diversification.get('grade', '')})")
    report.append("")

    # 持仓明细
    report.append("## 📋 持仓明细")
    report.append("| 资产 | 类型 | 数量 | 现价 | 市值 | 盈亏 |")
    report.append("|------|------|------|------|------|------|")

    for v in sorted(values, key=lambda x: x.get("value", 0), reverse=True):
        symbol = v.get("symbol", "")
        atype = {"stock": "股票", "crypto": "加密", "commodity": "商品"}.get(v.get("type", ""), "其他")
        qty = v.get("quantity", 0)
        price = v.get("price", 0)
        value = v.get("value", 0)
        pl = v.get("profit_loss", 0)
        pl_pct = v.get("profit_loss_percent", 0)

        pl_str = f"{pl:+,.0f} ({pl_pct:+.1f}%)" if pl != 0 else "-"
        report.append(f"| {symbol} | {atype} | {qty} | ${price:,.2f} | ¥{value:,.0f} | {pl_str} |")

    report.append("")

    # 资产配置
    report.append("## 📊 资产配置")
    type_dist = risk.get("diversification", {}).get("type_distribution", {})
    for t, pct in type_dist.items():
        type_name = {"stock": "股票", "crypto": "加密货币", "commodity": "大宗商品"}.get(t, t)
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        report.append(f"{type_name}: {bar} {pct:.1f}%")
    report.append("")

    # 近期表现
    report.append("## 📈 近期表现 (本月)")
    report.append(f"**月度收益**: {perf.get('total_return', 0):+.2f}%")
    if perf.get("top_performers"):
        report.append("**表现最佳**:")
        for p in perf["top_performers"][:3]:
            report.append(f"  - {p['symbol']}: {p['period_return']:+.1f}%")
    report.append("")

    # 调仓建议
    report.append("## 💡 调仓建议")
    for s in suggestions:
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢", "info": "ℹ️"}.get(s.get("priority", ""), "")
        report.append(f"{priority_emoji} {s.get('message', '')}")
    report.append("")

    report.append("=" * 50)

    return "\n".join(report)


def generate_market_context_report() -> str:
    """生成市场背景报告"""
    overview = get_market_overview()

    report = []
    report.append("## 🌍 市场背景")

    # 指数
    report.append("### 主要指数")
    for idx in overview.get("indices", []):
        emoji = "🟢" if idx.get("direction") == "up" else "🔴"
        report.append(f"{emoji} {idx.get('name', '')}: {idx.get('price', 0):,.2f} ({idx.get('change_percent', 0):+.2f}%)")

    # 商品
    report.append("### 大宗商品")
    for c in overview.get("commodities", []):
        emoji = "🟢" if c.get("direction") == "up" else "🔴"
        report.append(f"{emoji} {c.get('name', '')}: ${c.get('price', 0):,.2f} ({c.get('change_percent', 0):+.2f}%)")

    # 加密货币
    report.append("### 加密货币")
    for crypto in overview.get("crypto", []):
        emoji = "🟢" if crypto.get("direction") == "up" else "🔴"
        report.append(f"{emoji} {crypto.get('name', '')}: ${crypto.get('price', 0):,.2f} ({crypto.get('change_percent', 0):+.2f}%)")

    return "\n".join(report)
