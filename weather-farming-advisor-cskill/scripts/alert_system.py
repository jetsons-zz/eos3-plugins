"""
Alert System Module
Detects weather alerts affecting farming operations.
"""

from typing import Dict, List, Optional
from datetime import datetime


# Alert thresholds
ALERT_THRESHOLDS = {
    "frost": {
        "watch": 2,      # °C - frost watch
        "warning": 0,    # °C - frost warning
        "emergency": -5  # °C - severe frost
    },
    "heat": {
        "watch": 32,     # °C - heat watch
        "warning": 35,   # °C - heat warning
        "emergency": 40  # °C - extreme heat
    },
    "drought": {
        "days_dry": 5,   # consecutive days without significant rain
        "rain_threshold": 2  # mm - considered "dry" day
    },
    "flood": {
        "watch": 25,     # mm in 24h
        "warning": 50,   # mm in 24h
        "emergency": 100 # mm in 24h
    },
    "wind": {
        "watch": 40,     # km/h
        "warning": 60,   # km/h
        "emergency": 80  # km/h
    }
}


def check_weather_alerts(
    weather_data: Dict,
    soil_data: Optional[Dict] = None,
    crop_name: Optional[str] = None
) -> List[Dict]:
    """
    Check for weather alerts affecting farming operations.

    Args:
        weather_data: Weather forecast data from get_weather_forecast()
        soil_data: Optional soil conditions data
        crop_name: Optional crop for specific alerts

    Returns:
        List of alert dicts, each containing:
        - type: "frost", "drought", "heat", "flood", "wind"
        - severity: "watch", "warning", "emergency"
        - start_date: Alert start date
        - end_date: Alert end date
        - message: Human-readable alert message
        - recommended_action: Suggested protective measures
    """
    alerts = []
    daily = weather_data.get("daily", [])

    if not daily:
        return alerts

    # Check for frost alerts
    frost_alerts = _check_frost(daily, crop_name)
    alerts.extend(frost_alerts)

    # Check for heat alerts
    heat_alerts = _check_heat(daily, crop_name)
    alerts.extend(heat_alerts)

    # Check for drought conditions
    drought_alerts = _check_drought(daily, soil_data)
    alerts.extend(drought_alerts)

    # Check for flood risk
    flood_alerts = _check_flood(daily)
    alerts.extend(flood_alerts)

    # Check for wind alerts
    wind_alerts = _check_wind(daily)
    alerts.extend(wind_alerts)

    # Sort by severity (emergency first)
    severity_order = {"emergency": 0, "warning": 1, "watch": 2}
    alerts.sort(key=lambda x: severity_order.get(x.get("severity", "watch"), 3))

    return alerts


def _check_frost(daily: List[Dict], crop_name: Optional[str] = None) -> List[Dict]:
    """Check for frost alerts."""
    alerts = []
    thresholds = ALERT_THRESHOLDS["frost"]

    frost_days = []
    for day in daily:
        min_temp = day.get("temp_min")
        if min_temp is not None:
            if min_temp <= thresholds["emergency"]:
                frost_days.append((day.get("date"), min_temp, "emergency"))
            elif min_temp <= thresholds["warning"]:
                frost_days.append((day.get("date"), min_temp, "warning"))
            elif min_temp <= thresholds["watch"]:
                frost_days.append((day.get("date"), min_temp, "watch"))

    if frost_days:
        # Group consecutive days
        max_severity = max(d[2] for d in frost_days)
        min_temp_overall = min(d[1] for d in frost_days)
        dates = [d[0] for d in frost_days]

        if max_severity == "emergency":
            message = f"SEVERE FROST: Temperatures dropping to {min_temp_overall}°C"
            action = "Harvest sensitive crops immediately. Heavy frost protection required for all plants."
        elif max_severity == "warning":
            message = f"FROST WARNING: Overnight lows near {min_temp_overall}°C"
            action = "Cover frost-sensitive crops with fabric or plastic. Irrigate soil before sunset to retain heat."
        else:
            message = f"FROST WATCH: Cool nights expected, lows around {min_temp_overall}°C"
            action = "Monitor forecast. Prepare frost protection materials."

        if crop_name:
            message += f" (Affects {crop_name} planting/growth)"

        alerts.append({
            "type": "frost",
            "severity": max_severity,
            "affected_dates": dates,
            "start_date": dates[0] if dates else None,
            "end_date": dates[-1] if dates else None,
            "temperature": min_temp_overall,
            "message": message,
            "recommended_action": action
        })

    return alerts


