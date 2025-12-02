"""
Risk Scanner Module - 风险扫描模块
扫描企业法律、财务、声誉风险
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

# 模拟风险数据库
RISK_DATABASE = {
    "字节跳动": {
        "legal_risks": [
            {
                "type": "监管风险",
                "severity": "high",
                "description": "TikTok在美国面临国家安全审查，可能被强制出售或禁止",
                "status": "ongoing",
                "potential_impact": "可能失去美国市场，影响估值"
            },
            {
                "type": "数据隐私",
                "severity": "medium",
                "description": "欧盟GDPR合规调查，可能面临罚款",
                "status": "ongoing",
                "potential_impact": "罚款风险，需调整数据处理流程"
            }
        ],
        "financial_risks": [
            {
                "type": "收入集中",
                "severity": "medium",
                "description": "广告收入占比超70%，受宏观经济影响大",
                "mitigation": "正在发展电商、企业服务等多元化收入"
            }
        ],
        "reputation_risks": [
            {
                "type": "内容审核",
                "severity": "medium",
                "description": "平台内容争议时有发生",
                "mitigation": "持续投入内容安全系统建设"
            }
        ],
        "overall_risk_score": 65,
        "risk_level": "中高"
    },
    "openai": {
        "legal_risks": [
            {
                "type": "知识产权",
                "severity": "high",
                "description": "多起版权诉讼，被指训练数据侵权",
                "status": "ongoing",
                "potential_impact": "可能影响商业模式，需支付版权费"
            },
            {
                "type": "监管风险",
                "severity": "medium",
                "description": "AI监管法规不确定性",
                "status": "watching",
                "potential_impact": "可能需要调整产品功能"
            }
        ],
        "financial_risks": [
            {
                "type": "盈利压力",
                "severity": "high",
                "description": "研发成本高昂，目前仍在亏损",
                "mitigation": "企业客户增长迅速，收入快速增加"
            },
            {
                "type": "供应商依赖",
                "severity": "medium",
                "description": "高度依赖微软云服务和英伟达芯片",
                "mitigation": "与多家供应商建立合作关系"
            }
        ],
        "reputation_risks": [
            {
                "type": "AI安全争议",
                "severity": "medium",
                "description": "部分员工对AI安全问题表达担忧",
                "mitigation": "加强安全研究投入"
            },
            {
                "type": "高管变动",
                "severity": "medium",
                "description": "多名核心高管离职",
                "mitigation": "积极招聘新人才"
            }
        ],
        "overall_risk_score": 60,
        "risk_level": "中等"
    },
    "anthropic": {
        "legal_risks": [
            {
                "type": "知识产权",
                "severity": "medium",
                "description": "潜在的训练数据版权风险",
                "status": "watching",
                "potential_impact": "行业普遍问题，需关注法规发展"
            }
        ],
        "financial_risks": [
            {
                "type": "烧钱速度",
                "severity": "medium",
                "description": "AI研发成本高，持续需要融资",
                "mitigation": "已获得充足融资，现金储备充裕"
            }
        ],
        "reputation_risks": [
            {
                "type": "竞争压力",
                "severity": "low",
                "description": "面临OpenAI、Google等强劲竞争",
                "mitigation": "差异化定位于AI安全"
            }
        ],
        "overall_risk_score": 35,
        "risk_level": "较低"
    },
    "腾讯": {
        "legal_risks": [
            {
                "type": "反垄断",
                "severity": "medium",
                "description": "此前被反垄断处罚，需持续关注",
                "status": "resolved",
                "potential_impact": "已整改，风险降低"
            },
            {
                "type": "游戏监管",
                "severity": "medium",
                "description": "游戏版号审批不确定性",
                "status": "ongoing",
                "potential_impact": "影响新游戏上线节奏"
            }
        ],
        "financial_risks": [
            {
                "type": "增长放缓",
                "severity": "medium",
                "description": "国内互联网用户增长见顶",
                "mitigation": "拓展海外市场，发展企业服务"
            }
        ],
        "reputation_risks": [
            {
                "type": "游戏沉迷",
                "severity": "low",
                "description": "未成年人游戏保护压力",
                "mitigation": "已推出严格的未成年人保护系统"
            }
        ],
        "overall_risk_score": 45,
        "risk_level": "中等"
    }
}


def scan_legal_risks(company_name: str) -> Dict:
    """
    扫描法律风险

    Args:
        company_name: 公司名称

    Returns:
        法律风险评估
    """
    name_lower = company_name.lower()

    for key, data in RISK_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            legal_risks = data.get("legal_risks", [])

            # 计算法律风险得分
            severity_scores = {"high": 30, "medium": 15, "low": 5}
            total_score = sum(severity_scores.get(r.get("severity", "low"), 0) for r in legal_risks)
            max_score = len(legal_risks) * 30 if legal_risks else 1
            risk_score = min(100, int(total_score / max_score * 100)) if legal_risks else 0

            return {
                "status": "success",
                "company": key,
                "legal_risks": legal_risks,
                "risk_count": len(legal_risks),
                "high_severity_count": sum(1 for r in legal_risks if r.get("severity") == "high"),
                "risk_score": risk_score,
                "assessment": "高风险" if risk_score > 60 else "中等风险" if risk_score > 30 else "低风险",
                "recommendation": get_legal_recommendation(legal_risks)
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的风险信息",
        "note": "可通过天眼查等平台获取企业法律风险信息"
    }


def get_legal_recommendation(risks: List[Dict]) -> str:
    """生成法律风险建议"""
    high_risks = [r for r in risks if r.get("severity") == "high"]
    if high_risks:
        return f"存在{len(high_risks)}项高风险事项，建议在尽调中重点关注"
    elif risks:
        return "存在一定法律风险，建议进行详细法律尽调"
    return "未发现重大法律风险"


def scan_financial_risks(company_name: str) -> Dict:
    """
    扫描财务风险

    Args:
        company_name: 公司名称

    Returns:
        财务风险评估
    """
    name_lower = company_name.lower()

    for key, data in RISK_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            financial_risks = data.get("financial_risks", [])

            # 计算财务风险得分
            severity_scores = {"high": 30, "medium": 15, "low": 5}
            total_score = sum(severity_scores.get(r.get("severity", "low"), 0) for r in financial_risks)
            max_score = len(financial_risks) * 30 if financial_risks else 1
            risk_score = min(100, int(total_score / max_score * 100)) if financial_risks else 0

            return {
                "status": "success",
                "company": key,
                "financial_risks": financial_risks,
                "risk_count": len(financial_risks),
                "risk_score": risk_score,
                "assessment": "高风险" if risk_score > 60 else "中等风险" if risk_score > 30 else "低风险",
                "data_source": "模拟数据 (实际应分析财报)"
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的财务风险信息"
    }


def scan_reputation_risks(company_name: str) -> Dict:
    """
    扫描声誉风险

    Args:
        company_name: 公司名称

    Returns:
        声誉风险评估
    """
    name_lower = company_name.lower()

    for key, data in RISK_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            reputation_risks = data.get("reputation_risks", [])

            # 计算声誉风险得分
            severity_scores = {"high": 30, "medium": 15, "low": 5}
            total_score = sum(severity_scores.get(r.get("severity", "low"), 0) for r in reputation_risks)
            max_score = len(reputation_risks) * 30 if reputation_risks else 1
            risk_score = min(100, int(total_score / max_score * 100)) if reputation_risks else 0

            return {
                "status": "success",
                "company": key,
                "reputation_risks": reputation_risks,
                "risk_count": len(reputation_risks),
                "risk_score": risk_score,
                "assessment": "高风险" if risk_score > 60 else "中等风险" if risk_score > 30 else "低风险"
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的声誉风险信息"
    }


def get_risk_score(company_name: str) -> Dict:
    """
    获取综合风险评分

    Args:
        company_name: 公司名称

    Returns:
        综合风险评分
    """
    name_lower = company_name.lower()

    for key, data in RISK_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            overall_score = data.get("overall_risk_score", 50)
            risk_level = data.get("risk_level", "中等")

            # 各维度风险
            legal = scan_legal_risks(company_name)
            financial = scan_financial_risks(company_name)
            reputation = scan_reputation_risks(company_name)

            # 风险分布
            risk_breakdown = {
                "legal": legal.get("risk_score", 0),
                "financial": financial.get("risk_score", 0),
                "reputation": reputation.get("risk_score", 0)
            }

            # 风险等级指示
            if overall_score >= 70:
                risk_emoji = "🔴"
                investment_advice = "高风险，建议谨慎"
            elif overall_score >= 50:
                risk_emoji = "🟠"
                investment_advice = "中高风险，需详细尽调"
            elif overall_score >= 30:
                risk_emoji = "🟡"
                investment_advice = "中等风险，正常尽调即可"
            else:
                risk_emoji = "🟢"
                investment_advice = "风险较低，适合进一步接触"

            return {
                "status": "success",
                "company": key,
                "overall_score": overall_score,
                "risk_level": f"{risk_emoji} {risk_level}",
                "risk_breakdown": risk_breakdown,
                "top_risks": get_top_risks(data),
                "investment_advice": investment_advice,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的风险评分"
    }


def get_top_risks(data: Dict) -> List[Dict]:
    """获取最主要的风险项"""
    all_risks = []

    for risk in data.get("legal_risks", []):
        all_risks.append({
            "type": f"法律/{risk.get('type', '')}",
            "severity": risk.get("severity", "low"),
            "description": risk.get("description", "")
        })

    for risk in data.get("financial_risks", []):
        all_risks.append({
            "type": f"财务/{risk.get('type', '')}",
            "severity": risk.get("severity", "low"),
            "description": risk.get("description", "")
        })

    for risk in data.get("reputation_risks", []):
        all_risks.append({
            "type": f"声誉/{risk.get('type', '')}",
            "severity": risk.get("severity", "low"),
            "description": risk.get("description", "")
        })

    # 按严重程度排序
    severity_order = {"high": 0, "medium": 1, "low": 2}
    sorted_risks = sorted(all_risks, key=lambda x: severity_order.get(x.get("severity", "low"), 2))

    return sorted_risks[:5]


def compare_risk_profiles(companies: List[str]) -> Dict:
    """
    对比多家公司的风险状况

    Args:
        companies: 公司名称列表

    Returns:
        风险对比分析
    """
    profiles = []

    for company in companies:
        score = get_risk_score(company)
        if score.get("status") == "success":
            profiles.append({
                "company": score["company"],
                "overall_score": score["overall_score"],
                "risk_level": score["risk_level"],
                "breakdown": score["risk_breakdown"]
            })

    if not profiles:
        return {
            "status": "error",
            "message": "未能获取任何公司的风险数据"
        }

    # 按风险得分排序（低到高）
    ranked = sorted(profiles, key=lambda x: x["overall_score"])

    return {
        "status": "success",
        "comparison_date": datetime.now().strftime("%Y-%m-%d"),
        "companies_compared": len(profiles),
        "ranking_by_safety": ranked,
        "safest": ranked[0]["company"] if ranked else "N/A",
        "riskiest": ranked[-1]["company"] if ranked else "N/A",
        "summary": f"在{len(profiles)}家公司中，{ranked[0]['company']}风险最低" if ranked else ""
    }
