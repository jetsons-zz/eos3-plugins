"""
Company Info Module - 企业信息模块
获取企业基本信息、财务数据、高管团队
"""

from typing import Dict, List, Optional
from datetime import datetime

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


# 常见公司名称到股票代码的映射
COMPANY_TICKERS = {
    # 中国科技
    "腾讯": "0700.HK",
    "阿里巴巴": "BABA",
    "阿里": "BABA",
    "京东": "JD",
    "百度": "BIDU",
    "网易": "NTES",
    "拼多多": "PDD",
    "美团": "3690.HK",
    "小米": "1810.HK",
    "比亚迪": "1211.HK",
    "字节跳动": "PRIVATE",

    # 美国科技
    "苹果": "AAPL",
    "apple": "AAPL",
    "微软": "MSFT",
    "microsoft": "MSFT",
    "谷歌": "GOOGL",
    "google": "GOOGL",
    "亚马逊": "AMZN",
    "amazon": "AMZN",
    "特斯拉": "TSLA",
    "tesla": "TSLA",
    "英伟达": "NVDA",
    "nvidia": "NVDA",
    "meta": "META",
    "脸书": "META",
    "奈飞": "NFLX",
    "netflix": "NFLX",

    # 金融
    "摩根大通": "JPM",
    "高盛": "GS",
    "花旗": "C",
    "伯克希尔": "BRK-B",

    # 其他
    "可口可乐": "KO",
    "麦当劳": "MCD",
    "星巴克": "SBUX",
    "耐克": "NKE",
    "沃尔玛": "WMT",
}


# 私有公司数据库（模拟）
PRIVATE_COMPANY_DB = {
    "字节跳动": {
        "name": "字节跳动",
        "name_en": "ByteDance",
        "founded": "2012",
        "headquarters": "北京",
        "industry": "互联网/社交媒体",
        "products": ["抖音", "TikTok", "今日头条", "飞书"],
        "employees": "150,000+",
        "valuation": "$220B (2023估值)",
        "status": "私有",
        "founder": "张一鸣",
        "description": "全球最大的独角兽企业，旗下拥有抖音、TikTok等短视频平台"
    },
    "spacex": {
        "name": "SpaceX",
        "name_en": "Space Exploration Technologies Corp",
        "founded": "2002",
        "headquarters": "美国加州霍桑",
        "industry": "航空航天",
        "products": ["Falcon 9", "Starship", "Starlink"],
        "employees": "13,000+",
        "valuation": "$180B (2024估值)",
        "status": "私有",
        "founder": "Elon Musk",
        "description": "私人航天公司，可重复使用火箭技术领导者"
    },
    "openai": {
        "name": "OpenAI",
        "name_en": "OpenAI",
        "founded": "2015",
        "headquarters": "美国旧金山",
        "industry": "人工智能",
        "products": ["GPT-4", "ChatGPT", "DALL-E", "Codex"],
        "employees": "1,500+",
        "valuation": "$157B (2024估值)",
        "status": "私有",
        "founder": "Sam Altman, Greg Brockman, Ilya Sutskever",
        "description": "领先的AI研究公司，ChatGPT开发者"
    },
    "anthropic": {
        "name": "Anthropic",
        "name_en": "Anthropic",
        "founded": "2021",
        "headquarters": "美国旧金山",
        "industry": "人工智能",
        "products": ["Claude", "Constitutional AI"],
        "employees": "500+",
        "valuation": "$61B (2024估值)",
        "status": "私有",
        "founder": "Dario Amodei, Daniela Amodei",
        "description": "AI安全公司，Claude AI开发者"
    }
}


def resolve_ticker(company_name: str) -> Optional[str]:
    """解析公司名称到股票代码"""
    name_lower = company_name.lower().strip()

    # 直接匹配
    if name_lower in COMPANY_TICKERS:
        return COMPANY_TICKERS[name_lower]
    if company_name in COMPANY_TICKERS:
        return COMPANY_TICKERS[company_name]

    # 可能已经是股票代码
    if company_name.upper() in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]:
        return company_name.upper()

    # 检查是否包含关键词
    for key, ticker in COMPANY_TICKERS.items():
        if key in name_lower or name_lower in key:
            return ticker

    # 返回原样（假设是股票代码）
    return company_name.upper()