def _check_heat(daily: List[Dict], crop_name: Optional[str] = None) -> List[Dict]:
    """Check for heat alerts."""
    alerts = []
    thresholds = ALERT_THRESHOLDS["heat"]

    heat_days = []
    for day in daily:
        max_temp = day.get("temp_max")
        if max_temp is not None:
            if max_temp >= thresholds["emergency"]:
                heat_days.append((day.get("date"), max_temp, "emergency"))
            elif max_temp >= thresholds["warning"]:
                heat_days.append((day.get("date"), max_temp, "warning"))
            elif max_temp >= thresholds["watch"]:
                heat_days.append((day.get("date"), max_temp, "watch"))

    if heat_days:
        max_severity = max(d[2] for d in heat_days)
        max_temp_overall = max(d[1] for d in heat_days)
        dates = [d[0] for d in heat_days]

        if max_severity == "emergency":
            message = f"EXTREME HEAT: Temperatures reaching {max_temp_overall}°C"
            action = "Provide shade for crops. Increase irrigation significantly. Avoid working during peak heat."
        elif max_severity == "warning":
            message = f"HEAT WARNING: High temperatures around {max_temp_overall}°C"
            action = "Mulch heavily to retain soil moisture. Water early morning or evening."
        else:
            message = f"HEAT WATCH: Warm conditions expected, up to {max_temp_overall}°C"
            action = "Monitor soil moisture closely. Prepare shade cloth if needed."

        alerts.append({
            "type": "heat",
            "severity": max_severity,
            "affected_dates": dates,
            "start_date": dates[0] if dates else None,
            "end_date": dates[-1] if dates else None,
            "temperature": max_temp_overall,
            "message": message,
            "recommended_action": action
        })

    return alerts


def _check_drought(daily: List[Dict], soil_data: Optional[Dict] = None) -> List[Dict]:
    """Check for drought conditions."""
    alerts = []
    thresholds = ALERT_THRESHOLDS["drought"]

    # Count consecutive dry days
    dry_days = 0
    for day in daily:
        if day.get("precipitation", 0) < thresholds["rain_threshold"]:
            dry_days += 1
        else:
            break  # Stop counting if rain is coming

    # Also check soil moisture if available
    low_moisture = False
    if soil_data:
        moisture = soil_data.get("moisture", {}).get("root_zone_average", 0.3)
        if moisture < 0.15:
            low_moisture = True

    if dry_days >= thresholds["days_dry"] or low_moisture:
        if dry_days >= 10 or (dry_days >= 7 and low_moisture):
            severity = "warning"
            message = f"DROUGHT CONDITIONS: {dry_days} dry days ahead, soil moisture critically low"
            action = "Deep water established plants. Prioritize essential crops. Consider drought-tolerant varieties."
        else:
            severity = "watch"
            message = f"DRY PERIOD: {dry_days} days with little rain expected"
            action = "Monitor soil moisture. Plan irrigation schedule."

        alerts.append({
            "type": "drought",
            "severity": severity,
            "dry_days_forecast": dry_days,
            "soil_moisture_low": low_moisture,
            "message": message,
            "recommended_action": action
        })

    return alerts


