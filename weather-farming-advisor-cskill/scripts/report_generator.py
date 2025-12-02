"""
Report Generator Module
Generates comprehensive agricultural reports combining all analyses.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .weather_client import get_weather_forecast, get_soil_conditions
from .crop_advisor import calculate_crop_suitability, get_irrigation_advice, get_crop_info, list_available_crops
from .alert_system import check_weather_alerts, format_alerts_summary


def comprehensive_agricultural_report(
    latitude: float,
    longitude: float,
    crop_name: Optional[str] = None,
    location_name: Optional[str] = None
) -> Dict:
    """
    Generate comprehensive agricultural report combining ALL analyses.

    This is the "one-stop" function that users can call to get complete
    farming intelligence without knowing individual functions.

    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        crop_name: Optional specific crop for detailed analysis
        location_name: Optional human-readable location name

    Returns:
        Dict with ALL metrics consolidated:
        - location: Location metadata
        - generated_at: Timestamp
        - weather_forecast: 7-day forecast summary
        - soil_conditions: Temperature, moisture, workability
        - crop_analysis: Crop-specific analysis (if crop specified)
        - recommendations: Farming operation advice
        - alerts: Active weather alerts
        - summary: Overall insights
        - confidence: Data quality indicator

    Example:
        >>> report = comprehensive_agricultural_report(
        ...     40.7128, -74.0060,
        ...     crop_name="tomato",
        ...     location_name="New York Farm"
        ... )
        >>> print(report['summary'])
    """
    result = {
        "location": {
            "name": location_name or "Unknown Location",
            "latitude": latitude,
            "longitude": longitude,
            "coordinates": f"{latitude:.4f}°N, {abs(longitude):.4f}°{'W' if longitude < 0 else 'E'}"
        },
        "generated_at": datetime.now().isoformat(),
        "weather_forecast": None,
        "soil_conditions": None,
        "crop_analysis": None,
        "recommendations": {},
        "alerts": [],
        "summary": "",
        "confidence": 0.0,
        "errors": []
    }

    # Fetch weather data
    try:
        weather_data = get_weather_forecast(latitude, longitude, days=7)
        result["location"]["timezone"] = weather_data.get("location", {}).get("timezone", "Unknown")
        result["location"]["elevation"] = weather_data.get("location", {}).get("elevation")

        # Process weather forecast
        daily = weather_data.get("daily", [])
        summary_data = weather_data.get("summary", {})

        result["weather_forecast"] = {
            "period": f"{daily[0]['date']} to {daily[-1]['date']}" if daily else "N/A",
            "days": len(daily),
            "temperature_range": {
                "high": summary_data.get("temp_max_range", (None, None)),
                "low": summary_data.get("temp_min_range", (None, None))
            },
            "total_precipitation_mm": summary_data.get("total_precipitation", 0),
            "rainy_days": summary_data.get("rainy_days", 0),
            "frost_days": summary_data.get("frost_days", 0),
            "daily_forecasts": _format_daily_forecasts(daily)
        }
        result["confidence"] += 0.4

    except Exception as e:
        result["errors"].append(f"Weather data: {str(e)}")
        weather_data = {"daily": []}

    # Fetch soil data
    try:
        soil_data = get_soil_conditions(latitude, longitude)

        result["soil_conditions"] = {
            "temperature": soil_data.get("temperature", {}),
            "moisture": soil_data.get("moisture", {}),
            "workability_score": soil_data.get("workability_score", 0),
            "frost_risk": soil_data.get("frost_risk", False),
            "assessment": soil_data.get("assessment", "Unknown")
        }
        result["confidence"] += 0.3

    except Exception as e:
        result["errors"].append(f"Soil data: {str(e)}")
        soil_data = {}

    # Crop analysis (if specified)
    if crop_name:
        try:
            crop_suitability = calculate_crop_suitability(crop_name, weather_data, soil_data)

            if "error" not in crop_suitability:
                result["crop_analysis"] = {
                    "crop_name": crop_suitability.get("crop_name"),
                    "suitability_score": crop_suitability.get("overall_score"),
                    "recommendation": crop_suitability.get("recommendation"),
                    "component_scores": crop_suitability.get("component_scores"),
                    "limiting_factors": crop_suitability.get("limiting_factors"),
                    "optimal_window": crop_suitability.get("optimal_planting_window"),
                    "requirements": crop_suitability.get("crop_requirements"),
                    "notes": crop_suitability.get("notes")
                }

                # Get irrigation advice
                irrigation = get_irrigation_advice(crop_name, weather_data, soil_data)
                result["recommendations"]["irrigation"] = irrigation.get("recommendation", {})

                result["confidence"] += 0.2
            else:
                result["crop_analysis"] = {
                    "error": crop_suitability.get("error"),
                    "suggestions": crop_suitability.get("suggestions", [])
                }

        except Exception as e:
            result["errors"].append(f"Crop analysis: {str(e)}")

    # Generate recommendations
    result["recommendations"]["weekly_plan"] = _generate_weekly_plan(
        weather_data.get("daily", []),
        soil_data,
        crop_name
    )

    result["recommendations"]["general"] = _generate_general_recommendations(
        weather_data, soil_data, crop_name
    )

    # Check alerts
    try:
        alerts = check_weather_alerts(weather_data, soil_data, crop_name)
        result["alerts"] = alerts
        result["confidence"] += 0.1

    except Exception as e:
        result["errors"].append(f"Alerts: {str(e)}")

    # Generate summary
    result["summary"] = _generate_summary(result)

    # Normalize confidence
    result["confidence"] = min(1.0, result["confidence"])

    return result


def _format_daily_forecasts(daily: List[Dict]) -> List[Dict]:
    """Format daily forecasts for report."""
    formatted = []
    for day in daily:
        formatted.append({
            "date": day.get("date"),
            "temp_high": day.get("temp_max"),
            "temp_low": day.get("temp_min"),
            "precipitation_mm": day.get("precipitation", 0),
            "precip_chance": day.get("precip_probability", 0),
            "wind_kmh": day.get("wind_speed", 0),
            "humidity_pct": day.get("humidity", 0),
            "conditions": _get_weather_icon(day)
        })
    return formatted


def _get_weather_icon(day: Dict) -> str:
    """Get weather condition description."""
    precip = day.get("precipitation", 0)
    precip_prob = day.get("precip_probability", 0)

    if precip > 10 or precip_prob > 70:
        return "Rainy"
    elif precip > 2 or precip_prob > 40:
        return "Showers"
    elif day.get("temp_max", 20) > 30:
        return "Hot & Sunny"
    elif day.get("temp_min", 10) < 0:
        return "Cold/Frost"
    elif precip_prob > 20:
        return "Partly Cloudy"
    else:
        return "Clear/Sunny"


def _generate_weekly_plan(
    daily: List[Dict],
    soil_data: Dict,
    crop_name: Optional[str] = None
) -> List[Dict]:
    """Generate day-by-day operation plan."""
    plan = []
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for i, day in enumerate(daily[:7]):
        date = day.get("date", f"Day {i+1}")
        temp_max = day.get("temp_max", 20)
        temp_min = day.get("temp_min", 10)
        precip = day.get("precipitation", 0)
        wind = day.get("wind_speed", 0)

        activities = []
        warnings = []

        # Frost check
        if temp_min <= 0:
            warnings.append("Frost risk overnight - protect sensitive plants")

        # Rain day
        if precip > 10:
            activities.append("Indoor tasks - rain expected")
            activities.append("Avoid field work")
        elif precip > 2:
            activities.append("Light rain - limited field work")

        # Good planting day
        if precip < 5 and 5 < temp_max < 30 and wind < 30:
            activities.append("Good conditions for planting/transplanting")

        # Irrigation
        if precip < 2 and i > 0 and daily[i-1].get("precipitation", 0) < 2:
            activities.append("Check irrigation needs")

        # Harvesting
        if precip == 0 and wind < 25:
            activities.append("Good for harvesting")

        # Spraying
        if precip == 0 and wind < 20:
            activities.append("Suitable for spraying if needed")

        # Default activity
        if not activities:
            activities.append("Monitor crops and conditions")

        plan.append({
            "date": date,
            "day": days_of_week[i] if i < 7 else f"Day {i+1}",
            "conditions": _get_weather_icon(day),
            "temp_range": f"{temp_min}°C - {temp_max}°C",
            "recommended_activities": activities,
            "warnings": warnings
        })

    return plan


def _generate_general_recommendations(
    weather_data: Dict,
    soil_data: Dict,
    crop_name: Optional[str] = None
) -> Dict:
    """Generate general farming recommendations."""
    recs = {
        "planting": [],
        "irrigation": [],
        "protection": [],
        "general": []
    }

    daily = weather_data.get("daily", [])
    summary = weather_data.get("summary", {})
    soil = soil_data.get("temperature", {})
    moisture = soil_data.get("moisture", {})

    # Planting recommendations
    soil_temp = soil.get("depth_6cm", 10)
    if soil_temp < 5:
        recs["planting"].append("Soil too cold for most crops - wait for warming")
    elif soil_temp < 10:
        recs["planting"].append("Cool soil - suitable for cold-hardy crops (peas, lettuce, spinach)")
    elif soil_temp < 18:
        recs["planting"].append("Moderate soil temperature - good for many vegetables")
    else:
        recs["planting"].append("Warm soil - ideal for heat-loving crops (tomatoes, peppers, squash)")

    # Frost warning
    if summary.get("frost_days", 0) > 0:
        recs["protection"].append(f"Frost expected on {summary['frost_days']} day(s) - prepare covers")

    # Moisture recommendations
    root_moisture = moisture.get("root_zone_average", 0.3)
    if root_moisture < 0.15:
        recs["irrigation"].append("Soil is dry - irrigate before planting")
    elif root_moisture > 0.45:
        recs["irrigation"].append("Soil is wet - wait before working or planting")
    else:
        recs["irrigation"].append("Soil moisture is adequate")

    # Rain forecast
    total_precip = summary.get("total_precipitation", 0)
    if total_precip > 30:
        recs["irrigation"].append(f"Significant rain expected ({total_precip}mm) - reduce irrigation")
    elif total_precip < 5:
        recs["irrigation"].append("Little rain forecast - plan irrigation schedule")

    # Workability
    workability = soil_data.get("workability_score", 50)
    if workability >= 70:
        recs["general"].append("Soil conditions good for field work")
    elif workability >= 40:
        recs["general"].append("Limited field work possible - soil may be wet or cold")
    else:
        recs["general"].append("Postpone field work - soil not workable")

    return recs


def _generate_summary(report: Dict) -> str:
    """Generate overall summary text."""
    parts = []

    # Location intro
    loc = report.get("location", {})
    parts.append(f"Agricultural report for {loc.get('name', 'your location')}.")

    # Weather summary
    weather = report.get("weather_forecast", {})
    if weather:
        precip = weather.get("total_precipitation_mm", 0)
        frost_days = weather.get("frost_days", 0)

        if frost_days > 0:
            parts.append(f"Frost expected on {frost_days} day(s) - protect sensitive crops.")
        if precip > 20:
            parts.append(f"Significant rainfall expected ({precip}mm total).")
        elif precip < 5:
            parts.append("Dry period ahead - monitor irrigation needs.")

    # Soil summary
    soil = report.get("soil_conditions", {})
    if soil:
        workability = soil.get("workability_score", 0)
        if workability >= 70:
            parts.append("Soil conditions are favorable for field work.")
        elif workability < 40:
            parts.append("Soil conditions limit field operations.")

    # Crop summary
    crop = report.get("crop_analysis")
    if crop and "error" not in crop:
        score = crop.get("suitability_score", 0)
        rec = crop.get("recommendation", "")
        name = crop.get("crop_name", "crop")

        if score >= 70:
            parts.append(f"Conditions are {rec} for {name} cultivation.")
        elif score >= 50:
            parts.append(f"{name} can be planted but with some limitations.")
        else:
            parts.append(f"Conditions not ideal for {name} - consider alternatives.")

    # Alerts summary
    alerts = report.get("alerts", [])
    if alerts:
        emergency = sum(1 for a in alerts if a.get("severity") == "emergency")
        warnings = sum(1 for a in alerts if a.get("severity") == "warning")

        if emergency > 0:
            parts.append(f"ATTENTION: {emergency} emergency alert(s) active!")
        elif warnings > 0:
            parts.append(f"Note: {warnings} weather warning(s) in effect.")

    # Confidence note
    confidence = report.get("confidence", 0)
    if confidence < 0.5:
        parts.append("(Limited data available - results may be less accurate)")

    return " ".join(parts)


def format_report_text(report: Dict) -> str:
    """
    Format report as readable text output.

    Args:
        report: Output from comprehensive_agricultural_report()

    Returns:
        Formatted text string
    """
    lines = []

    # Header
    lines.append("=" * 60)
    lines.append("COMPREHENSIVE AGRICULTURAL REPORT")
    lines.append("=" * 60)

    # Location
    loc = report.get("location", {})
    lines.append(f"\nLocation: {loc.get('name', 'Unknown')}")
    lines.append(f"Coordinates: {loc.get('coordinates', 'N/A')}")
    lines.append(f"Generated: {report.get('generated_at', 'N/A')}")

    # Weather
    lines.append("\n" + "-" * 40)
    lines.append("WEATHER FORECAST (7 Days)")
    lines.append("-" * 40)

    weather = report.get("weather_forecast", {})
    if weather:
        lines.append(f"Period: {weather.get('period', 'N/A')}")
        lines.append(f"Precipitation: {weather.get('total_precipitation_mm', 0):.1f}mm total")
        lines.append(f"Frost days: {weather.get('frost_days', 0)}")

        lines.append("\nDaily Forecast:")
        for day in weather.get("daily_forecasts", [])[:7]:
            lines.append(
                f"  {day['date']}: {day['conditions']:12} "
                f"{day['temp_low']}°-{day['temp_high']}°C, "
                f"{day['precipitation_mm']:.0f}mm"
            )

    # Soil
    lines.append("\n" + "-" * 40)
    lines.append("SOIL CONDITIONS")
    lines.append("-" * 40)

    soil = report.get("soil_conditions", {})
    if soil:
        temps = soil.get("temperature", {})
        lines.append(f"Surface temp: {temps.get('surface', 'N/A')}°C")
        lines.append(f"6cm depth: {temps.get('depth_6cm', 'N/A')}°C")
        lines.append(f"Workability: {soil.get('workability_score', 0)}/100")
        lines.append(f"Assessment: {soil.get('assessment', 'N/A')}")

    # Crop Analysis
    crop = report.get("crop_analysis")
    if crop and "error" not in crop:
        lines.append("\n" + "-" * 40)
        lines.append(f"CROP ANALYSIS: {crop.get('crop_name', 'Unknown').upper()}")
        lines.append("-" * 40)
        lines.append(f"Suitability Score: {crop.get('suitability_score', 0)}/100")
        lines.append(f"Recommendation: {crop.get('recommendation', 'N/A').upper()}")
        lines.append(f"Optimal Window: {crop.get('optimal_window', 'N/A')}")

        factors = crop.get("limiting_factors", [])
        if factors:
            lines.append("Limiting Factors:")
            for f in factors:
                lines.append(f"  - {f}")

    # Weekly Plan
    lines.append("\n" + "-" * 40)
    lines.append("WEEKLY OPERATION PLAN")
    lines.append("-" * 40)

    plan = report.get("recommendations", {}).get("weekly_plan", [])
    for day in plan[:7]:
        lines.append(f"\n{day['day']} {day['date']}:")
        lines.append(f"  Conditions: {day['conditions']} ({day['temp_range']})")
        for act in day.get("recommended_activities", []):
            lines.append(f"  ✓ {act}")
        for warn in day.get("warnings", []):
            lines.append(f"  ⚠ {warn}")

    # Alerts
    alerts = report.get("alerts", [])
    if alerts:
        lines.append("\n" + "-" * 40)
        lines.append("WEATHER ALERTS")
        lines.append("-" * 40)
        for alert in alerts:
            sev = alert.get("severity", "watch").upper()
            lines.append(f"\n[{sev}] {alert.get('message', 'Alert')}")
            lines.append(f"  Action: {alert.get('recommended_action', 'Monitor')}")

    # Summary
    lines.append("\n" + "=" * 60)
    lines.append("SUMMARY")
    lines.append("=" * 60)
    lines.append(report.get("summary", "No summary available"))
    lines.append(f"\nConfidence: {report.get('confidence', 0)*100:.0f}%")

    if report.get("errors"):
        lines.append("\n⚠ Data issues: " + ", ".join(report["errors"]))

    return "\n".join(lines)


def get_farming_recommendations(
    latitude: float,
    longitude: float,
    crop_name: Optional[str] = None,
    operation: Optional[str] = None
) -> Dict:
    """
    Get farming recommendations for location.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        crop_name: Optional specific crop
        operation: Optional operation type (planting, irrigation, etc.)

    Returns:
        Dict with recommendations
    """
    # Get full report and extract recommendations
    report = comprehensive_agricultural_report(latitude, longitude, crop_name)

    result = {
        "location": report.get("location"),
        "recommendations": report.get("recommendations", {}),
        "alerts": report.get("alerts", []),
        "summary": report.get("summary")
    }

    # Filter by operation if specified
    if operation and operation in result["recommendations"]:
        result["recommendations"] = {operation: result["recommendations"][operation]}

    return result


if __name__ == "__main__":
    # Test report generator
    print("Testing Report Generator...")

    # Test with real coordinates (Des Moines, Iowa)
    lat, lon = 41.5868, -93.6250

    print(f"\nGenerating report for {lat}, {lon}...")
    report = comprehensive_agricultural_report(
        lat, lon,
        crop_name="corn",
        location_name="Des Moines, Iowa"
    )

    print("\n" + format_report_text(report))
