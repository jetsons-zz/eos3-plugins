"""
Portfolio Pulse - 全球资产仪表盘
股票+加密+贵金属+汇率 综合资产分析
"""

from .portfolio_manager import (
    Portfolio,
    add_holding,
    get_portfolio_value,
    get_portfolio_performance
)
from .asset_tracker import (
    get_stock_price,
    get_crypto_price,
    get_commodity_price,
    get_multi_asset_prices
)
from .risk_analyzer import (
    calculate_portfolio_risk,
    get_diversification_score,
    get_rebalance_suggestions
)
from .report_generator import (
    generate_portfolio_report,
    generate_performance_summary,
    generate_wealth_snapshot
)

__all__ = [
    'Portfolio',
    'add_holding',
    'get_portfolio_value',
    'get_portfolio_performance',
    'get_stock_price',
    'get_crypto_price',
    'get_commodity_price',
    'get_multi_asset_prices',
    'calculate_portfolio_risk',
    'get_diversification_score',
    'get_rebalance_suggestions',
    'generate_portfolio_report',
    'generate_performance_summary',
    'generate_wealth_snapshot'
]

__version__ = '1.0.0'