def get_company_profile(company_name: str) -> Dict:
    """
    获取公司基本资料

    Args:
        company_name: 公司名称或股票代码

    Returns:
        公司资料字典
    """
    # 检查私有公司数据库
    name_lower = company_name.lower()
    for key, data in PRIVATE_COMPANY_DB.items():
        if key in name_lower or name_lower in key or company_name in data.get("name", ""):
            return {
                "status": "success",
                "is_public": False,
                "data": data
            }

    # 尝试获取上市公司数据
    if not HAS_YFINANCE:
        return {
            "status": "error",
            "message": "需要安装 yfinance: pip install yfinance"
        }

    ticker = resolve_ticker(company_name)
    if ticker == "PRIVATE":
        return {
            "status": "error",
            "message": f"{company_name} 是私有公司，无公开交易数据"
        }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or info.get("regularMarketPrice") is None:
            return {
                "status": "error",
                "message": f"未找到 {company_name} 的信息"
            }

        profile = {
            "name": info.get("shortName") or info.get("longName", company_name),
            "ticker": ticker,
            "industry": info.get("industry", "N/A"),
            "sector": info.get("sector", "N/A"),
            "headquarters": f"{info.get('city', '')}, {info.get('country', '')}",
            "website": info.get("website", "N/A"),
            "employees": info.get("fullTimeEmployees", "N/A"),
            "description": info.get("longBusinessSummary", "")[:500] + "..." if info.get("longBusinessSummary") else "N/A",
            "market_cap": info.get("marketCap", 0),
            "market_cap_formatted": format_market_cap(info.get("marketCap", 0)),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", "N/A"),
            "current_price": info.get("regularMarketPrice", 0),
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            "founded": "N/A",  # yfinance doesn't provide founding date
            "ceo": info.get("companyOfficers", [{}])[0].get("name", "N/A") if info.get("companyOfficers") else "N/A"
        }

        return {
            "status": "success",
            "is_public": True,
            "data": profile
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"获取数据失败: {str(e)}"
        }


def format_market_cap(value: float) -> str:
    """格式化市值"""
    if value >= 1e12:
        return f"${value/1e12:.2f}万亿"
    elif value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.0f}"


