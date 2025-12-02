"""
Decision Framer Module - 决策框架模块
定义和管理决策问题
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

# 决策存储
DECISION_STORE = {}

# 决策模板
DECISION_TEMPLATES = {
    "investment": {
        "name": "投资决策",
        "description": "评估投资机会",
        "suggested_criteria": [
            {"name": "预期回报", "weight": 0.25, "type": "benefit"},
            {"name": "风险水平", "weight": 0.20, "type": "cost"},
            {"name": "流动性", "weight": 0.15, "type": "benefit"},
            {"name": "时间跨度", "weight": 0.15, "type": "cost"},
            {"name": "市场前景", "weight": 0.15, "type": "benefit"},
            {"name": "管理难度", "weight": 0.10, "type": "cost"}
        ]
    },
    "hiring": {
        "name": "招聘决策",
        "description": "选择最佳候选人",
        "suggested_criteria": [
            {"name": "专业能力", "weight": 0.30, "type": "benefit"},
            {"name": "文化契合", "weight": 0.20, "type": "benefit"},
            {"name": "经验背景", "weight": 0.20, "type": "benefit"},
            {"name": "薪资期望", "weight": 0.15, "type": "cost"},
            {"name": "成长潜力", "weight": 0.15, "type": "benefit"}
        ]
    },
    "vendor": {
        "name": "供应商选择",
        "description": "选择最佳供应商/合作伙伴",
        "suggested_criteria": [
            {"name": "价格", "weight": 0.25, "type": "cost"},
            {"name": "质量", "weight": 0.25, "type": "benefit"},
            {"name": "交付能力", "weight": 0.20, "type": "benefit"},
            {"name": "服务支持", "weight": 0.15, "type": "benefit"},
            {"name": "合作历史", "weight": 0.15, "type": "benefit"}
        ]
    },
    "strategy": {
        "name": "战略决策",
        "description": "重大战略方向选择",
        "suggested_criteria": [
            {"name": "市场机会", "weight": 0.20, "type": "benefit"},
            {"name": "竞争优势", "weight": 0.20, "type": "benefit"},
            {"name": "资源要求", "weight": 0.15, "type": "cost"},
            {"name": "执行难度", "weight": 0.15, "type": "cost"},
            {"name": "风险", "weight": 0.15, "type": "cost"},
            {"name": "战略契合", "weight": 0.15, "type": "benefit"}
        ]
    },
    "product": {
        "name": "产品决策",
        "description": "产品功能/路线图决策",
        "suggested_criteria": [
            {"name": "用户价值", "weight": 0.25, "type": "benefit"},
            {"name": "开发成本", "weight": 0.20, "type": "cost"},
            {"name": "市场需求", "weight": 0.20, "type": "benefit"},
            {"name": "技术可行性", "weight": 0.15, "type": "benefit"},
            {"name": "竞争差异化", "weight": 0.20, "type": "benefit"}
        ]
    }
}


def create_decision(
    title: str,
    description: str = "",
    template: str = None,
    deadline: str = None,
    stakeholders: List[str] = None
) -> Dict:
    """
    创建新决策

    Args:
        title: 决策标题
        description: 决策描述
        template: 使用的模板 (investment/hiring/vendor/strategy/product)
        deadline: 决策截止日期
        stakeholders: 利益相关者列表

    Returns:
        创建的决策对象
    """
    decision_id = str(uuid.uuid4())[:8]

    decision = {
        "id": decision_id,
        "title": title,
        "description": description,
        "status": "draft",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "deadline": deadline,
        "stakeholders": stakeholders or [],
        "options": [],
        "criteria": [],
        "scores": {},
        "recommendation": None
    }

    # 如果使用模板，应用模板的建议标准
    if template and template in DECISION_TEMPLATES:
        tpl = DECISION_TEMPLATES[template]
        decision["template"] = template
        decision["criteria"] = tpl.get("suggested_criteria", [])

    DECISION_STORE[decision_id] = decision

    return {
        "status": "success",
        "message": f"决策 '{title}' 已创建",
        "decision_id": decision_id,
        "decision": decision
    }


def get_decision(decision_id: str) -> Dict:
    """
    获取决策详情

    Args:
        decision_id: 决策ID

    Returns:
        决策对象
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    return {
        "status": "success",
        "decision": DECISION_STORE[decision_id]
    }


def list_decisions(status: str = None) -> Dict:
    """
    列出所有决策

    Args:
        status: 筛选状态 (draft/in_progress/completed)

    Returns:
        决策列表
    """
    decisions = list(DECISION_STORE.values())

    if status:
        decisions = [d for d in decisions if d.get("status") == status]

    # 按更新时间排序
    decisions = sorted(decisions, key=lambda x: x.get("updated_at", ""), reverse=True)

    return {
        "status": "success",
        "count": len(decisions),
        "decisions": [{
            "id": d["id"],
            "title": d["title"],
            "status": d["status"],
            "option_count": len(d.get("options", [])),
            "deadline": d.get("deadline"),
            "updated_at": d.get("updated_at")
        } for d in decisions]
    }


def update_decision(decision_id: str, updates: Dict) -> Dict:
    """
    更新决策

    Args:
        decision_id: 决策ID
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

    # 应用更新
    for key, value in updates.items():
        if key not in ["id", "created_at"]:  # 保护不可变字段
            decision[key] = value

    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": "决策已更新",
        "decision": decision
    }


def delete_decision(decision_id: str) -> Dict:
    """
    删除决策

    Args:
        decision_id: 决策ID

    Returns:
        删除结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    deleted = DECISION_STORE.pop(decision_id)

    return {
        "status": "success",
        "message": f"决策 '{deleted['title']}' 已删除"
    }


def get_available_templates() -> Dict:
    """获取可用的决策模板"""
    templates = []
    for key, tpl in DECISION_TEMPLATES.items():
        templates.append({
            "id": key,
            "name": tpl["name"],
            "description": tpl["description"],
            "criteria_count": len(tpl.get("suggested_criteria", []))
        })

    return {
        "status": "success",
        "templates": templates
    }


def apply_template(decision_id: str, template: str) -> Dict:
    """
    应用模板到决策

    Args:
        decision_id: 决策ID
        template: 模板ID

    Returns:
        应用结果
    """
    if decision_id not in DECISION_STORE:
        return {
            "status": "error",
            "message": f"未找到决策: {decision_id}"
        }

    if template not in DECISION_TEMPLATES:
        return {
            "status": "error",
            "message": f"未找到模板: {template}",
            "available_templates": list(DECISION_TEMPLATES.keys())
        }

    tpl = DECISION_TEMPLATES[template]
    decision = DECISION_STORE[decision_id]

    decision["template"] = template
    decision["criteria"] = tpl.get("suggested_criteria", [])
    decision["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "status": "success",
        "message": f"已应用模板: {tpl['name']}",
        "criteria_added": len(decision["criteria"]),
        "decision": decision
    }
