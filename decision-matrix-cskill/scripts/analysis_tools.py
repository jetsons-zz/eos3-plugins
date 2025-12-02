"""
Analysis Tools Module - 分析工具模块
敏感性分析、优劣势分析、风险评估
"""

from datetime import datetime
from typing import Dict, List, Optional
from .decision_framer import DECISION_STORE
from .scoring_engine import calculate_weighted_scores


def sensitivity_analysis(decision_id: str, criterion_name: str, weight_range: List[float] = None) -> Dict:
    """
    敏感性分析 - 分析标准权重变化对结果的影响

    Args:
        decision_id: 决策ID
        criterion_name: 要分析的标准名称
        weight_range: 权重变化范围 [min, max]

    Returns:
        敏感性分析结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    if weight_range is None:
        weight_range = [0.05, 0.50]

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    # 找到目标标准
    target_criterion = None
    for c in criteria:
        if c["name"] == criterion_name:
            target_criterion = c
            break

    if not target_criterion:
        return {
            "status": "error",
            "message": f"未找到标准: {criterion_name}"
        }

    original_weight = target_criterion["weight"]
    results = []

    # 测试不同权重
    test_weights = [
        weight_range[0],
        (weight_range[0] + original_weight) / 2,
        original_weight,
        (original_weight + weight_range[1]) / 2,
        weight_range[1]
    ]

    for test_weight in test_weights:
        # 临时修改权重
        target_criterion["weight"] = test_weight

        # 归一化其他权重
        other_total = sum(c["weight"] for c in criteria if c["name"] != criterion_name)
        scale = (1 - test_weight) / other_total if other_total > 0 else 0

        temp_weights = {}
        for c in criteria:
            if c["name"] != criterion_name:
                temp_weights[c["name"]] = c["weight"]
                c["weight"] = c["weight"] * scale

        # 计算结果
        weighted = calculate_weighted_scores(decision_id)

        if weighted.get("status") == "success":
            rankings = weighted.get("results", [])
            winner = rankings[0]["option_name"] if rankings else None

            results.append({
                "weight": round(test_weight, 2),
                "winner": winner,
                "rankings": [r["option_name"] for r in rankings[:3]]
            })

        # 恢复权重
        target_criterion["weight"] = original_weight
        for c in criteria:
            if c["name"] in temp_weights:
                c["weight"] = temp_weights[c["name"]]

    # 分析结果变化
    winners = [r["winner"] for r in results]
    is_stable = len(set(winners)) == 1

    return {
        "status": "success",
        "criterion_analyzed": criterion_name,
        "original_weight": original_weight,
        "weight_range_tested": weight_range,
        "results": results,
        "is_stable": is_stable,
        "stability_assessment": "结果稳定，对该标准不敏感" if is_stable else "结果不稳定，对该标准敏感",
        "recommendation": f"当前权重 {original_weight:.2f} 是否合理需要根据实际重要性判断"
    }


def pros_cons_analysis(decision_id: str) -> Dict:
    """
    优劣势对比分析

    Args:
        decision_id: 决策ID

    Returns:
        优劣势分析结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])
    criteria = decision.get("criteria", [])
    scores = decision.get("scores", {})

    if not options or not scores:
        return {
            "status": "error",
            "message": "需要先添加选项和评分"
        }

    analysis = []

    for option in options:
        opt_id = option["id"]
        opt_name = option["name"]

        if opt_id not in scores:
            continue

        opt_scores = scores[opt_id]

        # 找出优势和劣势
        strengths = []
        weaknesses = []

        for criterion_name, score in opt_scores.items():
            # 找到标准类型
            criterion = next((c for c in criteria if c["name"] == criterion_name), None)
            if not criterion:
                continue

            crit_type = criterion.get("type", "benefit")

            if crit_type == "benefit":
                if score >= 8:
                    strengths.append({"criterion": criterion_name, "score": score, "note": "表现优秀"})
                elif score <= 4:
                    weaknesses.append({"criterion": criterion_name, "score": score, "note": "需要改进"})
            else:  # cost
                if score <= 3:  # 低成本是好事
                    strengths.append({"criterion": criterion_name, "score": score, "note": "成本/风险低"})
                elif score >= 7:  # 高成本是坏事
                    weaknesses.append({"criterion": criterion_name, "score": score, "note": "成本/风险高"})

        # 也包含选项自带的pros/cons
        option_pros = option.get("pros", [])
        option_cons = option.get("cons", [])

        analysis.append({
            "option_name": opt_name,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "strength_count": len(strengths),
            "weakness_count": len(weaknesses),
            "additional_pros": option_pros,
            "additional_cons": option_cons,
            "balance": "优势明显" if len(strengths) > len(weaknesses) + 1 else
                      "劣势明显" if len(weaknesses) > len(strengths) + 1 else
                      "优劣均衡"
        })

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "analysis": analysis
    }


