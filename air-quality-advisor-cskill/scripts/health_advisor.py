"""
Health Advisor - 健康建议模块
基于空气质量提供健康和活动建议
"""

from datetime import datetime
from typing import Dict, List, Optional


# 敏感人群定义
SENSITIVE_GROUPS = {
    "children": {
        "name": "儿童",
        "name_en": "Children",
        "description": "儿童呼吸系统尚未发育完全，更容易受到空气污染影响",
        "extra_caution_aqi": 100  # 从这个 AQI 开始需要额外注意
    },
    "elderly": {
        "name": "老年人",
        "name_en": "Elderly",
        "description": "老年人心肺功能较弱，更容易受到影响",
        "extra_caution_aqi": 100
    },
    "respiratory": {
        "name": "呼吸系统疾病患者",
        "name_en": "Respiratory conditions",
        "description": "哮喘、慢阻肺等呼吸系统疾病患者",
        "extra_caution_aqi": 75
    },
    "cardiovascular": {
        "name": "心血管疾病患者",
        "name_en": "Heart disease",
        "description": "心脏病、高血压等心血管疾病患者",
        "extra_caution_aqi": 100
    },
    "pregnant": {
        "name": "孕妇",
        "name_en": "Pregnant women",
        "description": "孕妇需要保护胎儿健康",
        "extra_caution_aqi": 100
    },
    "outdoor_workers": {
        "name": "户外工作者",
        "name_en": "Outdoor workers",
        "description": "长时间户外工作的人群",
        "extra_caution_aqi": 150
    }
}

# 活动建议
ACTIVITY_RECOMMENDATIONS = {
    (0, 50): {
        "outdoor_exercise": "适宜",
        "window_open": "建议开窗通风",
        "mask": "无需佩戴口罩",
        "air_purifier": "无需使用",
        "activities": [
            "适合进行各种户外运动",
            "可以长时间户外活动",
            "适合户外用餐和聚会",
            "适合晨练和夜跑"
        ]
    },
    (51, 100): {
        "outdoor_exercise": "基本适宜",
        "window_open": "可以开窗通风",
        "mask": "敏感人群可佩戴",
        "air_purifier": "可选使用",
        "activities": [
            "一般人群可正常户外活动",
            "敏感人群适当减少剧烈运动",
            "户外活动时间可适当缩短",
            "建议选择空气流通好的区域"
        ]
    },
    (101, 150): {
        "outdoor_exercise": "减少",
        "window_open": "减少开窗",
        "mask": "建议佩戴口罩",
        "air_purifier": "建议使用",
        "activities": [
            "减少户外剧烈运动",
            "敏感人群应避免户外活动",
            "外出佩戴防护口罩",
            "室内活动为主"
        ]
    },
    (151, 200): {
        "outdoor_exercise": "避免",
        "window_open": "避免开窗",
        "mask": "必须佩戴 N95/KN95",
        "air_purifier": "必须使用",
        "activities": [
            "避免户外运动",
            "所有人群减少外出",
            "外出必须佩戴专业口罩",
            "室内使用空气净化器"
        ]
    },
    (201, 300): {
        "outdoor_exercise": "禁止",
        "window_open": "禁止开窗",
        "mask": "必须佩戴 N95/KN95",
        "air_purifier": "必须全天运行",
        "activities": [
            "所有户外活动取消",
            "尽量留在室内",
            "门窗紧闭，使用空气净化器",
            "必须外出时全程佩戴口罩"
        ]
    },
    (301, 500): {
        "outdoor_exercise": "禁止",
        "window_open": "禁止开窗",
        "mask": "必须佩戴专业防护口罩",
        "air_purifier": "必须全天运行",
        "activities": [
            "健康警报：停止一切户外活动",
            "所有人群留在室内",
            "考虑转移到空气质量更好的地区",
            "如有不适立即就医"
        ]
    }
}


