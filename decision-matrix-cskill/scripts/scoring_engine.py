"""
Scoring Engine Module - 评分引擎模块
计算加权得分和排名
"""

from datetime import datetime
from typing import Dict, List, Optional
from .decision_framer import DECISION_STORE


def score_option(
    decision_id: str,
    option_id: str,
    scores: Dict[str, float]
) -> Dict:
    """
    为选项评分

    Args:
        decision_id: 决策ID
        option_id: 选项ID
        scores: 评分字典 {标准名: 分数(1-10)}

    Returns:
        评分结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]

    # 验证选项存在
    option_exists = any(o["id"] == option_id for o in decision.get("options", []))
    if not option_exists:
        return {
            "status": "error",
            "message": f"未找到选项: {option_id}"
        }

    # 验证评分范围
    for criterion, score in scores.items():
        if not 1 <= score <= 10:
            return {
                "status": "error",
                "message": f"分数必须在1-10之间: {criterion}={score}"
            }

    # 存储评分
    if "scores" not in decision:
        decision["scores"] = {}

    decision["scores"][option_id] = scores
    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": f"选项 {option_id} 评分已保存",
        "scores": scores
    }


def get_scores(decision_id: str, option_id: str = None) -> Dict:
    """
    获取评分

    Args:
        decision_id: 决策ID
        option_id: 选项ID（可选，不提供则返回所有）

    Returns:
        评分数据
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    scores = decision.get("scores", {})

    if option_id:
        if option_id not in scores:
            return {
                "status": "error",
                "message": f"选项 {option_id} 未评分"
            }
        return {
            "status": "success",
            "option_id": option_id,
            "scores": scores[option_id]
        }

    return {
        "status": "success",
        "all_scores": scores,
        "scored_options": len(scores),
        "total_options": len(decision.get("options", []))
    }


def calculate_weighted_scores(decision_id: str) -> Dict:
    """
    计算加权得分

    Args:
        decision_id: 决策ID

    Returns:
        加权得分结果
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

    if not options:
        return {"status": "error", "message": "没有选项"}
    if not criteria:
        return {"status": "error", "message": "没有评估标准"}
    if not scores:
        return {"status": "error", "message": "没有评分数据"}

    # 构建标准权重和类型映射
    criteria_map = {c["name"]: c for c in criteria}

    results = []

    for option in options:
        opt_id = option["id"]
        opt_name = option["name"]

        if opt_id not in scores:
            continue

        opt_scores = scores[opt_id]
        weighted_sum = 0
        score_details = []

        for criterion_name, raw_score in opt_scores.items():
            if criterion_name not in criteria_map:
                continue

            criterion = criteria_map[criterion_name]
            weight = criterion.get("weight", 0)
            crit_type = criterion.get("type", "benefit")

            # 对于cost类型，分数反转（10变1，1变10）
            if crit_type == "cost":
                adjusted_score = 11 - raw_score
            else:
                adjusted_score = raw_score

            weighted_score = adjusted_score * weight
            weighted_sum += weighted_score

            score_details.append({
                "criterion": criterion_name,
                "raw_score": raw_score,
                "adjusted_score": adjusted_score,
                "weight": weight,
                "weighted_score": round(weighted_score, 3)
            })

        results.append({
            "option_id": opt_id,
            "option_name": opt_name,
            "weighted_score": round(weighted_sum, 3),
            "normalized_score": round(weighted_sum / 10 * 100, 1),  # 转换为百分制
            "score_details": score_details
        })

    # 按加权得分排序
    results = sorted(results, key=lambda x: x["weighted_score"], reverse=True)

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "results": results,
        "winner": results[0] if results else None
    }


def rank_options(decision_id: str) -> Dict:
    """
    对选项排名

    Args:
        decision_id: 决策ID

    Returns:
        排名结果
    """
    weighted = calculate_weighted_scores(decision_id)

    if weighted.get("status") != "success":
        return weighted

    results = weighted.get("results", [])

    rankings = []
    for i, result in enumerate(results, 1):
        rankings.append({
            "rank": i,
            "option_name": result["option_name"],
            "score": result["normalized_score"],
            "score_bar": "█" * int(result["normalized_score"] / 5) + "░" * (20 - int(result["normalized_score"] / 5))
        })

    return {
        "status": "success",
        "decision_title": weighted.get("decision_title"),
        "rankings": rankings,
        "top_choice": rankings[0] if rankings else None,
        "score_gap": round(rankings[0]["score"] - rankings[-1]["score"], 1) if len(rankings) > 1 else 0
    }


def get_recommendation(decision_id: str) -> Dict:
    """
    获取决策建议

    Args:
        decision_id: 决策ID

    Returns:
        决策建议
    """
    weighted = calculate_weighted_scores(decision_id)

    if weighted.get("status") != "success":
        return weighted

    results = weighted.get("results", [])

    if not results:
        return {
            "status": "error",
            "message": "没有足够的数据生成建议"
        }

    winner = results[0]
    runner_up = results[1] if len(results) > 1 else None

    # 计算置信度
    if runner_up:
        score_gap = winner["normalized_score"] - runner_up["normalized_score"]
        if score_gap > 20:
            confidence = "高"
            confidence_emoji = "🟢"
            advice = "明显的最佳选择"
        elif score_gap > 10:
            confidence = "中高"
            confidence_emoji = "🟡"
            advice = "较好的选择，但可再考虑"
        elif score_gap > 5:
            confidence = "中等"
            confidence_emoji = "🟠"
            advice = "两个选项接近，需要权衡"
        else:
            confidence = "低"
            confidence_emoji = "🔴"
            advice = "选项非常接近，需要更多信息"
    else:
        confidence = "仅有一个选项"
        confidence_emoji = "⚪"
        advice = "建议添加更多选项进行比较"
        score_gap = 0

    # 生成建议
    recommendation = {
        "status": "success",
        "recommendation": {
            "choice": winner["option_name"],
            "score": winner["normalized_score"],
            "confidence": confidence,
            "confidence_emoji": confidence_emoji,
            "advice": advice
        },
        "comparison": {
            "winner": winner["option_name"],
            "winner_score": winner["normalized_score"],
            "runner_up": runner_up["option_name"] if runner_up else None,
            "runner_up_score": runner_up["normalized_score"] if runner_up else None,
            "score_gap": round(score_gap, 1) if runner_up else None
        },
        "all_rankings": [{
            "rank": i + 1,
            "option": r["option_name"],
            "score": r["normalized_score"]
        } for i, r in enumerate(results)]
    }

    # 保存建议到决策
    decision = DECISION_STORE.get(decision_id)
    if decision:
        decision["recommendation"] = recommendation["recommendation"]
        decision["status"] = "completed"
        decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return recommendation
