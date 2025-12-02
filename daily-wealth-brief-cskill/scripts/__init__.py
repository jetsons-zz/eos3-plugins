"""
Daily Wealth Brief - 每日财富简报
高管个性化早间财经简报
"""

from .market_pulse import (
    get_market_overview,
    get_index_snapshot,
    get_crypto_snapshot,
    get_commodity_snapshot,
    get_forex_snapshot,
    get_market_movers
)

from .portfolio_snapshot import (
    get_portfolio_summary,
    get_holdings_performance,
    get_alerts,
    get_dividend_calendar
)

from .news_curator import (
    get_top_headlines,
    get_market_news,
    get_sector_news,
    curate_for_interests
)

from .calendar_digest import (
    get_economic_calendar,
    get_earnings_calendar,
    get_personal_highlights,
    get_market_hours
)

from .briefing_generator import (
    generate_morning_brief,
    generate_quick_brief,
    generate_market_alert,
    generate_weekly_review
)

__all__ = [
    # Market
    'get_market_overview',
    'get_index_snapshot',
    'get_crypto_snapshot',
    'get_commodity_snapshot',
    'get_forex_snapshot',
    'get_market_movers',
    # Portfolio
    'get_portfolio_summary',
    'get_holdings_performance',
    'get_alerts',
    'get_dividend_calendar',
    # News
    'get_top_headlines',
    'get_market_news',
    'get_sector_news',
    'curate_for_interests',
    # Calendar
    'get_economic_calendar',
    'get_earnings_calendar',
    'get_personal_highlights',
    'get_market_hours',
    # Briefing
    'generate_morning_brief',
    'generate_quick_brief',
    'generate_market_alert',
    'generate_weekly_review'
]