def get_health_recommendations(aqi: int, include_details: bool = True) -> Dict:
    """
    根据 AQI 获取健康建议

    Args:
        aqi: 空气质量指数
        include_details: 是否包含详细信息

    Returns:
        健康建议字典
    """
    # 获取对应的建议
    recommendations = None
    for (low, high), rec in ACTIVITY_RECOMMENDATIONS.items():
        if low <= aqi <= high:
            recommendations = rec
            break

    if recommendations is None:
        recommendations = ACTIVITY_RECOMMENDATIONS[(301, 500)]

    # 基础建议
    result = {
        "aqi": aqi,
        "outdoor_exercise": recommendations["outdoor_exercise"],
        "window_open": recommendations["window_open"],
        "mask": recommendations["mask"],
        "air_purifier": recommendations["air_purifier"],
        "activities": recommendations["activities"]
    }

    if include_details:
        # 添加详细说明
        if aqi <= 50:
            result["summary"] = "空气质量优秀，适合各种户外活动"
            result["emoji"] = "😊"
        elif aqi <= 100:
            result["summary"] = "空气质量良好，可正常进行户外活动"
            result["emoji"] = "🙂"
        elif aqi <= 150:
            result["summary"] = "空气质量一般，敏感人群需注意"
            result["emoji"] = "😐"
        elif aqi <= 200:
            result["summary"] = "空气质量较差，建议减少外出"
            result["emoji"] = "😷"
        elif aqi <= 300:
            result["summary"] = "空气污染严重，避免户外活动"
            result["emoji"] = "🤢"
        else:
            result["summary"] = "空气污染危险，请留在室内"
            result["emoji"] = "☠️"

    return result


def get_activity_advice(aqi: int, activity_type: str = "general") -> Dict:
    """
    获取特定活动的建议

    Args:
        aqi: 空气质量指数
        activity_type: 活动类型 (general, running, cycling, walking, outdoor_dining)

    Returns:
        活动建议
    """
    activity_thresholds = {
        "running": {
            "suitable_max": 75,
            "caution_max": 100,
            "avoid_max": 150,
            "name": "跑步",
            "intensity": "高"
        },
        "cycling": {
            "suitable_max": 75,
            "caution_max": 100,
            "avoid_max": 150,
            "name": "骑行",
            "intensity": "高"
        },
        "walking": {
            "suitable_max": 100,
            "caution_max": 150,
            "avoid_max": 200,
            "name": "散步",
            "intensity": "低"
        },
        "outdoor_dining": {
            "suitable_max": 75,
            "caution_max": 100,
            "avoid_max": 150,
            "name": "户外用餐",
            "intensity": "无"
        },
        "golf": {
            "suitable_max": 100,
            "caution_max": 150,
            "avoid_max": 200,
            "name": "高尔夫",
            "intensity": "中"
        },
        "tennis": {
            "suitable_max": 75,
            "caution_max": 100,
            "avoid_max": 150,
            "name": "网球",
            "intensity": "高"
        },
        "general": {
            "suitable_max": 100,
            "caution_max": 150,
            "avoid_max": 200,
            "name": "一般户外活动",
            "intensity": "中"
        }
    }

    activity = activity_thresholds.get(activity_type, activity_thresholds["general"])

    if aqi <= activity["suitable_max"]:
        status = "suitable"
        status_cn = "适宜"
        emoji = "✅"
        message = f"当前空气质量适合{activity['name']}"
    elif aqi <= activity["caution_max"]:
        status = "caution"
        status_cn = "注意"
        emoji = "⚠️"
        message = f"可以进行{activity['name']}，但建议缩短时间"
    elif aqi <= activity["avoid_max"]:
        status = "avoid"
        status_cn = "避免"
        emoji = "🚫"
        message = f"不建议进行{activity['name']}，请改为室内活动"
    else:
        status = "dangerous"
        status_cn = "危险"
        emoji = "☠️"
        message = f"禁止进行{activity['name']}及任何户外活动"

    return {
        "activity": activity["name"],
        "activity_type": activity_type,
        "aqi": aqi,
        "status": status,
        "status_cn": status_cn,
        "emoji": emoji,
        "message": message,
        "intensity": activity["intensity"],
        "thresholds": {
            "suitable": f"AQI ≤ {activity['suitable_max']}",
            "caution": f"AQI {activity['suitable_max']+1}-{activity['caution_max']}",
            "avoid": f"AQI {activity['caution_max']+1}-{activity['avoid_max']}",
            "dangerous": f"AQI > {activity['avoid_max']}"
        }
    }


def get_sensitive_group_warnings(aqi: int) -> List[Dict]:
    """
    获取敏感人群警告

    Args:
        aqi: 空气质量指数

    Returns:
        需要警告的敏感人群列表
    """
    warnings = []

    for group_id, group in SENSITIVE_GROUPS.items():
        if aqi >= group["extra_caution_aqi"]:
            # 根据 AQI 级别确定警告级别
            if aqi >= 200:
                level = "severe"
                level_cn = "严重警告"
                emoji = "🚨"
            elif aqi >= 150:
                level = "warning"
                level_cn = "警告"
                emoji = "⚠️"
            else:
                level = "caution"
                level_cn = "注意"
                emoji = "⚡"

            warnings.append({
                "group": group["name"],
                "group_en": group["name_en"],
                "level": level,
                "level_cn": level_cn,
                "emoji": emoji,
                "description": group["description"],
                "recommendation": _get_group_recommendation(group_id, aqi)
            })

    return warnings


