"""
AI Quant Trader Pro - 智能量化交易系统
大模型驱动的专业级交易决策支持
"""

# Market Analysis
from .market_analyzer import (
    MarketAnalyzer,
    analyze_stock,
    calculate_technical_indicators,
    detect_patterns,
    analyze_trend,
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_kdj
)

# Sentiment Analysis
from .sentiment_analyzer import (
    SentimentAnalyzer,
    analyze_news_sentiment,
    get_market_sentiment,
    analyze_insider_activity,
    get_analyst_ratings
)

# Alpha Generation
from .alpha_generator import (
    AlphaGenerator,
    generate_alpha_signals,
    run_factor_model,
    screen_stocks,
    find_similar_stocks
)

# Risk Management
from .risk_manager import (
    RiskManager,
    calculate_position_size,
    calculate_var,
    set_stop_loss,
    analyze_portfolio_risk
)

# Backtesting
from .backtester import (
    Backtester,
    backtest_strategy,
    analyze_performance,
    compare_strategies,
    optimize_parameters
)

# Report Generation
from .report_generator import (
    generate_trading_report,
    generate_watchlist_report,
    generate_portfolio_report,
    get_ai_recommendation
)

__all__ = [
    # Market Analysis
    'MarketAnalyzer',
    'analyze_stock',
    'calculate_technical_indicators',
    'detect_patterns',
    'analyze_trend',
    'calculate_sma',
    'calculate_ema',
    'calculate_rsi',
    'calculate_macd',
    'calculate_bollinger_bands',
    'calculate_kdj',

    # Sentiment Analysis
    'SentimentAnalyzer',
    'analyze_news_sentiment',
    'get_market_sentiment',
    'analyze_insider_activity',
    'get_analyst_ratings',

    # Alpha Generation
    'AlphaGenerator',
    'generate_alpha_signals',
    'run_factor_model',
    'screen_stocks',
    'find_similar_stocks',

    # Risk Management
    'RiskManager',
    'calculate_position_size',
    'calculate_var',
    'set_stop_loss',
    'analyze_portfolio_risk',

    # Backtesting
    'Backtester',
    'backtest_strategy',
    'analyze_performance',
    'compare_strategies',
    'optimize_parameters',

    # Reports
    'generate_trading_report',
    'generate_watchlist_report',
    'generate_portfolio_report',
    'get_ai_recommendation'
]

__version__ = '1.0.0'
__author__ = 'Agent-Skill-Creator'
