# Weather Farming Advisor

Agricultural weather intelligence skill for Claude Code. Get weather forecasts, soil conditions, crop recommendations, and farming operation advice.

## Features

- **7-Day Weather Forecast** - Temperature, precipitation, wind, humidity
- **Soil Analysis** - Temperature and moisture at multiple depths
- **Crop Suitability Scoring** - 20+ crops with detailed requirements
- **Farming Recommendations** - Planting, irrigation, protection advice
- **Weather Alerts** - Frost, drought, heat, flood, wind warnings
- **Comprehensive Reports** - All-in-one agricultural analysis

## Installation

```bash
# Navigate to the skill directory
cd weather-farming-advisor-cskill

# Install in Claude Code
/plugin marketplace add ./
```

## Usage Examples

### Get Weather Forecast
```
"What's the farming weather forecast for my location at 41.5, -93.6?"
"Agricultural weather for Des Moines, Iowa"
```

### Check Crop Planting Conditions
```
"Can I plant tomatoes this week? Location: 40.7, -74.0"
"Is it a good time to plant corn in Iowa?"
"Lettuce planting conditions for my garden"
```

### Soil Analysis
```
"What's the soil temperature at 40.7, -74.0?"
"Are soil conditions good for planting?"
```

### Irrigation Advice
```
"Should I irrigate my corn field today?"
"When should I water my tomatoes?"
```

### Weather Alerts
```
"Any frost risk this week?"
"Weather warnings for farming in my area"
```

### Complete Farm Report
```
"Complete agricultural report for 41.5, -93.6, planning to grow soybeans"
"Full farming analysis for my location"
```

## Supported Crops

| Crop | Min Soil Temp | Frost Tolerance |
|------|--------------|-----------------|
| Tomato | 16°C | None |
| Corn | 10°C | None |
| Wheat | 4°C | High |
| Rice | 18°C | None |
| Potato | 7°C | Low |
| Soybean | 10°C | None |
| Lettuce | 4°C | Medium |
| Carrot | 7°C | Medium |
| Pepper | 18°C | None |
| Cucumber | 16°C | None |
| Bean | 16°C | None |
| Pea | 4°C | High |
| Onion | 2°C | High |
| Garlic | 0°C | Very High |
| Cabbage | 4°C | High |
| Broccoli | 4°C | High |
| Spinach | 2°C | High |
| Squash | 16°C | None |
| Melon | 18°C | None |
| Strawberry | 7°C | Low |

## API

This skill uses the [Open-Meteo API](https://open-meteo.com/) which is:
- **Free** for non-commercial use
- **No API key required**
- Provides global coverage with high-resolution data

## Dependencies

```
requests>=2.28.0
python-dateutil>=2.8.0
```

## Technical Details

### Data Sources
- Weather: Open-Meteo Forecast API (ECMWF, NOAA, DWD models)
- Soil: Open-Meteo soil temperature and moisture data
- Crop data: Built-in database based on agricultural research

### Accuracy
- Weather forecast: 7-day ahead (accuracy decreases after day 3)
- Soil data: Current conditions with hourly resolution
- Location: Any global coordinates (WGS84)

## Troubleshooting

### "Invalid coordinates"
Ensure latitude is between -90 and 90, longitude between -180 and 180.

### "API timeout"
Open-Meteo servers may be slow. Wait and try again.

### "Unknown crop"
Check the supported crops list above. The skill will suggest similar names.

## License

MIT License - Free for personal and commercial use.

## Credits

- Weather data: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0)
- Created by: Agent-Skill-Creator v3.2
