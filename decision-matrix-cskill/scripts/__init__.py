"""
Decision Matrix - 重大决策分析器
结构化决策分析框架
"""

from .decision_framer import (
    create_decision,
    get_decision,
    list_decisions,
    update_decision,
    delete_decision
)

from .option_generator import (
    add_option,
    remove_option,
    get_options,
    generate_options_from_template
)

from .criteria_manager import (
    add_criterion,
    remove_criterion,
    get_criteria,
    set_weights,
    normalize_weights
)

from .scoring_engine import (
    score_option,
    calculate_weighted_scores,
    rank_options,
    get_recommendation
)

from .analysis_tools import (
    sensitivity_analysis,
    pros_cons_analysis,
    risk_assessment,
    scenario_analysis
)

from .decision_report import (
    generate_quick_summary,
    generate_decision_matrix,
    generate_full_report,
    generate_executive_summary
)

__all__ = [
    # Decision
    'create_decision',
    'get_decision',
    'list_decisions',
    'update_decision',
    'delete_decision',
    # Options
    'add_option',
    'remove_option',
    'get_options',
    'generate_options_from_template',
    # Criteria
    'add_criterion',
    'remove_criterion',
    'get_criteria',
    'set_weights',
    'normalize_weights',
    # Scoring
    'score_option',
    'calculate_weighted_scores',
    'rank_options',
    'get_recommendation',
    # Analysis
    'sensitivity_analysis',
    'pros_cons_analysis',
    'risk_assessment',
    'scenario_analysis',
    # Report
    'generate_quick_summary',
    'generate_decision_matrix',
    'generate_full_report',
    'generate_executive_summary'
]
