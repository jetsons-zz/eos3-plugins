"""
Option Generator Module - 选项生成模块
管理决策选项
"""

from datetime import datetime
from typing import Dict, List, Optional
from .decision_framer import DECISION_STORE


def add_option(
    decision_id: str,
    name: str,
    description: str = "",
    pros: List[str] = None,
    cons: List[str] = None,
    estimated_cost: str = None,
    estimated_time: str = None
) -> Dict:
    """
    添加决策选项

    Args:
        decision_id: 决策ID
        name: 选项名称
        description: 选项描述
        pros: 优势列表
        cons: 劣势列表
        estimated_cost: 预估成本
        estimated_time: 预估时间

    Returns:
        添加结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]

    # 生成选项ID
    option_id = f"opt_{len(decision['options']) + 1}"

    option = {
        "id": option_id,
        "name": name,
        "description": description,
        "pros": pros or [],
        "cons": cons or [],
        "estimated_cost": estimated_cost,
        "estimated_time": estimated_time,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    decision["options"].append(option)
    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": f"选项 '{name}' 已添加",
        "option": option,
        "total_options": len(decision["options"])
    }


def remove_option(decision_id: str, option_id: str) -> Dict:
    """
    移除选项

    Args:
        decision_id: 决策ID
        option_id: 选项ID

    Returns:
        移除结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])

    for i, opt in enumerate(options):
        if opt["id"] == option_id:
            removed = options.pop(i)
            decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

            # 同时删除相关评分
            if option_id in decision.get("scores", {}):
                del decision["scores"][option_id]

            return {
                "status": "success",
                "message": f"选项 '{removed['name']}' 已移除"
            }

    return {
        "status": "error",
        "message": f"未找到选项: {option_id}"
    }


def get_options(decision_id: str) -> Dict:
    """
    获取所有选项

    Args:
        decision_id: 决策ID

    Returns:
        选项列表
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])

    return {
        "status": "success",
        "decision_title": decision.get("title"),
        "option_count": len(options),
        "options": options
    }


def update_option(decision_id: str, option_id: str, updates: Dict) -> Dict:
    """
    更新选项

    Args:
        decision_id: 决策ID
        option_id: 选项ID
        updates: 更新内容

    Returns:
        更新结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    decision = DECISION_STORE[decision_id]
    options = decision.get("options", [])

    for opt in options:
        if opt["id"] == option_id:
            for key, value in updates.items():
                if key != "id":
                    opt[key] = value
            decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return {
                "status": "success",
                "message": "选项已更新",
                "option": opt
            }

    return {
        "status": "error",
        "message": f"未找到选项: {option_id}"
    }


def generate_options_from_template(decision_id: str, template_type: str) -> Dict:
    """
    根据模板生成选项建议

    Args:
        decision_id: 决策ID
        template_type: 模板类型

    Returns:
        生成的选项建议
    """
    option_templates = {
        "investment": [
            {"name": "保守投资", "description": "低风险固定收益产品"},
            {"name": "平衡投资", "description": "股债均衡配置"},
            {"name": "激进投资", "description": "高比例权益资产"},
            {"name": "另类投资", "description": "房产/私募/加密货币"}
        ],
        "hiring": [
            {"name": "候选人A", "description": "经验丰富的行业专家"},
            {"name": "候选人B", "description": "潜力新人，性价比高"},
            {"name": "候选人C", "description": "跨界人才，创新思维"},
            {"name": "暂不招聘", "description": "内部培养或外包"}
        ],
        "vendor": [
            {"name": "供应商A", "description": "行业领先，价格较高"},
            {"name": "供应商B", "description": "性价比优，服务一般"},
            {"name": "供应商C", "description": "新兴企业，创新方案"},
            {"name": "自建团队", "description": "内部开发/生产"}
        ],
        "strategy": [
            {"name": "扩张战略", "description": "积极扩大市场份额"},
            {"name": "专注战略", "description": "深耕核心业务"},
            {"name": "多元化战略", "description": "进入新市场/新业务"},
            {"name": "防守战略", "description": "降本增效，稳健经营"}
        ],
        "product": [
            {"name": "功能A", "description": "用户强需求，开发成本高"},
            {"name": "功能B", "description": "差异化卖点，技术挑战"},
            {"name": "功能C", "description": "快速实现，用户价值中等"},
            {"name": "暂不开发", "description": "观察市场，积累资源"}
        ]
    }

    suggestions = option_templates.get(template_type, [])

    if not suggestions:
        return {
            "status": "error",
            "message": f"未找到模板: {template_type}",
            "available_templates": list(option_templates.keys())
        }

    return {
        "status": "success",
        "template": template_type,
        "suggestions": suggestions,
        "note": "这些是建议选项，请根据实际情况调整"
    }


def add_quick_options(decision_id: str, option_names: List[str]) -> Dict:
    """
    快速添加多个选项

    Args:
        decision_id: 决策ID
        option_names: 选项名称列表

    Returns:
        添加结果
    """
    results = []
    for name in option_names:
        result = add_option(decision_id, name)
        results.append({
            "name": name,
            "success": result.get("status") == "success"
        })

    success_count = sum(1 for r in results if r["success"])

    return {
        "status": "success",
        "added_count": success_count,
        "total_requested": len(option_names),
        "results": results
    }
