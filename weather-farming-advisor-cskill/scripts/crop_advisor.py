"""
Crop Advisor Module
Provides crop-specific recommendations based on weather and soil conditions.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


# Comprehensive Crop Database
CROP_DATABASE = {
    "tomato": {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "min_soil_temp_c": 16,
        "optimal_temp_range_c": (21, 27),
        "max_temp_c": 35,
        "water_need": "high",
        "frost_tolerance": "none",
        "days_to_maturity": (60, 85),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.30, 0.50),
        "notes": "Sensitive to cold. Needs consistent moisture during fruiting."
    },
    "corn": {
        "name": "Corn",
        "scientific_name": "Zea mays",
        "min_soil_temp_c": 10,
        "optimal_temp_range_c": (18, 24),
        "max_temp_c": 35,
        "water_need": "medium",
        "frost_tolerance": "none",
        "days_to_maturity": (60, 100),
        "planting_depth_cm": 5,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Heavy nitrogen feeder. Critical water need during tasseling."
    },
    "wheat": {
        "name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "min_soil_temp_c": 4,
        "optimal_temp_range_c": (12, 18),
        "max_temp_c": 30,
        "water_need": "low",
        "frost_tolerance": "high",
        "days_to_maturity": (110, 130),
        "planting_depth_cm": 3,
        "optimal_soil_moisture": (0.20, 0.35),
        "notes": "Winter wheat planted in fall, spring wheat in early spring."
    },
    "rice": {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "min_soil_temp_c": 18,
        "optimal_temp_range_c": (25, 30),
        "max_temp_c": 40,
        "water_need": "very_high",
        "frost_tolerance": "none",
        "days_to_maturity": (100, 150),
        "planting_depth_cm": 2,
        "optimal_soil_moisture": (0.50, 0.70),
        "notes": "Requires flooded conditions for most varieties."
    },
    "potato": {
        "name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "min_soil_temp_c": 7,
        "optimal_temp_range_c": (15, 20),
        "max_temp_c": 25,
        "water_need": "medium",
        "frost_tolerance": "low",
        "days_to_maturity": (70, 120),
        "planting_depth_cm": 10,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Tuber formation slows above 25°C. Hill soil as plants grow."
    },
    "soybean": {
        "name": "Soybean",
        "scientific_name": "Glycine max",
        "min_soil_temp_c": 10,
        "optimal_temp_range_c": (20, 25),
        "max_temp_c": 35,
        "water_need": "medium",
        "frost_tolerance": "none",
        "days_to_maturity": (80, 120),
        "planting_depth_cm": 3,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Nitrogen-fixing legume. Critical water need during pod fill."
    },
    "lettuce": {
        "name": "Lettuce",
        "scientific_name": "Lactuca sativa",
        "min_soil_temp_c": 4,
        "optimal_temp_range_c": (15, 18),
        "max_temp_c": 24,
        "water_need": "high",
        "frost_tolerance": "medium",
        "days_to_maturity": (30, 70),
        "planting_depth_cm": 0.5,
        "optimal_soil_moisture": (0.35, 0.50),
        "notes": "Bolts in hot weather. Best grown in cool seasons."
    },
    "carrot": {
        "name": "Carrot",
        "scientific_name": "Daucus carota",
        "min_soil_temp_c": 7,
        "optimal_temp_range_c": (15, 20),
        "max_temp_c": 25,
        "water_need": "medium",
        "frost_tolerance": "medium",
        "days_to_maturity": (70, 80),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Needs loose, stone-free soil for straight roots."
    },
    "pepper": {
        "name": "Pepper",
        "scientific_name": "Capsicum annuum",
        "min_soil_temp_c": 18,
        "optimal_temp_range_c": (21, 29),
        "max_temp_c": 35,
        "water_need": "high",
        "frost_tolerance": "none",
        "days_to_maturity": (60, 90),
        "planting_depth_cm": 0.5,
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Slower to establish than tomatoes. Protect from wind."
    },
    "cucumber": {
        "name": "Cucumber",
        "scientific_name": "Cucumis sativus",
        "min_soil_temp_c": 16,
        "optimal_temp_range_c": (24, 29),
        "max_temp_c": 35,
        "water_need": "high",
        "frost_tolerance": "none",
        "days_to_maturity": (50, 70),
        "planting_depth_cm": 2,
        "optimal_soil_moisture": (0.35, 0.50),
        "notes": "Bitter fruit from water stress. Trellis for best quality."
    },
    "bean": {
        "name": "Bean (Green/Snap)",
        "scientific_name": "Phaseolus vulgaris",
        "min_soil_temp_c": 16,
        "optimal_temp_range_c": (21, 27),
        "max_temp_c": 32,
        "water_need": "medium",
        "frost_tolerance": "none",
        "days_to_maturity": (50, 60),
        "planting_depth_cm": 3,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Nitrogen-fixing. Don't overwater during germination."
    },
    "pea": {
        "name": "Pea",
        "scientific_name": "Pisum sativum",
        "min_soil_temp_c": 4,
        "optimal_temp_range_c": (13, 18),
        "max_temp_c": 24,
        "water_need": "medium",
        "frost_tolerance": "high",
        "days_to_maturity": (55, 70),
        "planting_depth_cm": 3,
        "optimal_soil_moisture": (0.25, 0.40),
        "notes": "Cool season crop. Plant as early as soil can be worked."
    },
    "onion": {
        "name": "Onion",
        "scientific_name": "Allium cepa",
        "min_soil_temp_c": 2,
        "optimal_temp_range_c": (13, 24),
        "max_temp_c": 30,
        "water_need": "low",
        "frost_tolerance": "high",
        "days_to_maturity": (90, 120),
        "planting_depth_cm": 2,
        "optimal_soil_moisture": (0.20, 0.35),
        "notes": "Day length sensitive. Choose variety for your latitude."
    },
    "garlic": {
        "name": "Garlic",
        "scientific_name": "Allium sativum",
        "min_soil_temp_c": 0,
        "optimal_temp_range_c": (13, 24),
        "max_temp_c": 30,
        "water_need": "low",
        "frost_tolerance": "very_high",
        "days_to_maturity": (90, 180),
        "planting_depth_cm": 5,
        "optimal_soil_moisture": (0.20, 0.35),
        "notes": "Plant in fall for best bulb size. Needs cold period."
    },
    "cabbage": {
        "name": "Cabbage",
        "scientific_name": "Brassica oleracea var. capitata",
        "min_soil_temp_c": 4,
        "optimal_temp_range_c": (15, 20),
        "max_temp_c": 25,
        "water_need": "high",
        "frost_tolerance": "high",
        "days_to_maturity": (70, 100),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Heavy feeder. Watch for cabbage worms."
    },
    "broccoli": {
        "name": "Broccoli",
        "scientific_name": "Brassica oleracea var. italica",
        "min_soil_temp_c": 4,
        "optimal_temp_range_c": (15, 20),
        "max_temp_c": 25,
        "water_need": "high",
        "frost_tolerance": "high",
        "days_to_maturity": (60, 90),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Harvest before flowers open. Side shoots extend harvest."
    },
    "spinach": {
        "name": "Spinach",
        "scientific_name": "Spinacia oleracea",
        "min_soil_temp_c": 2,
        "optimal_temp_range_c": (15, 18),
        "max_temp_c": 24,
        "water_need": "high",
        "frost_tolerance": "high",
        "days_to_maturity": (35, 50),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.35, 0.50),
        "notes": "Bolts quickly in heat. Best for spring and fall."
    },
    "squash": {
        "name": "Squash (Summer)",
        "scientific_name": "Cucurbita pepo",
        "min_soil_temp_c": 16,
        "optimal_temp_range_c": (21, 29),
        "max_temp_c": 35,
        "water_need": "medium",
        "frost_tolerance": "none",
        "days_to_maturity": (45, 65),
        "planting_depth_cm": 2,
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Very productive. Harvest when small for best flavor."
    },
    "melon": {
        "name": "Melon (Cantaloupe)",
        "scientific_name": "Cucumis melo",
        "min_soil_temp_c": 18,
        "optimal_temp_range_c": (24, 30),
        "max_temp_c": 35,
        "water_need": "high",
        "frost_tolerance": "none",
        "days_to_maturity": (75, 95),
        "planting_depth_cm": 2,
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Needs long warm season. Reduce water as fruit ripens."
    },
    "strawberry": {
        "name": "Strawberry",
        "scientific_name": "Fragaria × ananassa",
        "min_soil_temp_c": 7,
        "optimal_temp_range_c": (15, 22),
        "max_temp_c": 30,
        "water_need": "high",
        "frost_tolerance": "low",
        "days_to_maturity": (60, 90),
        "planting_depth_cm": 0,  # Crown at soil level
        "optimal_soil_moisture": (0.30, 0.45),
        "notes": "Mulch heavily. Protect flowers from late frost."
    }
}


# Water need to daily mm conversion
WATER_NEED_MM = {
    "low": 3,
    "medium": 5,
    "high": 7,
    "very_high": 10
}

# Frost tolerance to temperature threshold
FROST_TOLERANCE_TEMP = {
    "none": 2,      # Damaged at 2°C
    "low": 0,       # Damaged at 0°C
    "medium": -2,   # Damaged at -2°C
    "high": -5,     # Damaged at -5°C
    "very_high": -10  # Damaged at -10°C
}


def get_crop_info(crop_name: str) -> Optional[Dict]:
    """
    Get crop information from database.

    Args:
        crop_name: Name of crop (case-insensitive)

    Returns:
        Crop data dict or None if not found
    """
    return CROP_DATABASE.get(crop_name.lower())


def find_similar_crops(query: str) -> List[str]:
    """
    Find crops with similar names.

    Args:
        query: User's crop query

    Returns:
        List of similar crop names
    """
    query_lower = query.lower()
    matches = []

    for crop_key, crop_data in CROP_DATABASE.items():
        if query_lower in crop_key or query_lower in crop_data["name"].lower():
            matches.append(crop_data["name"])

    # If no matches, return first 5 crops as suggestions
    if not matches:
        matches = [CROP_DATABASE[k]["name"] for k in list(CROP_DATABASE.keys())[:5]]

    return matches[:5]


def list_available_crops() -> List[str]:
    """Return list of all available crop names."""
    return [data["name"] for data in CROP_DATABASE.values()]


def calculate_crop_suitability(
    crop_name: str,
    weather_data: Dict,
    soil_data: Dict
) -> Dict:
    """
    Calculate planting suitability score for specific crop.

    Args:
        crop_name: Crop name (e.g., "tomato", "corn")
        weather_data: Output from get_weather_forecast()
        soil_data: Output from get_soil_conditions()

    Returns:
        Dict with:
        - overall_score: 0-100 suitability score
        - soil_temp_score: Soil temperature suitability
        - moisture_score: Soil moisture suitability
        - weather_score: Weather conditions suitability
        - frost_risk_score: Frost risk impact
        - recommendation: "excellent", "good", "fair", "poor", "not_recommended"
        - limiting_factors: List of issues affecting score
        - optimal_planting_window: Suggested planting dates
    """
    crop = get_crop_info(crop_name)
    if not crop:
        similar = find_similar_crops(crop_name)
        return {
            "error": f"Unknown crop: {crop_name}",
            "suggestions": similar,
            "available_crops": list_available_crops()
        }

    # Extract relevant data
    soil_temp = soil_data.get("temperature", {}).get("depth_6cm", 10)
    soil_moisture = soil_data.get("moisture", {}).get("root_zone_average", 0.3)
    daily_forecasts = weather_data.get("daily", [])

    limiting_factors = []
    scores = {}

    # 1. Soil Temperature Score (0-100)
    min_temp = crop["min_soil_temp_c"]
    opt_low, opt_high = crop["optimal_temp_range_c"]

    if soil_temp < min_temp:
        scores["soil_temp"] = max(0, 50 - (min_temp - soil_temp) * 10)
        limiting_factors.append(f"Soil too cold ({soil_temp}°C < {min_temp}°C minimum)")
    elif opt_low <= soil_temp <= opt_high:
        scores["soil_temp"] = 100
    elif soil_temp < opt_low:
        scores["soil_temp"] = 70 + (soil_temp - min_temp) / (opt_low - min_temp) * 30
    else:  # Above optimal
        scores["soil_temp"] = max(50, 100 - (soil_temp - opt_high) * 5)
        if soil_temp > crop["max_temp_c"]:
            limiting_factors.append(f"Soil too warm ({soil_temp}°C)")

    # 2. Soil Moisture Score (0-100)
    opt_moist_low, opt_moist_high = crop["optimal_soil_moisture"]

    if opt_moist_low <= soil_moisture <= opt_moist_high:
        scores["moisture"] = 100
    elif soil_moisture < opt_moist_low:
        scores["moisture"] = max(30, soil_moisture / opt_moist_low * 100)
        if soil_moisture < opt_moist_low * 0.5:
            limiting_factors.append(f"Soil too dry ({soil_moisture:.2f} m³/m³)")
    else:  # Too wet
        excess = soil_moisture - opt_moist_high
        scores["moisture"] = max(30, 100 - excess * 200)
        if soil_moisture > opt_moist_high * 1.3:
            limiting_factors.append(f"Soil too wet ({soil_moisture:.2f} m³/m³)")

    # 3. Weather Score (0-100) - based on next 7 days
    if daily_forecasts:
        temp_scores = []
        for day in daily_forecasts[:7]:
            day_temp = (day.get("temp_max", 20) + day.get("temp_min", 10)) / 2
            if opt_low <= day_temp <= opt_high:
                temp_scores.append(100)
            elif day_temp < opt_low:
                temp_scores.append(max(50, 100 - (opt_low - day_temp) * 5))
            else:
                temp_scores.append(max(50, 100 - (day_temp - opt_high) * 5))

        scores["weather"] = sum(temp_scores) / len(temp_scores) if temp_scores else 70
    else:
        scores["weather"] = 70  # Default if no forecast

    # 4. Frost Risk Score (0-100)
    frost_threshold = FROST_TOLERANCE_TEMP.get(crop["frost_tolerance"], 0)
    frost_days = 0

    for day in daily_forecasts[:7]:
        if day.get("temp_min", 5) < frost_threshold:
            frost_days += 1

    if frost_days == 0:
        scores["frost_risk"] = 100
    elif frost_days <= 2:
        scores["frost_risk"] = 70
        limiting_factors.append(f"{frost_days} days with frost risk")
    else:
        scores["frost_risk"] = max(20, 100 - frost_days * 15)
        limiting_factors.append(f"High frost risk ({frost_days} days below {frost_threshold}°C)")

    # Calculate overall score (weighted average)
    weights = {
        "soil_temp": 0.35,
        "moisture": 0.25,
        "weather": 0.25,
        "frost_risk": 0.15
    }

    overall_score = sum(scores[k] * weights[k] for k in weights)
    overall_score = round(overall_score)

    # Determine recommendation
    if overall_score >= 85:
        recommendation = "excellent"
    elif overall_score >= 70:
        recommendation = "good"
    elif overall_score >= 55:
        recommendation = "fair"
    elif overall_score >= 40:
        recommendation = "poor"
    else:
        recommendation = "not_recommended"

    # Determine optimal planting window
    optimal_window = _find_optimal_window(daily_forecasts, crop)

    return {
        "crop_name": crop["name"],
        "overall_score": overall_score,
        "component_scores": {
            "soil_temperature": round(scores["soil_temp"]),
            "soil_moisture": round(scores["moisture"]),
            "weather_conditions": round(scores["weather"]),
            "frost_risk": round(scores["frost_risk"])
        },
        "recommendation": recommendation,
        "limiting_factors": limiting_factors if limiting_factors else ["None - conditions are favorable"],
        "optimal_planting_window": optimal_window,
        "crop_requirements": {
            "min_soil_temp": f"{crop['min_soil_temp_c']}°C",
            "optimal_temp_range": f"{opt_low}-{opt_high}°C",
            "water_need": crop["water_need"],
            "frost_tolerance": crop["frost_tolerance"],
            "days_to_maturity": f"{crop['days_to_maturity'][0]}-{crop['days_to_maturity'][1]} days"
        },
        "notes": crop["notes"]
    }


def _find_optimal_window(forecasts: List[Dict], crop: Dict) -> str:
    """Find best planting window in forecast period."""
    if not forecasts:
        return "Unable to determine - no forecast data"

    opt_low, opt_high = crop["optimal_temp_range_c"]
    frost_threshold = FROST_TOLERANCE_TEMP.get(crop["frost_tolerance"], 0)

    good_days = []
    for i, day in enumerate(forecasts):
        avg_temp = (day.get("temp_max", 20) + day.get("temp_min", 10)) / 2
        min_temp = day.get("temp_min", 5)
        precip = day.get("precipitation", 0)

        # Good day: no frost, reasonable temp, not heavy rain
        if min_temp > frost_threshold and opt_low - 5 <= avg_temp <= opt_high + 5 and precip < 10:
            good_days.append(day.get("date", f"Day {i+1}"))

    if not good_days:
        return "No ideal days in forecast - consider waiting or using protection"
    elif len(good_days) >= 5:
        return f"Good conditions throughout week. Best days: {', '.join(good_days[:3])}"
    else:
        return f"Optimal days: {', '.join(good_days)}"


def get_irrigation_advice(
    crop_name: str,
    weather_data: Dict,
    soil_data: Dict
) -> Dict:
    """
    Get irrigation recommendations for crop.

    Args:
        crop_name: Crop name
        weather_data: Weather forecast data
        soil_data: Soil conditions data

    Returns:
        Dict with irrigation advice
    """
    crop = get_crop_info(crop_name)
    if not crop:
        return {"error": f"Unknown crop: {crop_name}"}

    soil_moisture = soil_data.get("moisture", {}).get("root_zone_average", 0.3)
    opt_low, opt_high = crop["optimal_soil_moisture"]
    daily_need_mm = WATER_NEED_MM.get(crop["water_need"], 5)

    # Check upcoming precipitation
    total_precip = sum(
        d.get("precipitation", 0) for d in weather_data.get("daily", [])[:3]
    )

    # Calculate deficit
    if soil_moisture < opt_low:
        deficit = (opt_low - soil_moisture) * 100  # Convert to mm roughly
        urgency = "high" if soil_moisture < opt_low * 0.6 else "medium"
    else:
        deficit = 0
        urgency = "low"

    # Decision logic
    if soil_moisture >= opt_high:
        advice = "Do NOT irrigate - soil is adequately moist or wet"
        action = "wait"
        amount = 0
    elif total_precip > daily_need_mm * 2:
        advice = f"WAIT - {total_precip:.0f}mm rain expected in next 3 days"
        action = "wait"
        amount = 0
    elif deficit > 0:
        amount = max(daily_need_mm * 2, deficit)
        advice = f"IRRIGATE - Apply {amount:.0f}mm water"
        action = "irrigate"
    else:
        advice = "Monitor - conditions adequate for now"
        action = "monitor"
        amount = 0

    return {
        "crop": crop["name"],
        "current_moisture": f"{soil_moisture:.3f} m³/m³",
        "optimal_range": f"{opt_low:.2f}-{opt_high:.2f} m³/m³",
        "daily_water_need": f"{daily_need_mm}mm",
        "upcoming_rain": f"{total_precip:.1f}mm in 3 days",
        "recommendation": {
            "action": action,
            "advice": advice,
            "amount_mm": amount,
            "urgency": urgency
        }
    }


if __name__ == "__main__":
    # Test crop advisor
    print("Testing Crop Advisor...")
    print(f"\nAvailable crops: {', '.join(list_available_crops())}")

    crop_info = get_crop_info("tomato")
    print(f"\nTomato info: {crop_info}")

    # Test with mock data
    mock_weather = {
        "daily": [
            {"date": "2025-01-15", "temp_max": 22, "temp_min": 12, "precipitation": 0},
            {"date": "2025-01-16", "temp_max": 24, "temp_min": 14, "precipitation": 5},
            {"date": "2025-01-17", "temp_max": 23, "temp_min": 13, "precipitation": 0},
        ]
    }
    mock_soil = {
        "temperature": {"depth_6cm": 18},
        "moisture": {"root_zone_average": 0.35}
    }

    suitability = calculate_crop_suitability("tomato", mock_weather, mock_soil)
    print(f"\nTomato suitability: {suitability}")
