"""
Travel Advisor - 出行智囊核心模块
整合所有模块生成综合出行报告
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .weather_module import get_weather_forecast, get_clothing_advice
from .air_quality_module import get_air_quality, get_health_advice
from .forex_module import get_exchange_rate, get_budget_estimate
from .timezone_module import get_timezone_info, get_best_meeting_times
from .holiday_module import check_business_days, get_upcoming_holidays


def calculate_travel_score(
    weather: Dict,
    air_quality: Dict,
    business_days: Dict
) -> Dict:
    """
    计算出行综合评分

    Args:
        weather: 天气数据
        air_quality: 空气质量数据
        business_days: 工作日数据

    Returns:
        综合评分
    """
    score = 100
    factors = []

    # 天气评分 (40分)
    if "error" not in weather:
        summary = weather.get("summary", {})
        avg_temp = (summary.get("avg_high", 20) + summary.get("avg_low", 10)) / 2

        # 温度舒适度
        if 15 <= avg_temp <= 25:
            factors.append({"factor": "温度舒适", "impact": 0})
        elif 10 <= avg_temp <= 30:
            factors.append({"factor": "温度可接受", "impact": -5})
            score -= 5
        else:
            factors.append({"factor": "温度较极端", "impact": -15})
            score -= 15

        # 降雨概率
        rain_prob = summary.get("max_rain_probability", 0)
        if rain_prob > 70:
            factors.append({"factor": "降雨概率高", "impact": -10})
            score -= 10
        elif rain_prob > 40:
            factors.append({"factor": "可能有雨", "impact": -5})
            score -= 5
    else:
        factors.append({"factor": "天气数据不可用", "impact": -10})
        score -= 10

    # 空气质量评分 (30分)
    if "error" not in air_quality:
        aqi = air_quality.get("aqi", 50)
        health = get_health_advice(aqi)
        impact = health.get("score_impact", 0)
        if impact < 0:
            factors.append({"factor": f"空气质量{air_quality.get('level', '一般')}", "impact": impact})
            score += impact  # impact 是负数
        else:
            factors.append({"factor": "空气质量良好", "impact": 0})
    else:
        factors.append({"factor": "空气质量数据不可用", "impact": -5})
        score -= 5

    # 工作日评分 (30分)
    if "error" not in business_days:
        warnings = business_days.get("warnings", [])
        if warnings:
            factors.append({"factor": "包含节假日/周末", "impact": -10})
            score -= 10
        else:
            factors.append({"factor": "工作日安排合理", "impact": 0})
    else:
        factors.append({"factor": "日历数据不可用", "impact": -5})
        score -= 5

    # 确定等级
    if score >= 85:
        grade = "优秀"
        stars = "⭐⭐⭐⭐⭐"
        emoji = "🌟"
    elif score >= 70:
        grade = "良好"
        stars = "⭐⭐⭐⭐"
        emoji = "👍"
    elif score >= 55:
        grade = "一般"
        stars = "⭐⭐⭐"
        emoji = "👌"
    elif score >= 40:
        grade = "较差"
        stars = "⭐⭐"
        emoji = "⚠️"
    else:
        grade = "不佳"
        stars = "⭐"
        emoji = "❌"

    return {
        "score": max(0, min(100, score)),
        "grade": grade,
        "stars": stars,
        "emoji": emoji,
        "factors": factors
    }


def get_packing_checklist(
    weather: Dict,
    air_quality: Dict,
    days: int,
    is_business: bool = True
) -> Dict:
    """
    生成行李清单

    Args:
        weather: 天气数据
        air_quality: 空气质量数据
        days: 出行天数
        is_business: 是否商务出行

    Returns:
        行李清单
    """
    essentials = ["护照/身份证", "手机充电器", "转换插头"]
    clothing = []
    accessories = []
    health = []

    # 根据天气添加衣物
    if "error" not in weather:
        summary = weather.get("summary", {})
        avg_temp = (summary.get("avg_high", 20) + summary.get("avg_low", 10)) / 2

        advice = get_clothing_advice(
            summary.get("avg_high", 20),
            summary.get("avg_low", 10),
            summary.get("max_rain_probability", 0)
        )
        clothing.extend(advice.get("essential_items", []))

        if summary.get("needs_umbrella"):
            accessories.append("雨伞")

    # 根据空气质量
    if "error" not in air_quality:
        aqi = air_quality.get("aqi", 50)
        if aqi > 100:
            health.append("口罩 (KN95/N95)")
        if aqi > 150:
            health.append("便携空气净化器")

    # 商务出行必备
    if is_business:
        clothing.extend(["商务正装", "备用衬衫"])
        essentials.extend(["名片", "笔记本电脑", "商务资料"])

    # 根据天数调整
    if days > 3:
        accessories.append("洗漱用品")
    if days > 5:
        accessories.append("备用鞋")

    # 去重
    clothing = list(dict.fromkeys(clothing))
    accessories = list(dict.fromkeys(accessories))

    return {
        "essentials": essentials,
        "clothing": clothing,
        "accessories": accessories,
        "health": health,
        "tips": [
            "建议提前1天整理行李",
            "重要文件建议备份电子版",
            "贵重物品随身携带"
        ]
    }


def generate_travel_report(
    destination: str,
    start_date: str,
    end_date: str,
    origin: str = "北京",
    home_currency: str = "CNY",
    budget_level: str = "mid"
) -> str:
    """
    生成综合出行报告

    Args:
        destination: 目的地
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        origin: 出发地
        home_currency: 本国货币
        budget_level: 预算级别

    Returns:
        Markdown 格式的出行报告
    """
    # 计算天数
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1

    # 获取各模块数据
    weather = get_weather_forecast(destination, days)
    air_quality = get_air_quality(destination)
    timezone = get_timezone_info(origin, destination)
    business_days = check_business_days(destination, start_date, end_date)
    budget = get_budget_estimate(destination, days, budget_level, home_currency)

    # 计算评分
    score = calculate_travel_score(weather, air_quality, business_days)

    # 生成行李清单
    packing = get_packing_checklist(weather, air_quality, days)

    # 构建报告
    report = []

    # 标题
    report.append("━" * 50)
    report.append(f"🌍 {destination}出行智能报告")
    report.append(f"   {start_date} - {end_date} ({days}天)")
    report.append("━" * 50)
    report.append("")

    # 综合评分
    report.append(f"📊 出行评分: {score['score']}/100 {score['stars']}")
    report.append("")

    # 天气概况
    report.append("🌡️ 天气概况")
    if "error" not in weather:
        summary = weather.get("summary", {})
        # 显示前几天天气
        forecasts = weather.get("forecasts", [])[:3]
        weather_str = " → ".join([f.get("weather", "") for f in forecasts])
        report.append(f"   {summary.get('temp_range', 'N/A')} | {weather_str}")

        if summary.get("needs_umbrella"):
            report.append(f"   ⚠️ 可能有雨，建议携带雨具")
    else:
        report.append(f"   ⚠️ {weather.get('error', '无法获取数据')}")
    report.append("")

    # 空气质量
    report.append("💨 空气质量")
    if "error" not in air_quality:
        report.append(f"   AQI {air_quality['aqi']} {air_quality['emoji']} {air_quality['level']}")
        health = get_health_advice(air_quality['aqi'])
        if air_quality['aqi'] > 100:
            report.append(f"   ⚠️ {health['mask']}")
    else:
        report.append(f"   ⚠️ {air_quality.get('error', '无法获取数据')}")
    report.append("")

    # 汇率换算
    report.append("💱 汇率预算")
    if "error" not in budget:
        daily = budget["daily_budget"]
        total = budget["total_budget"]
        report.append(f"   汇率: 1 {home_currency} = {round(1/budget['exchange_rate'], 4)} {budget.get('city', destination)}货币")
        report.append(f"   日均预算: {daily['formatted']} ({budget['level_cn']})")
        report.append(f"   总预算: {total['formatted']}")
    report.append("")

    # 时差提醒
    report.append("🕐 时差提醒")
    if "error" not in timezone:
        report.append(f"   {timezone['time_difference_desc']}")
        report.append(f"   {origin} 09:00 = {destination} {timezone['conversion_examples'][0]['dest_time']}")
        jet_lag = timezone.get("jet_lag_advice", {})
        if jet_lag.get("adjustment_days", 0) > 0:
            report.append(f"   💡 {jet_lag.get('advice', '')}")
    else:
        report.append(f"   ⚠️ {timezone.get('error', '无法获取数据')}")
    report.append("")

    # 当地日历
    report.append("📅 当地情况")
    if "error" not in business_days:
        if business_days.get("holidays_in_period"):
            for h in business_days["holidays_in_period"]:
                report.append(f"   📌 {h['date']}: {h['name']}")
        else:
            report.append("   ✓ 无重大节假日")

        report.append(f"   工作日: {business_days['business_days']}天 / 总共{business_days['total_days']}天")

        for warning in business_days.get("warnings", []):
            report.append(f"   ⚠️ {warning}")
    report.append("")

    # 注意事项
    report.append("⚠️ 注意事项")
    for factor in score["factors"]:
        if factor["impact"] < 0:
            report.append(f"   • {factor['factor']}")

    # 添加通用建议
    if "error" not in weather:
        summary = weather.get("summary", {})
        avg_temp = (summary.get("avg_high", 20) + summary.get("avg_low", 10)) / 2
        if avg_temp < 10:
            report.append("   • 天气较冷，注意保暖")
        elif avg_temp > 30:
            report.append("   • 天气炎热，注意防暑")
    report.append("")

    # 行李清单
    report.append("✈️ 行李清单")
    all_items = packing["clothing"] + packing["accessories"] + packing["health"]
    for item in all_items[:8]:  # 只显示前8项
        report.append(f"   □ {item}")
    if len(all_items) > 8:
        report.append(f"   ... 及其他 {len(all_items) - 8} 项")

    report.append("")
    report.append("━" * 50)

    return "\n".join(report)


def quick_travel_check(destination: str, date: str = None) -> str:
    """
    快速出行检查（一句话版本）

    Args:
        destination: 目的地
        date: 日期 (可选)

    Returns:
        简洁的出行建议
    """
    weather = get_weather_forecast(destination, 1)
    air_quality = get_air_quality(destination)

    parts = [f"🌍 {destination}"]

    if "error" not in weather:
        summary = weather.get("summary", {})
        parts.append(f"🌡️ {summary.get('temp_range', 'N/A')}")

    if "error" not in air_quality:
        parts.append(f"{air_quality['emoji']} AQI {air_quality['aqi']}")

    return " | ".join(parts)
