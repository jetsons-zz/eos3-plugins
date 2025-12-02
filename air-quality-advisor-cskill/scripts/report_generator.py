"""
Report Generator - 空气质量报告生成器
生成适合高管阅读的空气质量报告
"""

from datetime import datetime
from typing import Dict, List, Optional
from .aqi_client import AQIClient, get_city_aqi
from .health_advisor import (
    get_health_recommendations,
    get_activity_advice,
    get_sensitive_group_warnings,
    get_mask_recommendation,
    get_travel_health_advice
)


def generate_aqi_report(city: str, token: str = None) -> str:
    """
    生成城市空气质量报告

    Args:
        city: 城市名称
        token: API token

    Returns:
        Markdown 格式报告
    """
    client = AQIClient(token)
    data = client.get_city_aqi(city)

    if not data or 'error' in data:
        return f"## ❌ 无法获取 {city} 的空气质量数据\n\n{data.get('error', '未知错误')}"

    aqi = data['aqi']
    health = get_health_recommendations(aqi)
    mask = get_mask_recommendation(aqi)
    warnings = get_sensitive_group_warnings(aqi)

    report = []

    # 标题
    report.append(f"# {data['emoji']} {data['city']} 空气质量报告")
    report.append(f"*更新时间: {data.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M'))}*\n")

    # 核心指标
    report.append("## 📊 空气质量指数")
    report.append(f"# **AQI {aqi}** - {data['level']}")
    report.append(f"\n{data['health_implications']}\n")

    # 行动建议
    report.append("## 🎯 行动建议")
    report.append(f"- **户外运动**: {health['outdoor_exercise']}")
    report.append(f"- **开窗通风**: {health['window_open']}")
    report.append(f"- **口罩佩戴**: {mask['type']}")
    report.append(f"- **空气净化器**: {health['air_purifier']}")
    report.append("")

    # 敏感人群警告
    if warnings:
        report.append("## ⚠️ 敏感人群提示")
        for w in warnings:
            report.append(f"- {w['emoji']} **{w['group']}**: {w['recommendation']}")
        report.append("")

    # 污染物详情
    pollutants = data.get('pollutants', {})
    if pollutants:
        report.append("## 🔬 污染物详情")
        report.append("| 污染物 | 数值 |")
        report.append("| --- | --- |")
        for key, pol in pollutants.items():
            report.append(f"| {pol['name']} | {pol['value']} {pol['unit']} |")
        report.append("")

    # 天气信息
    weather = data.get('weather', {})
    if weather:
        report.append("## 🌡️ 天气状况")
        if 'temperature' in weather:
            report.append(f"- 温度: {weather['temperature']}°C")
        if 'humidity' in weather:
            report.append(f"- 湿度: {weather['humidity']}%")
        if 'wind' in weather:
            report.append(f"- 风速: {weather['wind']} m/s")
        report.append("")

    # 预测
    forecast = data.get('forecast', {})
    pm25_forecast = forecast.get('pm25', [])
    if pm25_forecast:
        report.append("## 📅 未来几天预测 (PM2.5)")
        for day in pm25_forecast[:5]:
            avg = day.get('avg', '-')
            date = day.get('day', '')
            report.append(f"- {date}: AQI {avg}")
        report.append("")

    return "\n".join(report)


def generate_quick_report(city: str, token: str = None) -> str:
    """
    生成简洁的快速报告（一句话版本）

    Args:
        city: 城市名称
        token: API token

    Returns:
        简洁报告
    """
    client = AQIClient(token)
    data = client.get_city_aqi(city)

    if not data or 'error' in data:
        return f"❌ 无法获取 {city} 数据"

    aqi = data['aqi']
    health = get_health_recommendations(aqi)

    return (
        f"{data['emoji']} {data['city']} AQI {aqi} ({data['level']}) | "
        f"户外运动{health['outdoor_exercise']} | "
        f"{health['summary']}"
    )


def generate_travel_advisory(
    origin_city: str,
    destination_city: str,
    token: str = None
) -> str:
    """
    生成出行空气质量对比报告

    Args:
        origin_city: 出发城市
        destination_city: 目的地城市
        token: API token

    Returns:
        出行建议报告
    """
    client = AQIClient(token)

    origin_data = client.get_city_aqi(origin_city)
    dest_data = client.get_city_aqi(destination_city)

    if not origin_data or 'error' in origin_data:
        return f"❌ 无法获取 {origin_city} 数据"
    if not dest_data or 'error' in dest_data:
        return f"❌ 无法获取 {destination_city} 数据"

    travel_advice = get_travel_health_advice(origin_data['aqi'], dest_data['aqi'])

    report = []

    # 标题
    report.append(f"# ✈️ 出行空气质量对比")
    report.append(f"*{origin_city} → {destination_city}*\n")

    # 对比表格
    report.append("## 📊 空气质量对比")
    report.append("| 指标 | 出发地 | 目的地 |")
    report.append("| --- | --- | --- |")
    report.append(f"| 城市 | {origin_data['city']} | {dest_data['city']} |")
    report.append(f"| AQI | {origin_data['emoji']} {origin_data['aqi']} | {dest_data['emoji']} {dest_data['aqi']} |")
    report.append(f"| 等级 | {origin_data['level']} | {dest_data['level']} |")
    report.append("")

    # 出行建议
    report.append(f"## {travel_advice['emoji']} 出行建议")
    report.append(f"**{travel_advice['message']}**\n")

    # 准备事项
    report.append("### 📋 出行准备")
    for prep in travel_advice['preparation']:
        report.append(f"- {prep}")
    report.append("")

    # 目的地详细建议
    dest_health = get_health_recommendations(dest_data['aqi'])
    report.append("### 🎯 目的地活动建议")
    for activity in dest_health['activities']:
        report.append(f"- {activity}")
    report.append("")

    # 敏感人群警告
    dest_warnings = get_sensitive_group_warnings(dest_data['aqi'])
    if dest_warnings:
        report.append("### ⚠️ 敏感人群注意")
        for w in dest_warnings:
            report.append(f"- {w['emoji']} **{w['group']}**: {w['recommendation']}")

    return "\n".join(report)


