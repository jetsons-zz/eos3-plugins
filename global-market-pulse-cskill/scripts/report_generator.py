"""
Report Generator - 市场报告生成器
生成适合高管阅读的简洁市场报告
"""

from datetime import datetime
from typing import Dict, List, Optional
from .market_client import MarketClient
from .market_analyzer import (
    analyze_market_sentiment,
    get_sector_performance,
    get_market_movers,
    get_quick_analysis
)


def format_change(change: float, with_sign: bool = True) -> str:
    """格式化涨跌幅"""
    if change > 0:
        return f"+{change:.2f}%" if with_sign else f"{change:.2f}%"
    else:
        return f"{change:.2f}%"


def format_price(price: float, currency: str = "USD") -> str:
    """格式化价格"""
    if currency in ["USD", "EUR", "GBP"]:
        return f"{price:,.2f}"
    elif currency in ["JPY", "KRW"]:
        return f"{price:,.0f}"
    else:
        return f"{price:,.2f}"


def get_direction_emoji(direction: str) -> str:
    """获取方向表情"""
    if direction == "up":
        return "🟢"
    elif direction == "down":
        return "🔴"
    else:
        return "⚪"


def format_market_table(data: List[Dict], columns: List[str] = None) -> str:
    """
    格式化为表格

    Args:
        data: 数据列表
        columns: 要显示的列

    Returns:
        Markdown 表格
    """
    if not data:
        return "暂无数据"

    if columns is None:
        columns = ["name", "price", "change_percent"]

    # 表头映射
    header_map = {
        "name": "名称",
        "price": "价格",
        "rate": "汇率",
        "change": "涨跌",
        "change_percent": "涨跌幅",
        "region": "地区",
        "direction": "方向"
    }

    # 构建表格
    headers = [header_map.get(col, col) for col in columns]
    header_row = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []
    for item in data:
        row_data = []
        for col in columns:
            if col == "change_percent":
                val = item.get(col, 0)
                emoji = get_direction_emoji(item.get('direction', 'flat'))
                row_data.append(f"{emoji} {format_change(val)}")
            elif col == "price" or col == "rate":
                val = item.get(col, 0)
                row_data.append(format_price(val, item.get('currency', 'USD')))
            elif col == "direction":
                row_data.append(get_direction_emoji(item.get(col, 'flat')))
            else:
                row_data.append(str(item.get(col, "")))
        rows.append("| " + " | ".join(row_data) + " |")

    return "\n".join([header_row, separator] + rows)


def generate_executive_summary(analysis: Dict = None) -> str:
    """
    生成高管摘要（一句话版本）

    Args:
        analysis: 市场分析数据，如果为None则自动获取

    Returns:
        简洁的市场摘要
    """
    if analysis is None:
        analysis = get_quick_analysis()

    sentiment = analysis.get('sentiment', {})
    movers = analysis.get('movers', {})
    market_status = analysis.get('market_status', {})

    # 构建摘要
    emoji = sentiment.get('emoji', '📊')
    sentiment_cn = sentiment.get('sentiment_cn', '中性')
    stats = sentiment.get('statistics', {})

    # 涨跌统计
    up = stats.get('up_count', 0)
    down = stats.get('down_count', 0)
    avg_change = stats.get('avg_change_percent', 0)

    # 最强/最弱
    gainers = movers.get('top_gainers', [])
    losers = movers.get('top_losers', [])

    best = gainers[0] if gainers else None
    worst = losers[0] if losers else None

    summary = f"{emoji} 全球市场{sentiment_cn}｜"
    summary += f"{up}涨{down}跌｜"
    summary += f"均幅{format_change(avg_change)}"

    if best:
        summary += f"｜最强{best['name']}{format_change(best['change_percent'])}"
    if worst:
        summary += f"｜最弱{worst['name']}{format_change(worst['change_percent'])}"

    return summary


