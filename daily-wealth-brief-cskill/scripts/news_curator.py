"""
News Curator Module - 新闻策展模块
智能筛选财经新闻
"""

from datetime import datetime
from typing import Dict, List, Optional

# 模拟新闻数据库
NEWS_DATABASE = {
    "headlines": [
        {
            "id": 1,
            "title": "美联储维持利率不变，暗示2025年降息放缓",
            "source": "华尔街日报",
            "category": "央行政策",
            "importance": "high",
            "summary": "美联储在最新议息会议后宣布维持基准利率在4.25%-4.5%区间，同时下调2025年降息预期至2次。",
            "impact": "利空债券，利好美元"
        },
        {
            "id": 2,
            "title": "英伟达发布新一代AI芯片，性能提升3倍",
            "source": "彭博社",
            "category": "科技",
            "importance": "high",
            "summary": "英伟达CEO黄仁勋在GTC大会上发布Blackwell Ultra芯片，算力达到前代3倍，售价5万美元起。",
            "impact": "利好NVDA及AI板块"
        },
        {
            "id": 3,
            "title": "中国11月PMI回升至50.3，制造业重返扩张",
            "source": "财新",
            "category": "宏观经济",
            "importance": "medium",
            "summary": "中国官方制造业PMI连续第三个月回升，显示经济政策刺激效果显现。",
            "impact": "利好A股及人民币"
        },
        {
            "id": 4,
            "title": "比特币突破10万美元创历史新高",
            "source": "CoinDesk",
            "category": "加密货币",
            "importance": "high",
            "summary": "比特币价格突破10万美元心理关口，市场情绪高涨，机构投资者持续入场。",
            "impact": "加密市场整体走强"
        },
        {
            "id": 5,
            "title": "欧佩克+确认2025年产量计划不变",
            "source": "路透社",
            "category": "能源",
            "importance": "medium",
            "summary": "欧佩克+部长级会议决定维持现有减产政策，2025年逐步恢复产量。",
            "impact": "油价短期承压"
        },
        {
            "id": 6,
            "title": "特斯拉上海工厂产能提升至120万辆",
            "source": "第一财经",
            "category": "汽车",
            "importance": "medium",
            "summary": "特斯拉上海超级工厂完成产线升级，年产能提升20%，新增储能产品生产线。",
            "impact": "利好TSLA"
        }
    ],
    "market_news": [
        {"title": "A股三大指数集体高开", "category": "股市"},
        {"title": "港股恒生指数涨超1%", "category": "股市"},
        {"title": "美股期货小幅走高", "category": "股市"},
        {"title": "黄金价格创一周新高", "category": "商品"},
        {"title": "人民币中间价上调150点", "category": "外汇"}
    ],
    "sector_news": {
        "科技": [
            "苹果Vision Pro销量不及预期，股价承压",
            "微软Copilot企业用户突破5000万",
            "AMD发布新款AI芯片对标英伟达"
        ],
        "金融": [
            "高盛2024年交易收入创新高",
            "摩根大通上调中国银行股评级",
            "花旗宣布新一轮裁员计划"
        ],
        "消费": [
            "星巴克中国推出全新门店模式",
            "耐克下调全年营收指引",
            "奢侈品巨头LVMH股价创年内新低"
        ],
        "医疗": [
            "诺和诺德减肥药销售额破百亿",
            "辉瑞裁撤多个研发项目",
            "强生完成医疗器械分拆"
        ]
    }
}


def get_top_headlines(limit: int = 5) -> Dict:
    """
    获取头条新闻

    Args:
        limit: 返回数量

    Returns:
        头条新闻列表
    """
    headlines = NEWS_DATABASE.get("headlines", [])[:limit]

    # 按重要性排序
    importance_order = {"high": 0, "medium": 1, "low": 2}
    headlines = sorted(headlines, key=lambda x: importance_order.get(x.get("importance", "low"), 2))[:limit]

    return {
        "status": "success",
        "count": len(headlines),
        "headlines": headlines,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_market_news(limit: int = 10) -> Dict:
    """
    获取市场快讯

    Args:
        limit: 返回数量

    Returns:
        市场快讯
    """
    news = NEWS_DATABASE.get("market_news", [])[:limit]

    return {
        "status": "success",
        "count": len(news),
        "news": news,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_sector_news(sector: str) -> Dict:
    """
    获取行业新闻

    Args:
        sector: 行业名称

    Returns:
        行业新闻
    """
    sector_news = NEWS_DATABASE.get("sector_news", {})

    if sector in sector_news:
        news = sector_news[sector]
    else:
        # 模糊匹配
        for key, value in sector_news.items():
            if sector in key or key in sector:
                news = value
                sector = key
                break
        else:
            return {
                "status": "not_found",
                "message": f"未找到 {sector} 行业的新闻",
                "available_sectors": list(sector_news.keys())
            }

    return {
        "status": "success",
        "sector": sector,
        "news": news,
        "count": len(news),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def curate_for_interests(interests: List[str]) -> Dict:
    """
    根据兴趣策展新闻

    Args:
        interests: 兴趣标签列表 (如 ["AI", "加密货币", "中国经济"])

    Returns:
        个性化新闻
    """
    all_news = NEWS_DATABASE.get("headlines", [])
    sector_news = NEWS_DATABASE.get("sector_news", {})

    curated = []

    # 根据兴趣筛选头条
    for news in all_news:
        title = news.get("title", "").lower()
        category = news.get("category", "").lower()
        summary = news.get("summary", "").lower()

        for interest in interests:
            interest_lower = interest.lower()
            if interest_lower in title or interest_lower in category or interest_lower in summary:
                if news not in curated:
                    curated.append({
                        "type": "headline",
                        "matched_interest": interest,
                        **news
                    })
                break

    # 根据兴趣添加行业新闻
    interest_to_sector = {
        "AI": "科技",
        "人工智能": "科技",
        "芯片": "科技",
        "科技股": "科技",
        "银行": "金融",
        "保险": "金融",
        "金融": "金融",
        "消费": "消费",
        "零售": "消费",
        "医疗": "医疗",
        "医药": "医疗"
    }

    for interest in interests:
        sector = interest_to_sector.get(interest)
        if sector and sector in sector_news:
            for news in sector_news[sector][:2]:
                curated.append({
                    "type": "sector",
                    "matched_interest": interest,
                    "sector": sector,
                    "title": news
                })

    return {
        "status": "success",
        "interests": interests,
        "curated_count": len(curated),
        "curated_news": curated,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def generate_news_summary() -> str:
    """
    生成新闻摘要

    Returns:
        格式化的新闻摘要
    """
    headlines = get_top_headlines(3)
    market = get_market_news(3)

    lines = []
    lines.append("📰 今日财经要闻")
    lines.append("-" * 40)

    for news in headlines.get("headlines", []):
        importance = news.get("importance", "")
        emoji = "🔴" if importance == "high" else "🟡" if importance == "medium" else "🟢"
        lines.append(f"{emoji} {news.get('title', '')}")
        lines.append(f"   └ {news.get('summary', '')[:50]}...")
        lines.append("")

    lines.append("📊 市场快讯")
    lines.append("-" * 40)
    for news in market.get("news", []):
        lines.append(f"• {news.get('title', '')}")

    return "\n".join(lines)