def compare_cities(cities: List[str], token: str = None) -> str:
    """
    比较多个城市的空气质量

    Args:
        cities: 城市名称列表
        token: API token

    Returns:
        对比报告
    """
    client = AQIClient(token)
    results = client.get_multiple_cities(cities)

    if not results:
        return "❌ 无法获取城市数据"

    # 按 AQI 排序
    sorted_cities = sorted(results, key=lambda x: x.get('aqi', 999))

    report = []
    report.append("# 🌍 多城市空气质量对比")
    report.append(f"*{datetime.now().strftime('%Y年%m月%d日 %H:%M')}*\n")

    # 排名表格
    report.append("## 📊 空气质量排名")
    report.append("| 排名 | 城市 | AQI | 等级 | 户外运动 |")
    report.append("| --- | --- | --- | --- | --- |")

    for i, city in enumerate(sorted_cities, 1):
        health = get_health_recommendations(city['aqi'])
        report.append(
            f"| {i} | {city['emoji']} {city['city']} | {city['aqi']} | "
            f"{city['level']} | {health['outdoor_exercise']} |"
        )

    report.append("")

    # 最佳和最差
    best = sorted_cities[0]
    worst = sorted_cities[-1]

    report.append("## 📌 摘要")
    report.append(f"- **空气最好**: {best['city']} (AQI {best['aqi']})")
    report.append(f"- **空气最差**: {worst['city']} (AQI {worst['aqi']})")
    report.append(f"- **对比城市**: {len(results)} 个")

    return "\n".join(report)


def generate_activity_check(
    city: str,
    activity: str = "general",
    token: str = None
) -> str:
    """
    生成特定活动的空气质量检查报告

    Args:
        city: 城市名称
        activity: 活动类型
        token: API token

    Returns:
        活动建议报告
    """
    client = AQIClient(token)
    data = client.get_city_aqi(city)

    if not data or 'error' in data:
        return f"❌ 无法获取 {city} 数据"

    advice = get_activity_advice(data['aqi'], activity)

    report = []
    report.append(f"# {advice['emoji']} {data['city']} - {advice['activity']}适宜度检查")
    report.append(f"*当前 AQI: {data['aqi']} ({data['level']})*\n")

    report.append(f"## 结论: **{advice['status_cn']}**")
    report.append(f"\n{advice['message']}\n")

    report.append("## 📋 参考标准")
    for level, threshold in advice['thresholds'].items():
        if level == advice['status']:
            report.append(f"- **{threshold}** ← 当前")
        else:
            report.append(f"- {threshold}")

    return "\n".join(report)


def generate_executive_brief(cities: List[str] = None, token: str = None) -> str:
    """
    生成高管简报

    Args:
        cities: 关注的城市列表，默认为主要商业城市
        token: API token

    Returns:
        简洁的高管简报
    """
    if cities is None:
        cities = ["北京", "上海", "广州", "深圳", "香港", "新加坡"]

    client = AQIClient(token)
    results = client.get_multiple_cities(cities)

    if not results:
        return "❌ 无法获取数据"

    now = datetime.now()

    report = []
    report.append(f"# 🌏 空气质量快报")
    report.append(f"*{now.strftime('%Y年%m月%d日 %H:%M')}*\n")

    # 一行摘要
    good_cities = [c for c in results if c['aqi'] <= 100]
    poor_cities = [c for c in results if c['aqi'] > 100]

    if len(good_cities) == len(results):
        report.append("✅ **所有城市空气质量良好**\n")
    elif len(poor_cities) == len(results):
        report.append("⚠️ **所有城市空气质量欠佳**\n")
    else:
        report.append(f"📊 **{len(good_cities)}个城市良好，{len(poor_cities)}个城市需注意**\n")

    # 城市列表
    for city in sorted(results, key=lambda x: x['aqi']):
        health = get_health_recommendations(city['aqi'])
        report.append(f"{city['emoji']} **{city['city']}** AQI {city['aqi']} - {health['summary']}")

    return "\n".join(report)