def _get_group_recommendation(group_id: str, aqi: int) -> str:
    """获取特定人群的建议"""
    if group_id == "children":
        if aqi >= 150:
            return "儿童应避免户外活动，在室内保持空气清洁"
        else:
            return "儿童应减少户外剧烈运动时间"

    elif group_id == "elderly":
        if aqi >= 150:
            return "老年人应留在室内，避免外出"
        else:
            return "老年人外出时应减少活动强度"

    elif group_id == "respiratory":
        if aqi >= 150:
            return "请留在室内，备好急救药物，如有不适立即就医"
        else:
            return "减少户外活动，随身携带药物"

    elif group_id == "cardiovascular":
        if aqi >= 150:
            return "避免任何剧烈活动，如有胸闷等症状立即就医"
        else:
            return "减少体力消耗，注意休息"

    elif group_id == "pregnant":
        if aqi >= 150:
            return "请留在室内，使用空气净化器，保持室内空气清洁"
        else:
            return "减少外出，外出时佩戴口罩"

    elif group_id == "outdoor_workers":
        if aqi >= 200:
            return "建议暂停户外工作，如必须工作请做好全面防护"
        elif aqi >= 150:
            return "缩短户外工作时间，增加休息频率，佩戴防护口罩"
        else:
            return "工作时佩戴口罩，适当增加休息"

    return "请注意防护"


def get_mask_recommendation(aqi: int) -> Dict:
    """
    获取口罩佩戴建议

    Args:
        aqi: 空气质量指数

    Returns:
        口罩建议
    """
    if aqi <= 50:
        return {
            "need_mask": False,
            "type": "无需",
            "message": "空气质量优秀，无需佩戴口罩"
        }
    elif aqi <= 100:
        return {
            "need_mask": False,
            "type": "可选",
            "message": "一般人群无需佩戴，敏感人群可选择佩戴普通口罩"
        }
    elif aqi <= 150:
        return {
            "need_mask": True,
            "type": "普通口罩/KN95",
            "message": "建议外出时佩戴口罩，敏感人群建议 KN95"
        }
    elif aqi <= 200:
        return {
            "need_mask": True,
            "type": "KN95/N95",
            "message": "外出必须佩戴 KN95 或 N95 口罩"
        }
    else:
        return {
            "need_mask": True,
            "type": "N95 专业防护",
            "message": "必须佩戴 N95 专业防护口罩，尽量避免外出"
        }


def get_travel_health_advice(origin_aqi: int, destination_aqi: int) -> Dict:
    """
    获取出行健康建议

    Args:
        origin_aqi: 出发地 AQI
        destination_aqi: 目的地 AQI

    Returns:
        出行建议
    """
    aqi_diff = destination_aqi - origin_aqi

    if aqi_diff <= -50:
        status = "better"
        message = "目的地空气质量明显优于出发地，有利于健康"
        emoji = "👍"
    elif aqi_diff <= 0:
        status = "similar_better"
        message = "目的地空气质量略好于或接近出发地"
        emoji = "✅"
    elif aqi_diff <= 50:
        status = "similar_worse"
        message = "目的地空气质量略差于出发地，注意适应"
        emoji = "⚠️"
    else:
        status = "worse"
        message = "目的地空气质量明显差于出发地，建议做好防护"
        emoji = "🚨"

    return {
        "origin_aqi": origin_aqi,
        "destination_aqi": destination_aqi,
        "difference": aqi_diff,
        "status": status,
        "emoji": emoji,
        "message": message,
        "preparation": _get_travel_preparation(destination_aqi)
    }


def _get_travel_preparation(destination_aqi: int) -> List[str]:
    """获取出行准备建议"""
    prep = []

    if destination_aqi > 100:
        prep.append("携带口罩（建议 KN95 或 N95）")

    if destination_aqi > 150:
        prep.append("准备便携式空气净化器")
        prep.append("选择有空气净化系统的酒店")

    if destination_aqi > 200:
        prep.append("考虑调整行程或缩短停留时间")
        prep.append("携带必要的呼吸道药物")

    if not prep:
        prep.append("无需特别准备，正常出行即可")

    return prep
