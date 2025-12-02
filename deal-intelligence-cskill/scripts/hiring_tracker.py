"""
Hiring Tracker Module - 招聘追踪模块
追踪企业招聘活动，分析增长信号
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

# 模拟招聘数据库
HIRING_DATABASE = {
    "字节跳动": {
        "total_openings": 5000,
        "growth_rate": 15,  # 同比增长%
        "departments": {
            "研发/工程": {"count": 2500, "growth": 20, "hot_roles": ["AI/ML工程师", "后端开发", "iOS/Android"]},
            "产品": {"count": 500, "growth": 10, "hot_roles": ["产品经理", "用户研究"]},
            "运营": {"count": 800, "growth": 5, "hot_roles": ["内容运营", "商务拓展"]},
            "销售": {"count": 600, "growth": 25, "hot_roles": ["广告销售", "企业销售"]},
            "设计": {"count": 300, "growth": 8, "hot_roles": ["UI设计", "交互设计"]},
            "其他": {"count": 300, "growth": 5, "hot_roles": ["HR", "财务", "法务"]}
        },
        "locations": {
            "北京": 2000,
            "上海": 1200,
            "深圳": 800,
            "新加坡": 400,
            "美国": 600
        },
        "salary_range": {
            "junior": "25-40万",
            "mid": "40-80万",
            "senior": "80-150万",
            "executive": "150万+"
        },
        "key_hires_2024": [
            {"name": "某AI专家", "role": "AI研究负责人", "from": "Google DeepMind"},
            {"name": "某产品VP", "role": "产品副总裁", "from": "Meta"}
        ]
    },
    "openai": {
        "total_openings": 500,
        "growth_rate": 80,
        "departments": {
            "研发/工程": {"count": 300, "growth": 100, "hot_roles": ["ML Research", "Systems Engineer", "Security"]},
            "产品": {"count": 50, "growth": 60, "hot_roles": ["Product Manager", "Technical PM"]},
            "安全/对齐": {"count": 80, "growth": 120, "hot_roles": ["AI Safety", "Alignment Research"]},
            "GTM": {"count": 40, "growth": 150, "hot_roles": ["Enterprise Sales", "Solutions Architect"]},
            "其他": {"count": 30, "growth": 40, "hot_roles": ["Legal", "Policy", "HR"]}
        },
        "locations": {
            "旧金山": 400,
            "伦敦": 50,
            "远程": 50
        },
        "salary_range": {
            "junior": "$150-200k",
            "mid": "$200-350k",
            "senior": "$350-500k",
            "executive": "$500k+"
        },
        "key_hires_2024": [
            {"name": "某高管", "role": "CFO", "from": "Stripe"},
            {"name": "某研究员", "role": "研究科学家", "from": "Google Brain"}
        ]
    },
    "anthropic": {
        "total_openings": 200,
        "growth_rate": 120,
        "departments": {
            "研发/工程": {"count": 120, "growth": 150, "hot_roles": ["ML Engineer", "Research Scientist"]},
            "安全研究": {"count": 40, "growth": 100, "hot_roles": ["AI Safety", "Interpretability"]},
            "产品": {"count": 20, "growth": 80, "hot_roles": ["Product Manager", "API Product"]},
            "GTM": {"count": 15, "growth": 200, "hot_roles": ["Enterprise Sales", "Partnerships"]},
            "其他": {"count": 5, "growth": 50, "hot_roles": ["Legal", "HR"]}
        },
        "locations": {
            "旧金山": 180,
            "远程": 20
        },
        "salary_range": {
            "junior": "$180-250k",
            "mid": "$250-400k",
            "senior": "$400-600k",
            "executive": "$600k+"
        },
        "key_hires_2024": [
            {"name": "某研究员", "role": "安全研究负责人", "from": "DeepMind"}
        ]
    },
    "腾讯": {
        "total_openings": 8000,
        "growth_rate": -5,
        "departments": {
            "研发/工程": {"count": 4000, "growth": -8, "hot_roles": ["游戏开发", "后端", "云原生"]},
            "产品": {"count": 800, "growth": 0, "hot_roles": ["产品经理", "策划"]},
            "运营": {"count": 1500, "growth": -10, "hot_roles": ["游戏运营", "社区运营"]},
            "销售": {"count": 1000, "growth": 5, "hot_roles": ["广告销售", "云销售"]},
            "其他": {"count": 700, "growth": -5, "hot_roles": ["HR", "财务"]}
        },
        "locations": {
            "深圳": 5000,
            "上海": 1500,
            "北京": 1000,
            "成都": 500
        },
        "salary_range": {
            "junior": "20-35万",
            "mid": "35-60万",
            "senior": "60-120万",
            "executive": "120万+"
        },
        "key_hires_2024": []
    }
}


def get_hiring_activity(company_name: str) -> Dict:
    """
    获取公司招聘活动概况

    Args:
        company_name: 公司名称

    Returns:
        招聘活动信息
    """
    name_lower = company_name.lower()

    for key, data in HIRING_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            return {
                "status": "success",
                "company": key,
                "snapshot": {
                    "total_openings": data["total_openings"],
                    "yoy_growth": f"{data['growth_rate']:+d}%",
                    "hiring_trend": "扩张" if data['growth_rate'] > 10 else "稳定" if data['growth_rate'] > -5 else "收缩"
                },
                "departments": data["departments"],
                "locations": data["locations"],
                "salary_ranges": data["salary_range"],
                "key_hires": data.get("key_hires_2024", []),
                "data_source": "模拟数据 (可对接LinkedIn/Boss直聘 API)",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的招聘信息"
    }


def analyze_growth_signals(company_name: str) -> Dict:
    """
    分析招聘背后的增长信号

    Args:
        company_name: 公司名称

    Returns:
        增长信号分析
    """
    hiring = get_hiring_activity(company_name)

    if hiring.get("status") != "success":
        return hiring

    snapshot = hiring["snapshot"]
    departments = hiring["departments"]

    # 分析各部门增长
    dept_signals = []
    for dept, info in departments.items():
        growth = info.get("growth", 0)
        if growth > 50:
            signal = f"🔥 {dept}: 快速扩张 (+{growth}%)"
            interpretation = "战略重点领域"
        elif growth > 20:
            signal = f"📈 {dept}: 稳健增长 (+{growth}%)"
            interpretation = "业务发展良好"
        elif growth > 0:
            signal = f"➡️ {dept}: 平稳发展 (+{growth}%)"
            interpretation = "正常补充"
        elif growth > -10:
            signal = f"⚠️ {dept}: 轻微收缩 ({growth}%)"
            interpretation = "优化调整中"
        else:
            signal = f"🔴 {dept}: 大幅收缩 ({growth}%)"
            interpretation = "业务收缩或重组"

        dept_signals.append({
            "department": dept,
            "signal": signal,
            "growth_rate": growth,
            "interpretation": interpretation,
            "hot_roles": info.get("hot_roles", [])
        })

    # 计算综合信号强度
    avg_growth = sum(d.get("growth", 0) for d in departments.values()) / len(departments)
    total_growth = snapshot.get("yoy_growth", "0%")

    if avg_growth > 30:
        overall_signal = "强增长信号"
        recommendation = "建议密切关注，可能是合作/投资好时机"
        score = 90
    elif avg_growth > 10:
        overall_signal = "正增长信号"
        recommendation = "公司处于健康发展期"
        score = 70
    elif avg_growth > 0:
        overall_signal = "稳定信号"
        recommendation = "业务稳定，无明显扩张迹象"
        score = 50
    elif avg_growth > -10:
        overall_signal = "谨慎信号"
        recommendation = "公司可能在优化调整，需关注"
        score = 30
    else:
        overall_signal = "收缩信号"
        recommendation = "公司可能面临挑战，需谨慎评估"
        score = 15

    # 识别战略重点
    strategic_focus = []
    for dept, info in departments.items():
        if info.get("growth", 0) > 30:
            strategic_focus.append(dept)

    return {
        "status": "success",
        "company": hiring["company"],
        "overall_assessment": {
            "signal": overall_signal,
            "score": score,
            "total_openings": snapshot["total_openings"],
            "yoy_change": total_growth,
            "recommendation": recommendation
        },
        "strategic_focus": strategic_focus if strategic_focus else ["未发现明显战略重点"],
        "department_signals": sorted(dept_signals, key=lambda x: x["growth_rate"], reverse=True),
        "key_hires": hiring.get("key_hires", []),
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }


def get_department_breakdown(company_name: str) -> Dict:
    """
    获取部门招聘明细

    Args:
        company_name: 公司名称

    Returns:
        部门招聘明细
    """
    hiring = get_hiring_activity(company_name)

    if hiring.get("status") != "success":
        return hiring

    departments = hiring["departments"]
    total = hiring["snapshot"]["total_openings"]

    breakdown = []
    for dept, info in departments.items():
        count = info.get("count", 0)
        percentage = (count / total * 100) if total else 0
        breakdown.append({
            "department": dept,
            "openings": count,
            "percentage": f"{percentage:.1f}%",
            "growth_rate": f"{info.get('growth', 0):+d}%",
            "hot_roles": info.get("hot_roles", [])
        })

    return {
        "status": "success",
        "company": hiring["company"],
        "total_openings": total,
        "department_breakdown": sorted(breakdown, key=lambda x: x["openings"], reverse=True)
    }


def track_key_hires(company_name: str) -> Dict:
    """
    追踪关键人才变动

    Args:
        company_name: 公司名称

    Returns:
        关键人才变动信息
    """
    hiring = get_hiring_activity(company_name)

    if hiring.get("status") != "success":
        return hiring

    key_hires = hiring.get("key_hires", [])

    # 分析人才来源
    sources = {}
    for hire in key_hires:
        source = hire.get("from", "Unknown")
        sources[source] = sources.get(source, 0) + 1

    return {
        "status": "success",
        "company": hiring["company"],
        "recent_key_hires": key_hires,
        "hire_count": len(key_hires),
        "talent_sources": sources,
        "signal": "积极" if len(key_hires) > 2 else "正常" if key_hires else "平静",
        "note": "关键人才引进通常预示新业务方向或战略调整"
    }


def compare_hiring(companies: List[str]) -> Dict:
    """
    对比多家公司招聘情况

    Args:
        companies: 公司名称列表

    Returns:
        对比分析
    """
    comparisons = []

    for company in companies:
        signals = analyze_growth_signals(company)
        if signals.get("status") == "success":
            comparisons.append({
                "company": signals["company"],
                "signal_score": signals["overall_assessment"]["score"],
                "signal": signals["overall_assessment"]["signal"],
                "total_openings": signals["overall_assessment"]["total_openings"],
                "yoy_change": signals["overall_assessment"]["yoy_change"],
                "strategic_focus": signals["strategic_focus"]
            })

    if not comparisons:
        return {
            "status": "error",
            "message": "未能获取任何公司的招聘数据"
        }

    # 排名
    ranked = sorted(comparisons, key=lambda x: x["signal_score"], reverse=True)

    return {
        "status": "success",
        "comparison_date": datetime.now().strftime("%Y-%m-%d"),
        "companies_compared": len(comparisons),
        "ranking": ranked,
        "leader": ranked[0]["company"] if ranked else "N/A",
        "summary": f"在{len(comparisons)}家公司中，{ranked[0]['company']}展现最强增长信号" if ranked else ""
    }
