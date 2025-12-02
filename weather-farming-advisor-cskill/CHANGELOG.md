# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of Weather Farming Advisor skill
- 7-day weather forecast with agricultural focus
- Soil temperature analysis at 4 depths (0cm, 6cm, 18cm, 54cm)
- Soil moisture monitoring at 5 depth ranges
- Crop suitability scoring system with 20 supported crops
- Weather alert system (frost, heat, drought, flood, wind)
- Irrigation timing recommendations
- Comprehensive agricultural reports
- Weekly operation planning

### Supported Crops
- Vegetables: Tomato, Pepper, Cucumber, Lettuce, Carrot, Onion, Garlic, Cabbage, Broccoli, Spinach
- Grains: Corn, Wheat, Rice
- Legumes: Soybean, Bean, Pea
- Fruits: Melon, Strawberry
- Root crops: Potato
- Squash family: Squash

### API
- Uses Open-Meteo API (free, no API key required)
- Global coverage with 11km resolution
- Data sources: ECMWF, NOAA, DWD, Météo-France

### Documentation
- Complete SKILL.md with activation keywords and usage examples
- API reference documentation
- Crop requirements database
- Architecture decisions document