def _check_flood(daily: List[Dict]) -> List[Dict]:
    """Check for flood/heavy rain alerts."""
    alerts = []
    thresholds = ALERT_THRESHOLDS["flood"]

    for day in daily:
        precip = day.get("precipitation", 0)
        date = day.get("date")

        if precip >= thresholds["emergency"]:
            alerts.append({
                "type": "flood",
                "severity": "emergency",
                "date": date,
                "start_date": date,
                "end_date": date,
                "precipitation_mm": precip,
                "message": f"FLOOD RISK: Extreme rainfall {precip}mm expected on {date}",
                "recommended_action": "Clear drainage channels. Protect seedlings from washing out. Delay planting."
            })
        elif precip >= thresholds["warning"]:
            alerts.append({
                "type": "flood",
                "severity": "warning",
                "date": date,
                "start_date": date,
                "end_date": date,
                "precipitation_mm": precip,
                "message": f"HEAVY RAIN: {precip}mm expected on {date}",
                "recommended_action": "Ensure good drainage. Avoid heavy field work before rain."
            })
        elif precip >= thresholds["watch"]:
            alerts.append({
                "type": "flood",
                "severity": "watch",
                "date": date,
                "start_date": date,
                "end_date": date,
                "precipitation_mm": precip,
                "message": f"RAIN WATCH: Significant rainfall {precip}mm on {date}",
                "recommended_action": "Postpone irrigation. Plan for wet field conditions."
            })

    return alerts


def _check_wind(daily: List[Dict]) -> List[Dict]:
    """Check for wind alerts."""
    alerts = []
    thresholds = ALERT_THRESHOLDS["wind"]

    wind_days = []
    for day in daily:
        wind = day.get("wind_speed", 0)
        if wind >= thresholds["emergency"]:
            wind_days.append((day.get("date"), wind, "emergency"))
        elif wind >= thresholds["warning"]:
            wind_days.append((day.get("date"), wind, "warning"))
        elif wind >= thresholds["watch"]:
            wind_days.append((day.get("date"), wind, "watch"))

    if wind_days:
        max_severity = max(d[2] for d in wind_days)
        max_wind = max(d[1] for d in wind_days)
        dates = [d[0] for d in wind_days]

        if max_severity == "emergency":
            message = f"SEVERE WIND: Gusts up to {max_wind}km/h expected"
            action = "Secure all structures. Stake tall plants. Harvest ripe crops if possible."
        elif max_severity == "warning":
            message = f"HIGH WIND: Wind speeds reaching {max_wind}km/h"
            action = "Secure row covers and plastic. Support tall crops. Postpone spraying."
        else:
            message = f"WIND WATCH: Breezy conditions with {max_wind}km/h winds"
            action = "Check plant supports. Avoid spraying pesticides."

        alerts.append({
            "type": "wind",
            "severity": max_severity,
            "affected_dates": dates,
            "start_date": dates[0] if dates else None,
            "end_date": dates[-1] if dates else None,
            "wind_speed": max_wind,
            "message": message,
            "recommended_action": action
        })

    return alerts


def format_alerts_summary(alerts: List[Dict]) -> str:
    """
    Format alerts into human-readable summary.

    Args:
        alerts: List of alert dicts

    Returns:
        Formatted string summary
    """
    if not alerts:
        return "No active weather alerts. Conditions favorable for farming."

    lines = ["ACTIVE WEATHER ALERTS:", "=" * 40]

    severity_icons = {
        "emergency": "🚨",
        "warning": "⚠️",
        "watch": "👁️"
    }

    for alert in alerts:
        icon = severity_icons.get(alert.get("severity", "watch"), "ℹ️")
        severity = alert.get("severity", "watch").upper()
        msg = alert.get("message", "Alert")
        action = alert.get("recommended_action", "Monitor conditions")

        lines.append(f"\n{icon} [{severity}] {msg}")
        lines.append(f"   Action: {action}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test alert system
    print("Testing Alert System...")

    # Mock weather data with various conditions
    mock_weather = {
        "daily": [
            {"date": "2025-01-15", "temp_max": 8, "temp_min": -2, "precipitation": 0, "wind_speed": 25},
            {"date": "2025-01-16", "temp_max": 10, "temp_min": 1, "precipitation": 55, "wind_speed": 45},
            {"date": "2025-01-17", "temp_max": 12, "temp_min": 3, "precipitation": 0, "wind_speed": 20},
        ]
    }

    alerts = check_weather_alerts(mock_weather)
    print(f"\nFound {len(alerts)} alerts:")
    for alert in alerts:
        print(f"  - {alert['type']}: {alert['severity']} - {alert['message']}")

    print("\n" + format_alerts_summary(alerts))
