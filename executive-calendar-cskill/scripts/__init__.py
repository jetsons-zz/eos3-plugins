"""
Executive Calendar - 高管日程智囊
跨时区会议安排、日程优化
"""

from .timezone_manager import (
    get_city_time,
    convert_time,
    get_time_difference,
    get_business_hours_overlap,
    CITY_TIMEZONES
)

from .meeting_scheduler import (
    find_optimal_meeting_time,
    suggest_meeting_slots,
    calculate_meeting_fatigue,
    get_meeting_recommendations
)

from .calendar_manager import (
    add_event,
    get_today_agenda,
    get_week_agenda,
    check_conflicts,
    get_free_slots,
    clear_calendar
)

from .reminder_engine import (
    generate_meeting_prep,
    get_travel_reminder,
    get_timezone_alert,
    generate_daily_briefing
)

from .calendar_report import (
    generate_daily_schedule,
    generate_week_overview,
    generate_meeting_summary,
    analyze_time_allocation
)

__all__ = [
    # Timezone
    'get_city_time',
    'convert_time',
    'get_time_difference',
    'get_business_hours_overlap',
    'CITY_TIMEZONES',
    # Meeting
    'find_optimal_meeting_time',
    'suggest_meeting_slots',
    'calculate_meeting_fatigue',
    'get_meeting_recommendations',
    # Calendar
    'add_event',
    'get_today_agenda',
    'get_week_agenda',
    'check_conflicts',
    'get_free_slots',
    'clear_calendar',
    # Reminder
    'generate_meeting_prep',
    'get_travel_reminder',
    'get_timezone_alert',
    'generate_daily_briefing',
    # Report
    'generate_daily_schedule',
    'generate_week_overview',
    'generate_meeting_summary',
    'analyze_time_allocation'
]