def risk_assessment(decision_id: str) -> Dict:
    """
    风险评估

    Args:
        decision_id: 决策ID

    Returns:
        风险评估结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])
    criteria = decision.get("criteria", [])
    scores = decision.get("scores", {})

    # 找出风险类标准
    risk_criteria = [c for c in criteria if c.get("type") == "cost"]

    if not risk_criteria:
        return {
            "status": "warning",
            "message": "没有风险类标准(type=cost)，无法进行风险评估",
            "suggestion": "建议添加风险、成本等负向标准"
        }

    assessments = []

    for option in options:
        opt_id = option["id"]
        opt_name = option["name"]

        if opt_id not in scores:
            continue

        opt_scores = scores[opt_id]

        risk_total = 0
        risk_count = 0
        risk_details = []

        for criterion in risk_criteria:
            crit_name = criterion["name"]
            if crit_name in opt_scores:
                score = opt_scores[crit_name]
                weight = criterion.get("weight", 0)

                risk_total += score * weight
                risk_count += 1

                # 风险等级
                if score >= 8:
                    risk_level = "高风险"
                    emoji = "🔴"
                elif score >= 5:
                    risk_level = "中风险"
                    emoji = "🟡"
                else:
                    risk_level = "低风险"
                    emoji = "🟢"

                risk_details.append({
                    "criterion": crit_name,
                    "score": score,
                    "level": risk_level,
                    "emoji": emoji
                })

        # 计算综合风险得分
        overall_risk = risk_total / sum(c.get("weight", 0) for c in risk_criteria) if risk_criteria else 0

        if overall_risk >= 7:
            overall_level = "高风险"
            overall_emoji = "🔴"
            recommendation = "需要制定风险缓解措施"
        elif overall_risk >= 4:
            overall_level = "中风险"
            overall_emoji = "🟡"
            recommendation = "可接受，但需要监控"
        else:
            overall_level = "低风险"
            overall_emoji = "🟢"
            recommendation = "风险可控"

        assessments.append({
            "option_name": opt_name,
            "overall_risk_score": round(overall_risk, 1),
            "overall_level": overall_level,
            "overall_emoji": overall_emoji,
            "risk_details": risk_details,
            "recommendation": recommendation
        })

    # 按风险排序（低风险在前）
    assessments = sorted(assessments, key=lambda x: x["overall_risk_score"])

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "risk_criteria_count": len(risk_criteria),
        "assessments": assessments,
        "lowest_risk": assessments[0]["option_name"] if assessments else None,
        "highest_risk": assessments[-1]["option_name"] if assessments else None
    }


def scenario_analysis(decision_id: str, scenarios: List[Dict]) -> Dict:
    """
    场景分析 - 在不同场景下评估决策

    Args:
        decision_id: 决策ID
        scenarios: 场景列表 [{"name": "乐观", "weight_adjustments": {"回报": 1.5}}]

    Returns:
        场景分析结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    if not scenarios:
        # 使用默认场景
        scenarios = [
            {"name": "基准情景", "weight_adjustments": {}},
            {"name": "乐观情景", "weight_adjustments": {"风险水平": 0.5}},  # 降低风险权重
            {"name": "悲观情景", "weight_adjustments": {"风险水平": 1.5}}   # 提高风险权重
        ]

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    results = []

    for scenario in scenarios:
        scenario_name = scenario.get("name", "未命名场景")
        adjustments = scenario.get("weight_adjustments", {})

        # 临时调整权重
        original_weights = {c["name"]: c["weight"] for c in criteria}

        for c in criteria:
            if c["name"] in adjustments:
                c["weight"] = original_weights[c["name"]] * adjustments[c["name"]]

        # 归一化
        total = sum(c["weight"] for c in criteria)
        for c in criteria:
            c["weight"] = c["weight"] / total if total > 0 else 0

        # 计算该场景下的结果
        weighted = calculate_weighted_scores(decision_id)

        if weighted.get("status") == "success":
            rankings = weighted.get("results", [])
            results.append({
                "scenario": scenario_name,
                "winner": rankings[0]["option_name"] if rankings else None,
                "winner_score": rankings[0]["normalized_score"] if rankings else 0,
                "full_rankings": [{"option": r["option_name"], "score": r["normalized_score"]} for r in rankings]
            })

        # 恢复原始权重
        for c in criteria:
            c["weight"] = original_weights[c["name"]]

    # 分析一致性
    winners = [r["winner"] for r in results]
    is_robust = len(set(winners)) == 1

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "scenarios_analyzed": len(results),
        "results": results,
        "is_robust": is_robust,
        "robustness_assessment": "决策在各场景下一致" if is_robust else "决策因场景而异，需要更多考量",
        "most_frequent_winner": max(set(winners), key=winners.count) if winners else None
    }
