"""
Risk Analyzer - 风险分析模块
分析投资组合风险和分散度
"""

from datetime import datetime
from typing import Dict, List
import math


def calculate_portfolio_risk(holdings: List[Dict], values: List[Dict]) -> Dict:
    """
    计算投资组合风险

    Args:
        holdings: 持仓列表
        values: 当前价值列表

    Returns:
        风险分析结果
    """
    if not values:
        return {"error": "无持仓数据"}

    total_value = sum(v.get("value", 0) for v in values)
    if total_value == 0:
        return {"error": "投资组合总价值为0"}

    # 计算各资产权重
    weights = []
    for v in values:
        weight = v.get("value", 0) / total_value
        weights.append({
            "symbol": v.get("symbol"),
            "type": v.get("type", "stock"),
            "value": v.get("value", 0),
            "weight": round(weight * 100, 2)
        })

    # 按权重排序
    weights.sort(key=lambda x: x["weight"], reverse=True)

    # 计算集中度风险
    top_weight = weights[0]["weight"] if weights else 0
    top_3_weight = sum(w["weight"] for w in weights[:3])

    # 风险评级
    if top_weight > 50:
        concentration_risk = "高"
        concentration_score = 30
    elif top_weight > 30:
        concentration_risk = "中"
        concentration_score = 60
    else:
        concentration_risk = "低"
        concentration_score = 90

    # 资产类别分布
    type_distribution = {}
    for w in weights:
        t = w["type"]
        if t not in type_distribution:
            type_distribution[t] = 0
        type_distribution[t] += w["weight"]

    # 多样化评分
    num_types = len(type_distribution)
    if num_types >= 4:
        diversification_score = 90
    elif num_types >= 3:
        diversification_score = 70
    elif num_types >= 2:
        diversification_score = 50
    else:
        diversification_score = 30

    # 综合风险评分
    overall_score = (concentration_score + diversification_score) / 2

    if overall_score >= 80:
        risk_level = "低风险"
        risk_emoji = "🟢"
    elif overall_score >= 60:
        risk_level = "中低风险"
        risk_emoji = "🟡"
    elif overall_score >= 40:
        risk_level = "中高风险"
        risk_emoji = "🟠"
    else:
        risk_level = "高风险"
        risk_emoji = "🔴"

    return {
        "overall_score": round(overall_score),
        "risk_level": risk_level,
        "risk_emoji": risk_emoji,
        "concentration": {
            "risk": concentration_risk,
            "score": concentration_score,
            "top_holding_weight": top_weight,
            "top_3_weight": top_3_weight
        },
        "diversification": {
            "score": diversification_score,
            "asset_types": num_types,
            "type_distribution": type_distribution
        },
        "weight_breakdown": weights[:10],  # 前10大持仓
        "analyzed_at": datetime.now().isoformat()
    }


def get_diversification_score(holdings: List[Dict]) -> Dict:
    """
    计算分散度评分

    Args:
        holdings: 持仓列表

    Returns:
        分散度评分
    """
    if not holdings:
        return {"score": 0, "message": "无持仓"}

    # 统计资产类型
    types = set(h.get("type", "stock") for h in holdings)
    num_holdings = len(holdings)

    # 评分规则
    type_score = min(len(types) * 20, 40)  # 最多40分
    count_score = min(num_holdings * 5, 30)  # 最多30分

    # 检查是否有不同地区
    regions = set()
    for h in holdings:
        symbol = h.get("symbol", "")
        if ".HK" in symbol:
            regions.add("HK")
        elif ".SS" in symbol or ".SZ" in symbol:
            regions.add("CN")
        elif symbol.endswith("-USD"):
            regions.add("CRYPTO")
        else:
            regions.add("US")

    region_score = min(len(regions) * 10, 30)  # 最多30分

    total_score = type_score + count_score + region_score

    if total_score >= 80:
        grade = "优秀"
        message = "投资组合分散度良好，风险分布合理"
    elif total_score >= 60:
        grade = "良好"
        message = "投资组合有一定分散度，可考虑增加资产类型"
    elif total_score >= 40:
        grade = "一般"
        message = "投资组合集中度较高，建议增加分散投资"
    else:
        grade = "较差"
        message = "投资组合过于集中，风险较高"

    return {
        "score": total_score,
        "grade": grade,
        "message": message,
        "breakdown": {
            "asset_types": list(types),
            "type_score": type_score,
            "holdings_count": num_holdings,
            "count_score": count_score,
            "regions": list(regions),
            "region_score": region_score
        }
    }


def get_rebalance_suggestions(holdings: List[Dict], values: List[Dict]) -> List[Dict]:
    """
    获取再平衡建议

    Args:
        holdings: 持仓列表
        values: 当前价值列表

    Returns:
        再平衡建议
    """
    suggestions = []

    if not values:
        return [{"type": "warning", "message": "无法获取持仓价值"}]

    total_value = sum(v.get("value", 0) for v in values)
    if total_value == 0:
        return [{"type": "warning", "message": "投资组合总价值为0"}]

    # 检查单一资产过重
    for v in values:
        weight = v.get("value", 0) / total_value * 100
        if weight > 40:
            suggestions.append({
                "type": "reduce",
                "priority": "high",
                "asset": v.get("symbol"),
                "current_weight": round(weight, 1),
                "target_weight": 25,
                "message": f"{v.get('symbol')} 占比过高 ({weight:.1f}%)，建议减持至25%以下"
            })
        elif weight > 30:
            suggestions.append({
                "type": "reduce",
                "priority": "medium",
                "asset": v.get("symbol"),
                "current_weight": round(weight, 1),
                "target_weight": 20,
                "message": f"{v.get('symbol')} 占比较高 ({weight:.1f}%)，可考虑适当减持"
            })

    # 检查资产类型分布
    type_values = {}
    for v in values:
        t = v.get("type", "stock")
        if t not in type_values:
            type_values[t] = 0
        type_values[t] += v.get("value", 0)

    # 建议增加缺失的资产类型
    ideal_types = {"stock", "crypto", "commodity"}
    current_types = set(type_values.keys())
    missing = ideal_types - current_types

    for m in missing:
        type_names = {"stock": "股票", "crypto": "加密货币", "commodity": "大宗商品"}
        suggestions.append({
            "type": "add",
            "priority": "low",
            "asset_type": m,
            "message": f"建议配置一些{type_names.get(m, m)}以增加分散度"
        })

    # 如果没有建议
    if not suggestions:
        suggestions.append({
            "type": "ok",
            "priority": "info",
            "message": "投资组合配置合理，暂无调整建议"
        })

    return suggestions
