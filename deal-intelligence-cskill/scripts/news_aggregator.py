"""
News Aggregator Module - 新闻聚合模块
聚合公司新闻、行业动态、舆情分析
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

# 模拟新闻数据库
NEWS_DATABASE = {
    "字节跳动": [
        {
            "title": "字节跳动2024年营收突破1100亿美元",
            "source": "36氪",
            "date": "2024-11-15",
            "sentiment": "positive",
            "category": "财务",
            "summary": "字节跳动2024年营收预计达1100亿美元，同比增长30%，主要得益于TikTok广告和电商业务增长。"
        },
        {
            "title": "TikTok美国业务面临新监管挑战",
            "source": "华尔街日报",
            "date": "2024-11-10",
            "sentiment": "negative",
            "category": "监管",
            "summary": "美国国会推进法案，要求TikTok与中国母公司分离，否则面临禁令。"
        },
        {
            "title": "字节跳动AI大模型进军企业市场",
            "source": "科技日报",
            "date": "2024-11-05",
            "sentiment": "positive",
            "category": "产品",
            "summary": "字节跳动发布企业级AI产品，与飞书深度整合，进军B端市场。"
        }
    ],
    "openai": [
        {
            "title": "OpenAI完成66亿美元融资，估值达1570亿",
            "source": "Bloomberg",
            "date": "2024-10-02",
            "sentiment": "positive",
            "category": "融资",
            "summary": "OpenAI完成科技史上最大规模私募融资，投资者包括Thrive Capital、微软、英伟达、软银。"
        },
        {
            "title": "OpenAI发布GPT-4o，多模态能力大幅提升",
            "source": "TechCrunch",
            "date": "2024-05-13",
            "sentiment": "positive",
            "category": "产品",
            "summary": "新模型支持实时语音对话、图像理解，响应速度提升数倍。"
        },
        {
            "title": "多名高管离职引发公司治理担忧",
            "source": "The Information",
            "date": "2024-09-25",
            "sentiment": "negative",
            "category": "人事",
            "summary": "CTO、首席研究官等多位核心高管相继离职，引发外界对公司方向的质疑。"
        }
    ],
    "anthropic": [
        {
            "title": "Anthropic获亚马逊40亿美元投资",
            "source": "CNBC",
            "date": "2024-08-20",
            "sentiment": "positive",
            "category": "融资",
            "summary": "亚马逊完成对Anthropic的40亿美元投资，成为其最大股东之一。"
        },
        {
            "title": "Claude 3.5 Sonnet性能超越GPT-4",
            "source": "Wired",
            "date": "2024-06-20",
            "sentiment": "positive",
            "category": "产品",
            "summary": "Anthropic发布Claude 3.5 Sonnet，在多项基准测试中超越竞争对手。"
        }
    ],
    "腾讯": [
        {
            "title": "腾讯Q3营收1672亿，游戏业务回暖",
            "source": "财新",
            "date": "2024-11-13",
            "sentiment": "positive",
            "category": "财务",
            "summary": "腾讯第三季度营收同比增长8%，国内游戏业务恢复增长。"
        },
        {
            "title": "微信小程序日活突破4亿",
            "source": "腾讯官方",
            "date": "2024-10-20",
            "sentiment": "positive",
            "category": "产品",
            "summary": "微信小程序生态持续扩大，日活用户达4亿，交易规模同比增长30%。"
        },
        {
            "title": "腾讯视频号商业化加速",
            "source": "晚点LatePost",
            "date": "2024-09-15",
            "sentiment": "positive",
            "category": "业务",
            "summary": "视频号广告收入快速增长，成为腾讯新的增长引擎。"
        }
    ]
}

# 行业新闻
INDUSTRY_NEWS = {
    "AI": [
        {"title": "全球AI投资2024年预计达2000亿美元", "sentiment": "positive"},
        {"title": "欧盟AI法案正式生效，企业面临合规压力", "sentiment": "neutral"},
        {"title": "AI芯片供应紧张持续，英伟达产能告急", "sentiment": "neutral"}
    ],
    "互联网": [
        {"title": "中国互联网广告市场恢复增长", "sentiment": "positive"},
        {"title": "短视频用户时长首次下滑", "sentiment": "negative"},
        {"title": "出海成为互联网公司新增长点", "sentiment": "positive"}
    ],
    "金融科技": [
        {"title": "数字人民币试点范围扩大", "sentiment": "positive"},
        {"title": "跨境支付监管趋严", "sentiment": "neutral"},
        {"title": "BNPL坏账率上升引发担忧", "sentiment": "negative"}
    ]
}


def get_company_news(company_name: str, days: int = 30, limit: int = 10) -> Dict:
    """
    获取公司相关新闻

    Args:
        company_name: 公司名称
        days: 查询天数
        limit: 返回数量限制

    Returns:
        新闻列表
    """
    name_lower = company_name.lower()

    for key, news_list in NEWS_DATABASE.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            # 过滤日期（模拟）
            filtered = news_list[:limit]

            return {
                "status": "success",
                "company": key,
                "news_count": len(filtered),
                "time_range": f"最近{days}天",
                "news": filtered,
                "data_source": "模拟数据 (可对接新闻API)"
            }

    return {
        "status": "not_found",
        "message": f"未找到 {company_name} 的相关新闻",
        "suggestion": "可尝试搜索公司全称或简称"
    }


def get_industry_news(industry: str, limit: int = 5) -> Dict:
    """
    获取行业新闻

    Args:
        industry: 行业名称
        limit: 返回数量限制

    Returns:
        行业新闻列表
    """
    industry_lower = industry.lower()

    for key, news_list in INDUSTRY_NEWS.items():
        if industry_lower in key.lower() or key.lower() in industry_lower:
            return {
                "status": "success",
                "industry": key,
                "news_count": len(news_list[:limit]),
                "news": news_list[:limit]
            }

    return {
        "status": "not_found",
        "message": f"未找到 {industry} 行业的新闻",
        "available_industries": list(INDUSTRY_NEWS.keys())
    }


def sentiment_analysis(company_name: str) -> Dict:
    """
    分析公司舆情

    Args:
        company_name: 公司名称

    Returns:
        舆情分析结果
    """
    news_result = get_company_news(company_name)

    if news_result.get("status") != "success":
        return news_result

    news_list = news_result.get("news", [])

    # 统计情感分布
    sentiment_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }

    category_count = {}

    for news in news_list:
        sentiment = news.get("sentiment", "neutral")
        sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1

        category = news.get("category", "其他")
        category_count[category] = category_count.get(category, 0) + 1

    total = len(news_list)
    if total == 0:
        return {
            "status": "error",
            "message": "没有足够的新闻进行分析"
        }

    # 计算情感得分 (0-100)
    positive_pct = sentiment_count["positive"] / total * 100
    negative_pct = sentiment_count["negative"] / total * 100
    sentiment_score = 50 + (positive_pct - negative_pct) / 2

    # 确定整体情感
    if sentiment_score >= 70:
        overall_sentiment = "积极"
        sentiment_emoji = "🟢"
    elif sentiment_score >= 50:
        overall_sentiment = "中性偏积极"
        sentiment_emoji = "🟡"
    elif sentiment_score >= 30:
        overall_sentiment = "中性偏消极"
        sentiment_emoji = "🟠"
    else:
        overall_sentiment = "消极"
        sentiment_emoji = "🔴"

    # 识别主要话题
    main_topics = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "status": "success",
        "company": news_result["company"],
        "analysis_period": "最近30天",
        "total_news": total,
        "sentiment_summary": {
            "score": round(sentiment_score, 1),
            "overall": overall_sentiment,
            "emoji": sentiment_emoji,
            "breakdown": {
                "positive": f"{sentiment_count['positive']} ({positive_pct:.0f}%)",
                "neutral": f"{sentiment_count['neutral']} ({sentiment_count['neutral']/total*100:.0f}%)",
                "negative": f"{sentiment_count['negative']} ({negative_pct:.0f}%)"
            }
        },
        "main_topics": main_topics[:5],
        "positive_headlines": [n["title"] for n in news_list if n.get("sentiment") == "positive"][:3],
        "negative_headlines": [n["title"] for n in news_list if n.get("sentiment") == "negative"][:3],
        "recommendation": get_sentiment_recommendation(sentiment_score)
    }


def get_sentiment_recommendation(score: float) -> str:
    """根据情感得分给出建议"""
    if score >= 70:
        return "舆论环境良好，适合推进合作/投资"
    elif score >= 50:
        return "舆论整体正面，需关注潜在风险点"
    elif score >= 30:
        return "存在一定负面舆论，建议深入调查原因"
    else:
        return "负面舆论较多，需谨慎评估风险"


def get_press_releases(company_name: str, limit: int = 5) -> Dict:
    """
    获取公司官方新闻稿

    Args:
        company_name: 公司名称
        limit: 返回数量

    Returns:
        新闻稿列表
    """
    news_result = get_company_news(company_name)

    if news_result.get("status") != "success":
        return news_result

    # 模拟筛选官方发布
    official_releases = []
    for news in news_result.get("news", []):
        if news.get("source") in ["腾讯官方", "官方", "公司公告"]:
            official_releases.append(news)

    # 如果没有官方发布，返回正面新闻
    if not official_releases:
        official_releases = [n for n in news_result.get("news", []) if n.get("sentiment") == "positive"][:limit]

    return {
        "status": "success",
        "company": news_result["company"],
        "press_releases": official_releases[:limit],
        "note": "数据为模拟内容，实际应用需对接官方IR页面"
    }


def get_news_summary(company_name: str) -> str:
    """
    生成新闻摘要（一句话版本）

    Args:
        company_name: 公司名称

    Returns:
        简洁摘要
    """
    sentiment = sentiment_analysis(company_name)

    if sentiment.get("status") != "success":
        return f"未找到 {company_name} 的相关新闻"

    summary = sentiment.get("sentiment_summary", {})
    score = summary.get("score", 50)
    emoji = summary.get("emoji", "🟡")
    overall = summary.get("overall", "中性")
    total = sentiment.get("total_news", 0)

    topics = sentiment.get("main_topics", [])
    top_topic = topics[0][0] if topics else "综合"

    return f"{emoji} {company_name} 舆情: {overall} ({score}分) | 新闻{total}条 | 热点: {top_topic}"
