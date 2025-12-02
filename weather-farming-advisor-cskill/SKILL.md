---
name: weather-farming-advisor-cskill
description: Agricultural weather advisor that provides 7-day weather forecasts, soil condition analysis, crop suitability scoring, and farming operation recommendations. Activates when user asks about weather for farming, crop planting advice, agricultural weather forecast, soil temperature, irrigation timing, frost alerts, or farming recommendations for specific locations and crops. Supports queries like 'weather forecast for my farm', 'is it good to plant tomatoes', 'soil conditions for wheat', 'when should I irrigate', 'frost risk this week'.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Weather Farming Advisor - Agricultural Intelligence Skill

**Version:** 1.0.0
**Type:** Simple Skill
**Domain:** Agricultural Weather Analysis
**Created by:** Agent-Skill-Creator v3.2
**API:** Open-Meteo (Free, No API Key Required)

---

## Table of Contents

1. [Overview](#overview)
2. [Core Capabilities](#core-capabilities)
3. [When to Use This Skill](#when-to-use-this-skill)
4. [Activation Keywords](#activation-keywords)
5. [Architecture & Design](#architecture--design)
6. [API Integration](#api-integration)
7. [Crop Database](#crop-database)
8. [Analysis Functions](#analysis-functions)
9. [Usage Examples](#usage-examples)
10. [Error Handling](#error-handling)
11. [Performance & Caching](#performance--caching)
12. [Extension Points](#extension-points)

---

## Overview

### Purpose

The **Weather Farming Advisor** is an intelligent agricultural assistant that bridges meteorological data with practical farming decisions. It fetches real-time weather forecasts and soil conditions, then applies crop-specific knowledge to generate actionable farming recommendations.

### Problem Statement

Farmers and gardeners face daily decisions influenced by weather:
- When is the optimal time to plant specific crops?
- Should I irrigate today or wait for predicted rain?
- Is there frost risk that requires protective measures?
- Are soil conditions suitable for seeding?
- What farming operations should I prioritize this week?

This skill automates the analysis of weather data and provides crop-specific recommendations, saving hours of manual weather interpretation.

### Solution Approach

1. **Weather Data Acquisition**: Fetch 7-day forecasts from Open-Meteo API
2. **Soil Condition Analysis**: Analyze soil temperature and moisture at multiple depths
3. **Crop Matching**: Apply crop-specific requirements to current conditions
4. **Suitability Scoring**: Calculate numerical scores for farming operations
5. **Recommendation Generation**: Produce actionable advice with confidence levels

### Key Benefits

- **No API Key Required**: Uses free Open-Meteo API
- **Crop-Specific Advice**: Built-in database of 20+ common crops
- **Multi-Layer Soil Analysis**: Temperature and moisture at 0-7cm, 7-28cm, 28-100cm depths
- **Actionable Output**: Clear recommendations with timing suggestions
- **Alert System**: Frost, drought, and extreme weather warnings

---

## Core Capabilities

### 1. Seven-Day Weather Forecast

Provides comprehensive weather forecast including:
- Daily high/low temperatures
- Precipitation probability and amount
- Wind speed and direction
- Relative humidity
- Solar radiation (for photosynthesis estimation)
- UV index

### 2. Soil Condition Analysis

Analyzes soil health indicators:
- **Soil Temperature** at 0cm, 6cm, 18cm, 54cm depths
- **Soil Moisture** at multiple soil layers
- **Frost Depth** estimation
- **Workability Score** (is soil too wet/frozen to work?)

### 3. Crop Suitability Scoring

For any specified crop, calculates:
- **Planting Suitability** (0-100 score)
- **Growth Conditions** rating
- **Harvest Window** assessment
- **Risk Factors** identification

### 4. Farming Operation Recommendations

Provides timing advice for:
- **Planting/Seeding**: Optimal dates based on soil temperature
- **Irrigation**: When to water vs. wait for rain
- **Fertilization**: Best application windows
- **Harvest**: Weather-based harvest timing
- **Protection**: Frost cover, wind barriers needed

### 5. Weather Alerts

Automatic detection of:
- **Frost Risk**: Temperatures below crop tolerance
- **Drought Conditions**: Extended dry periods
- **Heat Stress**: Extreme high temperatures
- **Heavy Rain**: Flood/erosion risk
- **Strong Winds**: Crop damage potential

### 6. Comprehensive Agricultural Report

One-stop function that combines all analyses into a complete farm status report.

---

## When to Use This Skill

### Activate When User:

**Asks about farming weather:**
- "What's the weather forecast for farming this week?"
- "Is the weather good for planting?"
- "Agricultural forecast for [location]"

**Asks about specific crops:**
- "Can I plant tomatoes this week?"
- "Is it good weather for wheat?"
- "Corn planting conditions in Iowa"

**Asks about soil conditions:**
- "What's the soil temperature?"
- "Is the soil warm enough for seeds?"
- "Soil moisture levels for my garden"

**Asks about farming operations:**
- "Should I irrigate today?"
- "When is the best time to plant?"
- "Is it safe to spray pesticides?"

**Asks about weather risks:**
- "Frost risk this week?"
- "Will there be drought?"
- "Is rain coming for my crops?"

### Do NOT Activate When:

- User asks for general weather (not farming-related)
- User asks about indoor gardening
- User asks about livestock (different domain)
- User asks about crop prices or markets

---

## Activation Keywords

### Layer 1: Exact Keywords (15 phrases)

```json
[
  "farming weather",
  "agricultural forecast",
  "crop planting advice",
  "soil temperature",
  "soil moisture",
  "irrigation timing",
  "frost alert farming",
  "planting conditions",
  "harvest weather",
  "farm weather forecast",
  "when to plant",
  "crop suitability",
  "agricultural weather",
  "farming recommendations",
  "soil conditions for planting"
]
```

### Layer 2: Regex Patterns (7 patterns)

```regex
# Pattern 1: Crop planting queries
(?i)(plant|sow|seed)\s+.*(weather|conditions?|suitable|good|ready)

# Pattern 2: Weather for farming
(?i)(weather|forecast)\s+.*(farm|crop|agricult|garden|plant)

# Pattern 3: Soil condition queries
(?i)soil\s+(temperature|moisture|conditions?|ready|warm)

# Pattern 4: Irrigation queries
(?i)(irrigat|water)\s+.*(when|should|timing|need)

# Pattern 5: Frost/freeze alerts
(?i)(frost|freeze)\s+.*(risk|alert|warning|protect)

# Pattern 6: Harvest timing
(?i)(harvest|pick)\s+.*(when|timing|weather|conditions?)

# Pattern 7: Specific crop + location
(?i)(tomato|corn|wheat|soybean|rice|potato).*\s+(plant|grow|farm)
```

### Layer 3: NLU Description Keywords (50+)

weather, forecast, farming, agricultural, crop, plant, planting, sow, seed, seeding, soil, temperature, moisture, irrigation, water, watering, frost, freeze, harvest, grow, growing, conditions, suitable, ready, timing, when, should, farm, garden, gardening, tomato, corn, wheat, rice, soybean, potato, vegetable, fruit, grain, field, outdoor, season, spring, summer, fall, autumn, winter, alert, warning, risk, drought, rain, precipitation

---

## Architecture & Design

### Component Structure

```
weather-farming-advisor-cskill/
├── .claude-plugin/
│   └── marketplace.json          # Plugin configuration
├── scripts/
│   ├── weather_client.py         # Open-Meteo API client
│   ├── soil_analyzer.py          # Soil condition analysis
│   ├── crop_advisor.py           # Crop-specific recommendations
│   ├── alert_system.py           # Weather alert detection
│   └── report_generator.py       # Comprehensive reports
├── references/
│   ├── crop_requirements.md      # Crop database documentation
│   └── api_reference.md          # API usage guide
├── SKILL.md                      # This file
├── DECISIONS.md                  # Architecture decisions
└── README.md                     # User documentation
```

### Data Flow

```
User Query
    ↓
Location Resolution (coordinates)
    ↓
Open-Meteo API Call
    ↓
┌─────────────────────────────────────┐
│         Data Processing              │
├─────────────┬─────────────┬─────────┤
│ Weather     │ Soil        │ Alerts  │
│ Forecast    │ Analysis    │ Check   │
└─────────────┴─────────────┴─────────┘
    ↓
Crop Requirements Matching
    ↓
Suitability Scoring
    ↓
Recommendation Generation
    ↓
Formatted Response
```

---

## API Integration

### Open-Meteo Forecast API

**Base URL:** `https://api.open-meteo.com/v1/forecast`

**Required Parameters:**
- `latitude`: Location latitude (WGS84)
- `longitude`: Location longitude (WGS84)

**Weather Variables Used:**
```
daily:
  - temperature_2m_max
  - temperature_2m_min
  - precipitation_sum
  - precipitation_probability_max
  - wind_speed_10m_max
  - relative_humidity_2m_mean
  - et0_fao_evapotranspiration

hourly:
  - soil_temperature_0cm
  - soil_temperature_6cm
  - soil_temperature_18cm
  - soil_temperature_54cm
  - soil_moisture_0_to_1cm
  - soil_moisture_1_to_3cm
  - soil_moisture_3_to_9cm
  - soil_moisture_9_to_27cm
  - soil_moisture_27_to_81cm
```

**Example Request:**
```python
import requests

params = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "hourly": ["soil_temperature_0cm", "soil_moisture_0_to_1cm"],
    "timezone": "auto",
    "forecast_days": 7
}

response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
data = response.json()
```

---

## Crop Database

### Supported Crops (20+)

| Crop | Min Soil Temp (°C) | Optimal Temp (°C) | Water Need | Frost Tolerance |
|------|-------------------|-------------------|------------|-----------------|
| Tomato | 16 | 21-27 | High | None |
| Corn | 10 | 18-24 | Medium | None |
| Wheat | 4 | 12-18 | Low | High |
| Rice | 18 | 25-30 | Very High | None |
| Potato | 7 | 15-20 | Medium | Low |
| Soybean | 10 | 20-25 | Medium | None |
| Lettuce | 4 | 15-18 | High | Medium |
| Carrot | 7 | 15-20 | Medium | Medium |
| Pepper | 18 | 21-29 | High | None |
| Cucumber | 16 | 24-29 | High | None |
| Bean | 16 | 21-27 | Medium | None |
| Pea | 4 | 13-18 | Medium | High |
| Onion | 2 | 13-24 | Low | High |
| Garlic | 0 | 13-24 | Low | Very High |
| Cabbage | 4 | 15-20 | High | High |
| Broccoli | 4 | 15-20 | High | High |
| Spinach | 2 | 15-18 | High | High |
| Squash | 16 | 21-29 | Medium | None |
| Melon | 18 | 24-30 | High | None |
| Strawberry | 7 | 15-22 | High | Low |

### Crop Requirement Structure

```python
CROP_DATABASE = {
    "tomato": {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "min_soil_temp_c": 16,
        "optimal_temp_range_c": (21, 27),
        "max_temp_c": 35,
        "water_need": "high",  # low, medium, high, very_high
        "frost_tolerance": "none",  # none, low, medium, high, very_high
        "days_to_maturity": (60, 85),
        "planting_depth_cm": 1,
        "optimal_soil_moisture": (0.3, 0.5),  # volumetric water content
        "growth_stages": ["seedling", "vegetative", "flowering", "fruiting"],
        "notes": "Sensitive to cold. Needs consistent moisture during fruiting."
    },
    # ... more crops
}
```

---

## Analysis Functions

### 1. get_weather_forecast()

```python
def get_weather_forecast(
    latitude: float,
    longitude: float,
    days: int = 7
) -> Dict:
    """
    Fetch weather forecast for specified location.

    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        days: Forecast days (1-16, default 7)

    Returns:
        Dict with daily forecasts including:
        - date: ISO date string
        - temp_max: Maximum temperature (°C)
        - temp_min: Minimum temperature (°C)
        - precipitation: Total precipitation (mm)
        - precip_probability: Precipitation chance (%)
        - wind_speed: Maximum wind speed (km/h)
        - humidity: Mean relative humidity (%)
        - evapotranspiration: Reference ET (mm)

    Example:
        >>> forecast = get_weather_forecast(40.7128, -74.0060)
        >>> print(forecast['daily'][0])
        {'date': '2025-01-15', 'temp_max': 8.2, 'temp_min': -1.3, ...}
    """
```

### 2. analyze_soil_conditions()

```python
def analyze_soil_conditions(
    latitude: float,
    longitude: float
) -> Dict:
    """
    Analyze current soil temperature and moisture at multiple depths.

    Args:
        latitude: Location latitude
        longitude: Location longitude

    Returns:
        Dict with:
        - soil_temp_surface: Surface soil temperature (°C)
        - soil_temp_6cm: Temperature at 6cm depth (°C)
        - soil_temp_18cm: Temperature at 18cm depth (°C)
        - soil_temp_54cm: Temperature at 54cm depth (°C)
        - soil_moisture_surface: Surface moisture (m³/m³)
        - soil_moisture_root_zone: Root zone moisture (m³/m³)
        - workability_score: 0-100 score for field work
        - frost_risk: Boolean frost risk indicator

    Example:
        >>> soil = analyze_soil_conditions(40.7128, -74.0060)
        >>> print(f"Soil at 6cm: {soil['soil_temp_6cm']}°C")
    """
```

### 3. calculate_crop_suitability()

```python
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
        soil_data: Output from analyze_soil_conditions()

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

    Example:
        >>> suitability = calculate_crop_suitability("tomato", weather, soil)
        >>> print(f"Score: {suitability['overall_score']}/100")
        >>> print(f"Recommendation: {suitability['recommendation']}")
    """
```

### 4. get_farming_recommendations()

```python
def get_farming_recommendations(
    latitude: float,
    longitude: float,
    crop_name: Optional[str] = None,
    operation: Optional[str] = None
) -> Dict:
    """
    Generate farming operation recommendations.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        crop_name: Optional crop for specific advice
        operation: Optional operation type: "planting", "irrigation",
                   "fertilization", "harvest", "protection"

    Returns:
        Dict with:
        - planting: Planting recommendations and timing
        - irrigation: Watering schedule suggestions
        - fertilization: Fertilizer application windows
        - harvest: Harvest timing advice
        - protection: Protective measures needed
        - alerts: Active weather alerts
        - weekly_plan: Day-by-day operation plan

    Example:
        >>> recs = get_farming_recommendations(40.7, -74.0, crop="tomato")
        >>> print(recs['planting']['advice'])
        >>> print(recs['weekly_plan'])
    """
```

### 5. check_weather_alerts()

```python
def check_weather_alerts(
    latitude: float,
    longitude: float,
    crop_name: Optional[str] = None
) -> List[Dict]:
    """
    Check for weather alerts affecting farming operations.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        crop_name: Optional crop for specific alerts

    Returns:
        List of alert dicts, each containing:
        - type: "frost", "drought", "heat", "flood", "wind"
        - severity: "watch", "warning", "emergency"
        - start_date: Alert start date
        - end_date: Alert end date
        - message: Human-readable alert message
        - recommended_action: Suggested protective measures

    Example:
        >>> alerts = check_weather_alerts(40.7, -74.0, crop="tomato")
        >>> for alert in alerts:
        ...     print(f"[{alert['severity']}] {alert['message']}")
    """
```

### 6. comprehensive_agricultural_report() [REQUIRED]

```python
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
        latitude: Location latitude
        longitude: Location longitude
        crop_name: Optional specific crop for detailed analysis
        location_name: Optional human-readable location name

    Returns:
        Dict with ALL metrics consolidated:
        {
            'location': {
                'name': str or "Unknown",
                'latitude': float,
                'longitude': float,
                'timezone': str
            },
            'generated_at': str (ISO timestamp),
            'weather_forecast': {
                '7_day_summary': str,
                'daily_forecasts': List[Dict],
                'precipitation_total': float,
                'temp_range': Tuple[float, float]
            },
            'soil_conditions': {
                'temperatures': Dict,
                'moisture': Dict,
                'workability': int,
                'assessment': str
            },
            'crop_analysis': {  # If crop specified
                'crop_name': str,
                'suitability_score': int,
                'recommendation': str,
                'limiting_factors': List[str],
                'optimal_window': str
            },
            'recommendations': {
                'planting': Dict,
                'irrigation': Dict,
                'protection': Dict,
                'weekly_plan': List[Dict]
            },
            'alerts': List[Dict],
            'summary': str (overall insights),
            'confidence': float (data quality indicator)
        }

    Example:
        >>> report = comprehensive_agricultural_report(
        ...     40.7128, -74.0060,
        ...     crop_name="tomato",
        ...     location_name="New York Farm"
        ... )
        >>> print(report['summary'])
        >>> print(report['recommendations']['weekly_plan'])
    """
```

---

## Usage Examples

### Example 1: Simple Weather Forecast

**User:** "What's the farming weather forecast for Des Moines, Iowa?"

**Response:**
```
📍 Des Moines, Iowa (41.59°N, -93.62°W)

🌤️ 7-Day Agricultural Forecast:

Mon Jan 15: ⛅ High 5°C / Low -3°C | Precip: 20% (2mm)
Tue Jan 16: 🌧️ High 7°C / Low 1°C | Precip: 80% (12mm)
Wed Jan 17: ☁️ High 4°C / Low -2°C | Precip: 10% (0mm)
Thu Jan 18: ⛅ High 6°C / Low -1°C | Precip: 15% (1mm)
Fri Jan 19: ☀️ High 8°C / Low 0°C | Precip: 5% (0mm)
Sat Jan 20: ☀️ High 10°C / Low 2°C | Precip: 0% (0mm)
Sun Jan 21: ⛅ High 9°C / Low 1°C | Precip: 10% (0mm)

🌡️ Soil Conditions:
- Surface temp: 2°C (frozen risk)
- 6cm depth: 4°C
- Moisture: Adequate (0.32 m³/m³)
- Workability: Poor (soil too wet/cold)

⚠️ Alerts:
- FROST WARNING: Overnight lows below 0°C Mon-Thu
- Wait for soil to warm before field work
```

### Example 2: Crop Planting Advice

**User:** "Is it a good time to plant tomatoes in Austin, Texas?"

**Response:**
```
🍅 Tomato Planting Analysis - Austin, TX

📊 Suitability Score: 78/100 (GOOD)

🌡️ Soil Temperature Check:
- Current 6cm temp: 18°C ✅
- Tomato minimum: 16°C
- Status: SUITABLE for planting

💧 Moisture Analysis:
- Soil moisture: 0.28 m³/m³
- Tomato optimal: 0.30-0.50 m³/m³
- Status: Slightly dry, irrigate after planting

🌤️ Weather Outlook:
- Next 7 days: No frost risk ✅
- Precipitation: Light rain Thu (8mm)
- Temperatures: 18-28°C range ✅

📋 Recommendation: GOOD TO PLANT
- Best planting window: Today through Wednesday
- Avoid planting Thursday (rain)
- Water deeply after transplanting
- Consider mulch to retain moisture

⚠️ Notes:
- Nighttime temps still cool, use row covers if below 10°C
- Harden off seedlings before transplanting
```

### Example 3: Irrigation Timing

**User:** "Should I irrigate my corn field today? Location: 41.5°N, -93.6°W"

**Response:**
```
🌽 Corn Irrigation Analysis

📍 Location: 41.50°N, -93.60°W

💧 Current Soil Moisture:
- Surface (0-1cm): 0.18 m³/m³ (DRY)
- Root zone (9-27cm): 0.25 m³/m³ (ADEQUATE)
- Deep (27-81cm): 0.31 m³/m³ (GOOD)

🌧️ Precipitation Forecast:
- Today: 0mm (0% chance)
- Tomorrow: 15mm expected (85% chance)
- Next 3 days: 22mm total

📊 Irrigation Decision: WAIT

✅ Recommendation: Do NOT irrigate today
- Reason: 15mm rain expected tomorrow
- Root zone moisture is adequate
- Irrigating now would waste water and risk waterlogging

📅 Re-evaluate: Check again in 3 days
- If rain doesn't materialize, irrigate Wednesday
- Target: 25mm application
```

### Example 4: Comprehensive Farm Report

**User:** "Complete agricultural report for my farm at coordinates 38.9, -77.0, planning to grow lettuce"

**Response:**
```
📋 COMPREHENSIVE AGRICULTURAL REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Location: 38.90°N, -77.00°W
📅 Generated: 2025-01-15 10:30 UTC
🥬 Crop Focus: Lettuce

═══════════════════════════════════════
🌤️ WEATHER SUMMARY (Next 7 Days)
═══════════════════════════════════════
Temperature Range: -2°C to 12°C
Total Precipitation: 18mm
Dominant Conditions: Partly cloudy, cool

Daily Breakdown:
│ Date   │ High │ Low  │ Rain │ Wind  │
├────────┼──────┼──────┼──────┼───────┤
│ Jan 15 │  8°C │ -1°C │  0mm │ 15kph │
│ Jan 16 │ 10°C │  2°C │  5mm │ 12kph │
│ Jan 17 │ 12°C │  4°C │  8mm │ 18kph │
│ Jan 18 │  9°C │  1°C │  3mm │ 10kph │
│ Jan 19 │  7°C │ -2°C │  0mm │  8kph │
│ Jan 20 │  8°C │  0°C │  2mm │ 14kph │
│ Jan 21 │ 11°C │  3°C │  0mm │ 11kph │

═══════════════════════════════════════
🌱 SOIL CONDITIONS
═══════════════════════════════════════
Surface Temperature: 4°C
6cm Depth: 6°C
18cm Depth: 8°C
Root Zone Moisture: 0.34 m³/m³ (GOOD)
Workability Score: 72/100 (FAIR)

Assessment: Soil is workable but cool. Light
cultivation possible on dry days.

═══════════════════════════════════════
🥬 LETTUCE SUITABILITY ANALYSIS
═══════════════════════════════════════
Overall Score: 85/100 (EXCELLENT)

Component Scores:
├── Soil Temperature: 90/100 ✅
├── Soil Moisture: 88/100 ✅
├── Weather Conditions: 82/100 ✅
└── Frost Risk: 75/100 ⚠️

Limiting Factors:
- Minor frost risk Jan 15, 19 (overnight lows below 0°C)
- Lettuce is frost-tolerant but protect young seedlings

Recommendation: EXCELLENT time to plant lettuce
- Cool weather is ideal for lettuce
- Soil temperature above minimum (4°C > 2°C required)
- Good moisture levels reduce irrigation needs

═══════════════════════════════════════
📋 WEEKLY OPERATION PLAN
═══════════════════════════════════════

MON Jan 15:
  ✅ Good day for planting (dry, mild)
  ⚠️ Cover seedlings overnight (frost risk)

TUE Jan 16:
  ✅ Continue planting in morning
  🌧️ Light rain PM - no irrigation needed

WED Jan 17:
  🌧️ Rain day - avoid field work
  📝 Good day for planning/indoor tasks

THU Jan 18:
  ✅ Resume planting after soil drains
  💧 Check moisture - likely adequate

FRI Jan 19:
  ⚠️ Frost protection needed overnight
  ✅ Daytime planting OK

SAT Jan 20:
  ✅ Good conditions for all operations
  💧 Light irrigation if no rain Thu

SUN Jan 21:
  ✅ Excellent planting conditions
  🌱 Ideal for transplanting seedlings

═══════════════════════════════════════
⚠️ ACTIVE ALERTS
═══════════════════════════════════════
[WATCH] Light Frost - Jan 15, 19 overnight
  Action: Cover young lettuce with row covers
  Impact: Low for established lettuce (frost tolerant)

═══════════════════════════════════════
📊 SUMMARY
═══════════════════════════════════════
This is an EXCELLENT week to grow lettuce. Cool
temperatures (7-12°C) are ideal for this crop, and
soil conditions are favorable. The main concern is
light frost on two nights - use row covers for
protection. Take advantage of the dry days (Mon,
Thu-Sun) for planting operations.

Confidence: 92% (based on high-quality forecast data)
```

---

## Error Handling

### Location Errors

```python
# Invalid coordinates
if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
    return {
        "error": "Invalid coordinates",
        "message": "Latitude must be -90 to 90, longitude -180 to 180",
        "suggestion": "Check your coordinates or use a location lookup service"
    }
```

### API Errors

```python
# API unavailable
try:
    response = requests.get(api_url, params=params, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return {
        "error": "API timeout",
        "message": "Weather service is slow, please try again",
        "fallback": get_cached_data(latitude, longitude)  # Use cache if available
    }
except requests.exceptions.HTTPError as e:
    return {
        "error": "API error",
        "message": f"Weather service returned error: {e}",
        "suggestion": "Try again in a few minutes"
    }
```

### Unknown Crop

```python
# Crop not in database
if crop_name.lower() not in CROP_DATABASE:
    similar = find_similar_crops(crop_name)
    return {
        "error": "Unknown crop",
        "message": f"'{crop_name}' not found in database",
        "suggestion": f"Did you mean: {', '.join(similar)}?",
        "available_crops": list(CROP_DATABASE.keys())
    }
```

---

## Performance & Caching

### Caching Strategy

```python
# Cache weather data for 1 hour (data updates hourly)
CACHE_TTL_WEATHER = 3600  # seconds

# Cache soil data for 3 hours (changes slowly)
CACHE_TTL_SOIL = 10800  # seconds

# Cache key format
def get_cache_key(lat: float, lon: float, data_type: str) -> str:
    # Round coordinates to 2 decimal places (11km precision)
    return f"{data_type}:{lat:.2f}:{lon:.2f}"
```

### Rate Limiting

Open-Meteo free tier:
- No hard rate limit for non-commercial use
- Recommended: Max 10 requests/minute
- Implemented: 1 second delay between API calls

---

## Extension Points

### Adding New Crops

```python
# Add to CROP_DATABASE in crop_advisor.py
CROP_DATABASE["new_crop"] = {
    "name": "New Crop",
    "scientific_name": "Genus species",
    "min_soil_temp_c": 10,
    "optimal_temp_range_c": (18, 25),
    # ... other requirements
}
```

### Custom Alert Thresholds

```python
# Override default thresholds
ALERT_THRESHOLDS = {
    "frost": 0,  # °C - default
    "heat": 35,  # °C - default
    "drought_days": 7,  # consecutive dry days
    "heavy_rain": 50,  # mm in 24 hours
    "wind": 50,  # km/h
}
```

### Adding New Weather Sources

The architecture supports adding alternative APIs:
1. Implement new client in `scripts/`
2. Follow same interface as `weather_client.py`
3. Update configuration to switch sources

---

## Dependencies

```
requests>=2.28.0
python-dateutil>=2.8.0
```

No additional dependencies required. Uses only Python standard library plus requests.

---

## References

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [FAO Crop Water Requirements](http://www.fao.org/3/x0490e/x0490e00.htm)
- [USDA Plant Hardiness Zones](https://planthardiness.ars.usda.gov/)

---

*Created by Agent-Skill-Creator v3.2*
*Weather data: Open-Meteo (CC BY 4.0)*
