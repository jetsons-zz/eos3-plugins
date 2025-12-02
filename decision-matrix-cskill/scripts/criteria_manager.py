"""
Criteria Manager Module - 标准管理模块
管理决策评估标准和权重
"""

from datetime import datetime
from typing import Dict, List, Optional
from .decision_framer import DECISION_STORE


def add_criterion(
    decision_id: str,
    name: str,
    weight: float = 0.1,
    criterion_type: str = "benefit",
    description: str = ""
) -> Dict:
    """
    添加评估标准

    Args:
        decision_id: 决策ID
        name: 标准名称
        weight: 权重 (0-1)
        criterion_type: 类型 (benefit-越高越好, cost-越低越好)
        description: 描述

    Returns:
        添加结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    if not 0 <= weight <= 1:
        return {
            "status": "error",
            "message": "权重必须在0-1之间"
        }

    if criterion_type not in ["benefit", "cost"]:
        return {
            "status": "error",
            "message": "类型必须是 'benefit' 或 'cost'"
        }

    decision = DECISION_STORE[decision_id]

    # 检查是否已存在
    for c in decision.get("criteria", []):
        if c["name"] == name:
            return {
                "status": "error",
                "message": f"标准 '{name}' 已存在"
            }

    criterion = {
        "name": name,
        "weight": weight,
        "type": criterion_type,
        "description": description
    }

    if "criteria" not in decision:
        decision["criteria"] = []

    decision["criteria"].append(criterion)
    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": f"标准 '{name}' 已添加",
        "criterion": criterion,
        "total_criteria": len(decision["criteria"]),
        "total_weight": sum(c["weight"] for c in decision["criteria"])
    }


def remove_criterion(decision_id: str, name: str) -> Dict:
    """
    移除评估标准

    Args:
        decision_id: 决策ID
        name: 标准名称

    Returns:
        移除结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    for i, c in enumerate(criteria):
        if c["name"] == name:
            removed = criteria.pop(i)
            decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return {
                "status": "success",
                "message": f"标准 '{name}' 已移除"
            }

    return {
        "status": "error",
        "message": f"未找到标准: {name}"
    }


def get_criteria(decision_id: str) -> Dict:
    """
    获取所有评估标准

    Args:
        decision_id: 决策ID

    Returns:
        标准列表
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    total_weight = sum(c["weight"] for c in criteria)

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "criteria_count": len(criteria),
        "total_weight": total_weight,
        "is_normalized": abs(total_weight - 1.0) < 0.01,
        "criteria": criteria
    }


def set_weights(decision_id: str, weights: Dict[str, float]) -> Dict:
    """
    设置标准权重

    Args:
        decision_id: 决策ID
        weights: 权重字典 {标准名: 权重}

    Returns:
        设置结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    updated = []
    for c in criteria:
        if c["name"] in weights:
            c["weight"] = weights[c["name"]]
            updated.append(c["name"])

    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_weight = sum(c["weight"] for c in criteria)

    return {
        "status": "success",
        "updated_count": len(updated),
        "updated_criteria": updated,
        "total_weight": total_weight,
        "warning": "权重总和不为1，建议归一化" if abs(total_weight - 1.0) > 0.01 else None
    }


def normalize_weights(decision_id: str) -> Dict:
    """
    归一化权重（使总和为1）

    Args:
        decision_id: 决策ID

    Returns:
        归一化结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    if not criteria:
        return {
            "status": "error",
            "message": "没有可归一化的标准"
        }

    total_weight = sum(c["weight"] for c in criteria)

    if total_weight == 0:
        # 平均分配
        avg_weight = 1.0 / len(criteria)
        for c in criteria:
            c["weight"] = avg_weight
    else:
        # 按比例归一化
        for c in criteria:
            c["weight"] = c["weight"] / total_weight

    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": "权重已归一化",
        "criteria": [{"name": c["name"], "weight": round(c["weight"], 3)} for c in criteria]
    }


def suggest_weights(decision_id: str, priority_order: List[str] = None) -> Dict:
    """
    建议权重分配

    Args:
        decision_id: 决策ID
        priority_order: 按重要性排序的标准名称列表

    Returns:
        建议权重
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    if not criteria:
        return {
            "status": "error",
            "message": "没有评估标准"
        }

    n = len(criteria)

    if priority_order:
        # 根据优先级顺序分配权重（线性递减）
        suggested = {}
        for i, name in enumerate(priority_order):
            weight = (n - i) / sum(range(1, n + 1))
            suggested[name] = round(weight, 3)
    else:
        # 平均分配
        suggested = {c["name"]: round(1.0 / n, 3) for c in criteria}

    return {
        "status": "success",
        "suggested_weights": suggested,
        "note": "建议权重仅供参考，请根据实际重要性调整"
    }


def validate_criteria(decision_id: str) -> Dict:
    """
    验证标准设置

    Args:
        decision_id: 决策ID

    Returns:
        验证结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    criteria = decision.get("criteria", [])

    issues = []

    if not criteria:
        issues.append("未设置任何评估标准")

    total_weight = sum(c["weight"] for c in criteria)
    if abs(total_weight - 1.0) > 0.01:
        issues.append(f"权重总和为 {total_weight:.2f}，建议归一化为1.0")

    if len(criteria) < 3:
        issues.append("建议至少设置3个评估标准")

    if len(criteria) > 10:
        issues.append("标准过多可能影响决策质量，建议精简")

    benefit_count = sum(1 for c in criteria if c.get("type") == "benefit")
    cost_count = sum(1 for c in criteria if c.get("type") == "cost")

    if benefit_count == 0:
        issues.append("没有正向标准(benefit)，建议添加")
    if cost_count == 0:
        issues.append("没有负向标准(cost)，建议添加风险/成本类标准")

    return {
        "status": "success",
        "is_valid": len(issues) == 0,
        "criteria_count": len(criteria),
        "total_weight": total_weight,
        "benefit_criteria": benefit_count,
        "cost_criteria": cost_count,
        "issues": issues if issues else ["标准设置完整，可以开始评分"]
    }
