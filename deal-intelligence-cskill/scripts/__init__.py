"""
Deal Intelligence - 商业尽调助手
帮助高管进行商业尽职调查
"""

from .company_info import (
    get_company_profile,
    get_company_financials,
    search_companies,
    get_executive_team
)

from .funding_analyzer import (
    get_funding_history,
    analyze_funding_trajectory,
    get_investor_info,
    estimate_valuation
)

from .hiring_tracker import (
    get_hiring_activity,
    analyze_growth_signals,
    get_department_breakdown,
    track_key_hires
)

from .news_aggregator import (
    get_company_news,
    get_industry_news,
    sentiment_analysis,
    get_press_releases
)

from .risk_scanner import (
    scan_legal_risks,
    scan_financial_risks,
    scan_reputation_risks,
    get_risk_score
)

from .due_diligence_report import (
    generate_quick_profile,
    generate_investment_memo,
    generate_full_dd_report,
    compare_companies
)

__all__ = [
    # Company Info
    'get_company_profile',
    'get_company_financials',
    'search_companies',
    'get_executive_team',
    # Funding
    'get_funding_history',
    'analyze_funding_trajectory',
    'get_investor_info',
    'estimate_valuation',
    # Hiring
    'get_hiring_activity',
    'analyze_growth_signals',
    'get_department_breakdown',
    'track_key_hires',
    # News
    'get_company_news',
    'get_industry_news',
    'sentiment_analysis',
    'get_press_releases',
    # Risk
    'scan_legal_risks',
    'scan_financial_risks',
    'scan_reputation_risks',
    'get_risk_score',
    # Reports
    'generate_quick_profile',
    'generate_investment_memo',
    'generate_full_dd_report',
    'compare_companies'
]
