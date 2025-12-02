"""
Funding Analyzer Module - 融资分析模块
分析企业融资历史、估值轨迹、投资人信息
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

# 模拟融资数据库（实际应用中可对接天眼查、Crunchbase等API）
FUNDING_DATABASE = {
    "字节跳动": {
        "total_raised": "$8.4B",
        "latest_valuation": "$220B",
        "funding_rounds": [
            {"round": "Pre-IPO", "date": "2021-12", "amount": "$5B", "investors": ["红杉资本", "泛大西洋投资"]},
            {"round": "Series E", "date": "2018-10", "amount": "$3B", "investors": ["软银愿景基金", "KKR", "General Atlantic"]},
            {"round": "Series D", "date": "2017-09", "amount": "$2B", "investors": ["General Atlantic", "软银"]},
            {"round": "Series C", "date": "2016-12", "amount": "$1B", "investors": ["红杉资本中国", "建银国际"]},
            {"round": "Series B", "date": "2014-06", "amount": "$100M", "investors": ["红杉资本中国", "DST Global"]},
            {"round": "Series A", "date": "2012-07", "amount": "$数百万", "investors": ["海纳亚洲创投"]},
        ]
    },
    "openai": {
        "total_raised": "$14B+",
        "latest_valuation": "$157B",
        "funding_rounds": [
            {"round": "Series F", "date": "2024-10", "amount": "$6.6B", "investors": ["Thrive Capital", "微软", "英伟达", "软银"]},
            {"round": "Series E", "date": "2023-04", "amount": "$300M", "investors": ["红杉资本", "Andreessen Horowitz"]},
            {"round": "Series D", "date": "2023-01", "amount": "$10B", "investors": ["微软"]},
            {"round": "Series C", "date": "2021-01", "amount": "$200M", "investors": ["Tiger Global", "Andreessen Horowitz"]},
            {"round": "Series B", "date": "2019-07", "amount": "$1B", "investors": ["微软"]},
        ]
    },
    "anthropic": {
        "total_raised": "$7.5B+",
        "latest_valuation": "$61B",
        "funding_rounds": [
            {"round": "Series E", "date": "2024-08", "amount": "$4B", "investors": ["亚马逊"]},
            {"round": "Series D", "date": "2024-01", "amount": "$750M", "investors": ["Menlo Ventures", "Google"]},
            {"round": "Series C", "date": "2023-05", "amount": "$450M", "investors": ["Spark Capital", "Google"]},
            {"round": "Series B", "date": "2023-02", "amount": "$300M", "investors": ["Google Cloud"]},
            {"round": "Series A", "date": "2022-04", "amount": "$580M", "investors": ["Jaan Tallinn", "Dustin Moskovitz"]},
        ]
    },
    "spacex": {
        "total_raised": "$10B+",
        "latest_valuation": "$180B",
        "funding_rounds": [
            {"round": "Series N", "date": "2024-06", "amount": "$350M", "investors": ["Andreessen Horowitz", "Gigafund"]},
            {"round": "Series M", "date": "2023-12", "amount": "$750M", "investors": ["Valor Equity Partners", "Fidelity"]},
            {"round": "Series L", "date": "2022-05", "amount": "$1.7B", "investors": ["Andreessen Horowitz", "Sequoia"]},
        ]
    }
}

# 投资机构信息
INVESTOR_DATABASE = {
    "红杉资本": {
        "name_en": "Sequoia Capital",
        "type": "VC",
        "aum": "$85B",
        "focus": ["科技", "医疗", "消费"],
        "notable_investments": ["苹果", "Google", "Airbnb", "Stripe", "字节跳动"],
        "stage_preference": ["Seed", "Series A", "Series B", "Growth"]
    },
    "软银愿景基金": {
        "name_en": "SoftBank Vision Fund",
        "type": "PE/VC",
        "aum": "$100B",
        "focus": ["AI", "科技", "出行"],
        "notable_investments": ["Uber", "WeWork", "字节跳动", "DoorDash"],
        "stage_preference": ["Late Stage", "Pre-IPO"]
    },
    "Andreessen Horowitz": {
        "name_en": "a16z",
        "type": "VC",
        "aum": "$35B",
        "focus": ["软件", "Crypto", "Bio"],
        "notable_investments": ["Facebook", "Airbnb", "Coinbase", "Instacart"],
        "stage_preference": ["Seed", "Series A", "Series B", "Growth"]
    },
    "微软": {
        "name_en": "Microsoft",
        "type": "Strategic",
        "aum": "N/A",
        "focus": ["AI", "云计算", "企业软件"],
        "notable_investments": ["OpenAI", "LinkedIn", "GitHub", "Nuance"],
        "stage_preference": ["Strategic"]
    },
    "亚马逊": {
        "name_en": "Amazon",
        "type": "Strategic",
        "aum": "N/A",
        "focus": ["AI", "物流", "零售科技"],
        "notable_investments": ["Anthropic", "Rivian", "Ring"],
        "stage_preference": ["Strategic"]
    }
}


def get_funding_history(company_name: str) -> Dict:
    """
    获取公司融资历史

    Args:
        company_name: 公司名称

    Returns:
        融资历史信息
    """
    name_lower = company_name.lower()

    # 查找匹配的公司
    for key, data in FUNDING_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            return {
                "status": "success",
                "company": key,
                "total_raised": data["total_raised"],
                "latest_valuation": data["latest_valuation"],
                "round_count": len(data["funding_rounds"]),
                "funding_rounds": data["funding_rounds"],
                "data_source": "模拟数据 (可对接天眼查/Crunchbase API)"
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的融资记录",
        "suggestion": "该公司可能是上市公司或融资信息未公开"
    }


def analyze_funding_trajectory(company_name: str) -> Dict:
    """
    分析融资轨迹和趋势

    Args:
        company_name: 公司名称

    Returns:
        融资轨迹分析
    """
    history = get_funding_history(company_name)

    if history.get("status") != "success":
        return history

    rounds = history["funding_rounds"]

    # 分析融资间隔
    intervals = []
    for i in range(len(rounds) - 1):
        try:
            date1 = datetime.strptime(rounds[i]["date"], "%Y-%m")
            date2 = datetime.strptime(rounds[i+1]["date"], "%Y-%m")
            interval = (date1 - date2).days / 30  # 月数
            intervals.append(interval)
        except:
            pass

    avg_interval = sum(intervals) / len(intervals) if intervals else 0

    # 分析投资人类型
    all_investors = []
    for r in rounds:
        all_investors.extend(r.get("investors", []))

    investor_types = {
        "VC": 0,
        "PE": 0,
        "Strategic": 0,
        "Other": 0
    }

    for inv in set(all_investors):
        if inv in INVESTOR_DATABASE:
            inv_type = INVESTOR_DATABASE[inv].get("type", "Other")
            if "VC" in inv_type:
                investor_types["VC"] += 1
            elif "PE" in inv_type:
                investor_types["PE"] += 1
            elif "Strategic" in inv_type:
                investor_types["Strategic"] += 1
            else:
                investor_types["Other"] += 1
        else:
            investor_types["Other"] += 1

    # 融资阶段分析
    latest_round = rounds[0] if rounds else {}

    analysis = {
        "status": "success",
        "company": history["company"],
        "summary": {
            "total_raised": history["total_raised"],
            "latest_valuation": history["latest_valuation"],
            "total_rounds": len(rounds),
            "latest_round": latest_round.get("round", "N/A"),
            "latest_amount": latest_round.get("amount", "N/A"),
            "latest_date": latest_round.get("date", "N/A"),
        },
        "trajectory_analysis": {
            "avg_funding_interval_months": round(avg_interval, 1),
            "funding_velocity": "快速" if avg_interval < 12 else "正常" if avg_interval < 24 else "缓慢",
            "stage": get_company_stage(latest_round.get("round", "")),
            "growth_signal": "强" if len(rounds) > 4 and avg_interval < 18 else "中" if len(rounds) > 2 else "弱"
        },
        "investor_mix": investor_types,
        "unique_investors": len(set(all_investors)),
        "repeat_investors": find_repeat_investors(rounds),
        "notable_investors": [inv for inv in set(all_investors) if inv in INVESTOR_DATABASE][:5]
    }

    return analysis


def get_company_stage(round_name: str) -> str:
    """判断公司所处阶段"""
    round_lower = round_name.lower()
    if "seed" in round_lower or "angel" in round_lower:
        return "种子期"
    elif "series a" in round_lower:
        return "早期"
    elif "series b" in round_lower or "series c" in round_lower:
        return "成长期"
    elif "series d" in round_lower or "series e" in round_lower:
        return "扩张期"
    elif "pre-ipo" in round_lower or "series f" in round_lower:
        return "Pre-IPO"
    else:
        return "成熟期"


def find_repeat_investors(rounds: List[Dict]) -> List[str]:
    """找出多轮投资的投资人"""
    investor_count = {}
    for r in rounds:
        for inv in r.get("investors", []):
            investor_count[inv] = investor_count.get(inv, 0) + 1

    return [inv for inv, count in investor_count.items() if count > 1]


def get_investor_info(investor_name: str) -> Dict:
    """
    获取投资机构信息

    Args:
        investor_name: 投资机构名称

    Returns:
        投资机构详情
    """
    # 精确匹配
    if investor_name in INVESTOR_DATABASE:
        data = INVESTOR_DATABASE[investor_name]
        return {
            "status": "success",
            "name": investor_name,
            "name_en": data.get("name_en", ""),
            "type": data.get("type", "N/A"),
            "aum": data.get("aum", "N/A"),
            "focus_areas": data.get("focus", []),
            "notable_investments": data.get("notable_investments", []),
            "stage_preference": data.get("stage_preference", [])
        }

    # 模糊匹配
    name_lower = investor_name.lower()
    for key, data in INVESTOR_DATABASE.items():
        if name_lower in key.lower() or name_lower in data.get("name_en", "").lower():
            return {
                "status": "success",
                "name": key,
                "name_en": data.get("name_en", ""),
                "type": data.get("type", "N/A"),
                "aum": data.get("aum", "N/A"),
                "focus_areas": data.get("focus", []),
                "notable_investments": data.get("notable_investments", []),
                "stage_preference": data.get("stage_preference", [])
            }

    return {
        "status": "not_found",
        "message": f"未找到 {investor_name} 的信息"
    }


def estimate_valuation(company_name: str, method: str = "comparable") -> Dict:
    """
    估算公司估值

    Args:
        company_name: 公司名称
        method: 估值方法 (comparable/dcf/funding)

    Returns:
        估值分析
    """
    history = get_funding_history(company_name)

    if history.get("status") != "success":
        return {
            "status": "error",
            "message": "无法获取融资数据进行估值"
        }

    latest_val = history.get("latest_valuation", "$0")

    # 解析估值
    try:
        val_str = latest_val.replace("$", "").replace("B", "")
        base_val = float(val_str.split()[0]) * 1e9
    except:
        base_val = 0

    # 不同估值方法
    if method == "comparable":
        # 可比公司法（模拟）
        premium = random.uniform(0.9, 1.2)
        estimated = base_val * premium
        confidence = "中等"
    elif method == "dcf":
        # DCF法（模拟）
        premium = random.uniform(0.85, 1.15)
        estimated = base_val * premium
        confidence = "低（需要财务数据）"
    else:
        # 基于最新融资
        estimated = base_val
        confidence = "高（基于最新融资）"

    return {
        "status": "success",
        "company": history["company"],
        "method": method,
        "latest_funding_valuation": latest_val,
        "estimated_current_valuation": f"${estimated/1e9:.1f}B",
        "valuation_range": {
            "low": f"${estimated*0.8/1e9:.1f}B",
            "mid": f"${estimated/1e9:.1f}B",
            "high": f"${estimated*1.2/1e9:.1f}B"
        },
        "confidence": confidence,
        "note": "此估值仅供参考，实际价值可能因市场条件而异"
    }