def generate_market_brief(analysis: Dict = None) -> str:
    """
    生成市场简报（适合1分钟阅读）

    Args:
        analysis: 市场分析数据

    Returns:
        Markdown 格式的市场简报
    """
    if analysis is None:
        analysis = get_quick_analysis()

    now = datetime.now()
    report = []

    # 标题
    report.append(f"# 📊 全球市场快报")
    report.append(f"*{now.strftime('%Y年%m月%d日 %H:%M')}*\n")

    # 市场状态
    status = analysis.get('market_status', {})
    report.append(f"**市场状态**: {status.get('总结', '未知')}\n")

    # 市场情绪
    sentiment = analysis.get('sentiment', {})
    report.append(f"## {sentiment.get('emoji', '📊')} 市场情绪: {sentiment.get('sentiment_cn', '中性')}")
    report.append(f"{sentiment.get('description', '')}\n")

    stats = sentiment.get('statistics', {})
    report.append(f"- 上涨: {stats.get('up_count', 0)} 个指数")
    report.append(f"- 下跌: {stats.get('down_count', 0)} 个指数")
    report.append(f"- 平均涨跌: {format_change(stats.get('avg_change_percent', 0))}\n")

    # VIX
    vix = sentiment.get('vix')
    if vix:
        report.append(f"**恐慌指数VIX**: {vix['value']:.1f} ({vix['level']}) - {vix['description']}\n")

    # 涨跌榜
    movers = analysis.get('movers', {})
    gainers = movers.get('top_gainers', [])[:3]
    losers = movers.get('top_losers', [])[:3]

    if gainers:
        report.append("## 📈 涨幅榜")
        for i, g in enumerate(gainers, 1):
            report.append(f"{i}. **{g['name']}** ({g['region']}) {format_change(g['change_percent'])}")
        report.append("")

    if losers:
        report.append("## 📉 跌幅榜")
        for i, l in enumerate(losers, 1):
            report.append(f"{i}. **{l['name']}** ({l['region']}) {format_change(l['change_percent'])}")
        report.append("")

    # 汇率
    currencies = analysis.get('currencies', [])
    if currencies:
        report.append("## 💱 主要汇率")
        for c in currencies[:4]:
            emoji = get_direction_emoji(c.get('direction'))
            report.append(f"- {c['name']}: {c['rate']:.4f} {emoji} {format_change(c['change_percent'])}")
        report.append("")

    # 大宗商品
    commodities = analysis.get('commodities', [])
    if commodities:
        report.append("## 🛢️ 大宗商品")
        for c in commodities:
            emoji = get_direction_emoji(c.get('direction'))
            report.append(f"- {c['name']}: ${c['price']:.2f} {emoji} {format_change(c['change_percent'])}")
        report.append("")

    # 加密货币
    crypto = analysis.get('crypto', [])
    if crypto:
        report.append("## ₿ 加密货币")
        for c in crypto:
            emoji = get_direction_emoji(c.get('direction'))
            report.append(f"- {c['name']}: ${c['price']:,.2f} {emoji} {format_change(c['change_percent'])}")
        report.append("")

    return "\n".join(report)


def generate_detailed_report(analysis: Dict = None) -> str:
    """
    生成详细市场报告（适合5分钟阅读）

    Args:
        analysis: 市场分析数据

    Returns:
        详细的 Markdown 报告
    """
    if analysis is None:
        analysis = get_quick_analysis()

    now = datetime.now()
    report = []

    # 标题
    report.append("# 📊 全球市场深度分析报告")
    report.append(f"*生成时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}*\n")

    # 执行摘要
    report.append("## 📌 执行摘要")
    report.append(generate_executive_summary(analysis))
    report.append("")

    # 市场情绪分析
    sentiment = analysis.get('sentiment', {})
    report.append("## 🎯 市场情绪分析")
    report.append(f"**整体判断**: {sentiment.get('sentiment_cn', '中性')} {sentiment.get('emoji', '')}")
    report.append(f"\n{sentiment.get('description', '')}\n")

    stats = sentiment.get('statistics', {})
    report.append("| 指标 | 数值 |")
    report.append("| --- | --- |")
    report.append(f"| 上涨指数 | {stats.get('up_count', 0)} |")
    report.append(f"| 下跌指数 | {stats.get('down_count', 0)} |")
    report.append(f"| 上涨占比 | {stats.get('up_ratio', 0)}% |")
    report.append(f"| 平均涨跌 | {format_change(stats.get('avg_change_percent', 0))} |")
    report.append("")

    # 各地区表现
    sector_perf = analysis.get('sector_performance', {})
    by_region = sector_perf.get('by_region', {})

    report.append("## 🌍 各地区表现")
    report.append("| 地区 | 平均涨跌 | 最强指数 | 最弱指数 |")
    report.append("| --- | --- | --- | --- |")

    for region in sector_perf.get('ranking', []):
        perf = by_region.get(region, {})
        best = perf.get('best_performer', {})
        worst = perf.get('worst_performer', {})
        emoji = get_direction_emoji(perf.get('direction', 'flat'))
        report.append(
            f"| {region} | {emoji} {format_change(perf.get('avg_change_percent', 0))} | "
            f"{best.get('name', '-')} | {worst.get('name', '-')} |"
        )
    report.append("")

    # 各区域详细指数
    indices = analysis.get('indices', {})
    for region in ['美国', '欧洲', '中国', '日本', '香港', '韩国', '澳大利亚', '印度']:
        if region in indices and indices[region]:
            report.append(f"### {region}")
            report.append(format_market_table(indices[region], ['name', 'price', 'change_percent']))
            report.append("")

    return "\n".join(report)


def generate_regional_report(region: str, analysis: Dict = None) -> str:
    """
    生成特定地区的市场报告

    Args:
        region: 地区名称（美国、欧洲、中国等）
        analysis: 市场分析数据

    Returns:
        地区报告
    """
    if analysis is None:
        analysis = get_quick_analysis()

    indices = analysis.get('indices', {})
    region_data = indices.get(region, [])

    if not region_data:
        return f"未找到{region}市场数据"

    report = []
    report.append(f"# 🌏 {region}市场报告")
    report.append(f"*{datetime.now().strftime('%Y年%m月%d日 %H:%M')}*\n")

    # 概览
    changes = [idx.get('change_percent', 0) for idx in region_data]
    avg_change = sum(changes) / len(changes) if changes else 0

    if avg_change > 0.5:
        mood = "📈 整体上涨"
    elif avg_change < -0.5:
        mood = "📉 整体下跌"
    else:
        mood = "➡️ 走势平稳"

    report.append(f"**{mood}** | 平均涨跌: {format_change(avg_change)}\n")

    # 详细数据
    report.append(format_market_table(region_data, ['name', 'price', 'change_percent']))

    return "\n".join(report)