def get_company_financials(company_name: str) -> Dict:
    """
    获取公司财务数据

    Args:
        company_name: 公司名称或股票代码

    Returns:
        财务数据字典
    """
    if not HAS_YFINANCE:
        return {
            "status": "error",
            "message": "需要安装 yfinance"
        }

    ticker = resolve_ticker(company_name)
    if ticker == "PRIVATE":
        return {
            "status": "error",
            "message": f"{company_name} 是私有公司，无公开财务数据"
        }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        financials = {
            "company": info.get("shortName", company_name),
            "ticker": ticker,
            "currency": info.get("currency", "USD"),

            # 估值指标
            "valuation": {
                "market_cap": info.get("marketCap", 0),
                "market_cap_formatted": format_market_cap(info.get("marketCap", 0)),
                "enterprise_value": info.get("enterpriseValue", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "forward_pe": info.get("forwardPE", 0),
                "pb_ratio": info.get("priceToBook", 0),
                "ps_ratio": info.get("priceToSalesTrailing12Months", 0),
            },

            # 盈利能力
            "profitability": {
                "revenue": info.get("totalRevenue", 0),
                "revenue_formatted": format_market_cap(info.get("totalRevenue", 0)),
                "gross_margin": f"{info.get('grossMargins', 0)*100:.1f}%" if info.get('grossMargins') else "N/A",
                "operating_margin": f"{info.get('operatingMargins', 0)*100:.1f}%" if info.get('operatingMargins') else "N/A",
                "profit_margin": f"{info.get('profitMargins', 0)*100:.1f}%" if info.get('profitMargins') else "N/A",
                "roe": f"{info.get('returnOnEquity', 0)*100:.1f}%" if info.get('returnOnEquity') else "N/A",
                "roa": f"{info.get('returnOnAssets', 0)*100:.1f}%" if info.get('returnOnAssets') else "N/A",
            },

            # 增长指标
            "growth": {
                "revenue_growth": f"{info.get('revenueGrowth', 0)*100:.1f}%" if info.get('revenueGrowth') else "N/A",
                "earnings_growth": f"{info.get('earningsGrowth', 0)*100:.1f}%" if info.get('earningsGrowth') else "N/A",
            },

            # 财务健康
            "financial_health": {
                "total_cash": info.get("totalCash", 0),
                "total_cash_formatted": format_market_cap(info.get("totalCash", 0)),
                "total_debt": info.get("totalDebt", 0),
                "total_debt_formatted": format_market_cap(info.get("totalDebt", 0)),
                "debt_to_equity": info.get("debtToEquity", 0),
                "current_ratio": info.get("currentRatio", 0),
                "quick_ratio": info.get("quickRatio", 0),
            },

            # 分红
            "dividend": {
                "dividend_yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A",
                "dividend_rate": info.get("dividendRate", 0),
                "payout_ratio": f"{info.get('payoutRatio', 0)*100:.1f}%" if info.get('payoutRatio') else "N/A",
            },

            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        return {
            "status": "success",
            "data": financials
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"获取财务数据失败: {str(e)}"
        }


def search_companies(keyword: str, limit: int = 10) -> Dict:
    """
    搜索公司

    Args:
        keyword: 搜索关键词
        limit: 返回数量限制

    Returns:
        匹配的公司列表
    """
    results = []
    keyword_lower = keyword.lower()

    # 搜索映射表
    for name, ticker in COMPANY_TICKERS.items():
        if keyword_lower in name.lower() or keyword_lower in ticker.lower():
            results.append({
                "name": name,
                "ticker": ticker,
                "type": "上市公司"
            })

    # 搜索私有公司
    for key, data in PRIVATE_COMPANY_DB.items():
        if keyword_lower in key or keyword_lower in data.get("name", "").lower():
            results.append({
                "name": data.get("name"),
                "ticker": "私有",
                "type": "私有公司",
                "industry": data.get("industry", "")
            })

    return {
        "status": "success",
        "query": keyword,
        "count": len(results[:limit]),
        "results": results[:limit]
    }


def get_executive_team(company_name: str) -> Dict:
    """
    获取高管团队信息

    Args:
        company_name: 公司名称

    Returns:
        高管团队信息
    """
    if not HAS_YFINANCE:
        return {
            "status": "error",
            "message": "需要安装 yfinance"
        }

    ticker = resolve_ticker(company_name)
    if ticker == "PRIVATE":
        # 返回私有公司的创始人信息
        for key, data in PRIVATE_COMPANY_DB.items():
            if company_name.lower() in key or key in company_name.lower():
                return {
                    "status": "success",
                    "company": data.get("name"),
                    "executives": [
                        {
                            "name": data.get("founder", "N/A"),
                            "title": "创始人",
                            "age": "N/A",
                            "compensation": "N/A"
                        }
                    ]
                }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        officers = info.get("companyOfficers", [])
        executives = []

        for officer in officers[:10]:  # 最多10位高管
            executives.append({
                "name": officer.get("name", "N/A"),
                "title": officer.get("title", "N/A"),
                "age": officer.get("age", "N/A"),
                "compensation": format_market_cap(officer.get("totalPay", 0)) if officer.get("totalPay") else "N/A",
                "since": officer.get("fiscalYear", "N/A")
            })

        return {
            "status": "success",
            "company": info.get("shortName", company_name),
            "ticker": ticker,
            "executive_count": len(executives),
            "executives": executives
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"获取高管信息失败: {str(e)}"
        }
