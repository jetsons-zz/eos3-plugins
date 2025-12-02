"""
Global Market Pulse - 全球股市快报
为高净值人群和企业高管提供全球主要股指实时行情
"""

from .market_client import MarketClient, get_market_summary, get_index_quote
from .market_analyzer import (
    analyze_market_sentiment,
    get_sector_performance,
    get_market_movers
)
from .report_generator import (
    generate_market_brief,
    generate_executive_summary,
    format_market_table
)

__all__ = [
    'MarketClient',
    'get_market_summary',
    'get_index_quote',
    'analyze_market_sentiment',
    'get_sector_performance',
    'get_market_movers',
    'generate_market_brief',
    'generate_executive_summary',
    'format_market_table'
]

__version__ = '1.0.0'
