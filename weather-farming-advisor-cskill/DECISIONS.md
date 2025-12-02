# Architecture Decisions

## Selected API: Open-Meteo

### Justification

- **Coverage**: Global weather data with 11km resolution
- **Cost**: Free for non-commercial use, no API key required
- **Rate Limit**: No hard limit, recommended 10 req/min
- **Quality**: Data from multiple national weather services (ECMWF, NOAA, DWD)
- **Documentation**: Excellent API documentation with examples
- **Soil Data**: Includes soil temperature and moisture at multiple depths

### Alternatives Considered

1. **OpenWeatherMap**
   - Rejected: Requires API key, limited free tier
   - No soil data in free tier

2. **Weather.gov (NOAA)**
   - Rejected: US-only coverage
   - Complex API structure

3. **Agromonitoring**
   - Rejected: Requires API key and subscription
   - Better soil data but paid

### Conclusion

Open-Meteo provides the best balance of features, coverage, and accessibility for an agricultural weather skill. The free tier with no API key requirement makes it ideal for immediate use.

---

## Architecture Type: Simple Skill

### Decision

Chose **Simple Skill** architecture over Complex Skill Suite.

### Reasoning

- **Estimated LOC**: ~600 lines (under 1000 threshold)
- **Single Domain**: Agricultural weather analysis
- **Cohesive Functionality**: All features work together
- **No Sub-Skills Needed**: Features are complementary, not independent

### Structure

```
weather-farming-advisor-cskill/
├── .claude-plugin/marketplace.json
├── scripts/
│   ├── __init__.py
│   ├── weather_client.py     # API client
│   ├── crop_advisor.py       # Crop recommendations
│   ├── alert_system.py       # Weather alerts
│   └── report_generator.py   # Comprehensive reports
├── SKILL.md
├── DECISIONS.md
└── README.md
```

---

## Crop Database Design

### Decision

Embedded crop database in Python code rather than external file.

### Reasoning

1. **Simplicity**: No external file dependencies
2. **Performance**: No file I/O needed
3. **Size**: 20 crops is manageable in code
4. **Extensibility**: Easy to add more crops

### Trade-offs

- (-) Harder to update without code changes
- (-) Can't be edited by non-programmers
- (+) No parsing errors possible
- (+) Type-safe access

---

## Alert Thresholds

### Decision

Use conservative thresholds for farmer safety.

### Thresholds

| Alert Type | Watch | Warning | Emergency |
|------------|-------|---------|-----------|
| Frost | 2°C | 0°C | -5°C |
| Heat | 32°C | 35°C | 40°C |
| Flood | 25mm/day | 50mm/day | 100mm/day |
| Wind | 40 km/h | 60 km/h | 80 km/h |

### Reasoning

- Thresholds based on general agricultural guidelines
- Conservative to prevent crop damage
- Can be customized per crop if needed

---

## Naming Convention

### Decision

Use `-cskill` suffix as per Agent-Skill-Creator standard.

### Applied Name

`weather-farming-advisor-cskill`

### Format

- Lowercase
- Hyphen-separated words
- Descriptive name
- `-cskill` suffix

---

*Decisions documented: 2025-01-15*
*Created by: Agent-Skill-Creator v3.2*
