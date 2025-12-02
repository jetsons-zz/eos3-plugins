---
name: executive-travel-intelligence-cskill
description: Executive travel intelligence provides comprehensive 6-dimension travel analysis including weather forecast, air quality, currency exchange, timezone conversion, holiday calendar, and smart recommendations. Activates when user mentions business trip, travel to city, going to destination, flight to place, or asks about travel conditions. Supports queries like 'I am going to Tokyo next week', 'business trip to London', 'travel report for New York'.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Executive Travel Intelligence - 高管出行智囊

**Version:** 1.0.0
**Type:** Flagship Skill (旗舰级)
**Domain:** Business Travel Intelligence
**Target Users:** 高净值人群、企业高管、商务旅行者

---

## Overview

高管出行智囊是一款旗舰级商务出行助手，通过6个维度的数据整合分析，为商务旅行者提供一站式智能决策支持。

### 6维度融合分析

| 维度 | 功能 | 数据源 |
|------|------|--------|
| 🌡️ 天气 | 7天预报、穿衣建议 | Open-Meteo |
| 💨 空气 | AQI、健康建议、口罩提醒 | AQICN |
| 💱 汇率 | 实时汇率、预算估算 | yfinance |
| 🕐 时区 | 时差计算、会议时间优化 | 内置 |
| 📅 日历 | 节假日、工作日检查 | 内置数据库 |
| ✈️ 综合 | 出行评分、行李清单 | AI分析 |

---

## Activation Keywords

### Primary Keywords
- 出差
- 出行
- 旅行
- business trip
- travel to
- going to
- flight to

### Query Patterns
- "我下周要去东京出差"
- "去伦敦出差，帮我分析一下"
- "纽约出行报告"
- "Business trip to Singapore"
- "Travel conditions for Paris"

---

## Usage Examples

### 完整出行报告
```
用户: 我12月2日到5日去东京出差
```

### 快速检查
```
用户: 东京现在适合出行吗？
```

### 时区查询
```
用户: 北京和纽约的时差
用户: 安排一个北京、伦敦、纽约三方会议
```

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 东京出行智能报告
   2025-12-02 - 2025-12-05 (4天)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 出行评分: 85/100 ⭐⭐⭐⭐

🌡️ 天气概况
   8-15°C | 多云 → 晴天 → 多云

💨 空气质量
   AQI 42 🟢 优

💱 汇率预算
   汇率: 1 CNY = 21.8 JPY
   日均预算: ¥2,100 (舒适)
   总预算: ¥8,400

🕐 时差提醒
   东京比北京快 1 小时
   北京 09:00 = 东京 10:00

📅 当地情况
   ✓ 无重大节假日
   工作日: 4天 / 总共4天

✈️ 行李清单
   □ 薄外套  □ 长袖衬衫
   □ 商务正装  □ 转换插头
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Supported Cities

| 地区 | 城市 |
|------|------|
| 亚太 | 东京、北京、上海、香港、新加坡、首尔、悉尼、迪拜 |
| 欧洲 | 伦敦、巴黎、法兰克福、苏黎世 |
| 美洲 | 纽约、洛杉矶、旧金山、多伦多 |

---

## Scoring System

| 分数 | 等级 | 说明 |
|------|------|------|
| 85-100 | ⭐⭐⭐⭐⭐ 优秀 | 出行条件极佳 |
| 70-84 | ⭐⭐⭐⭐ 良好 | 出行条件良好 |
| 55-69 | ⭐⭐⭐ 一般 | 可以出行，需注意 |
| 40-54 | ⭐⭐ 较差 | 建议调整行程 |
| <40 | ⭐ 不佳 | 不建议出行 |

---

## Architecture

```
executive-travel-intelligence-cskill/
├── scripts/
│   ├── weather_module.py      # 天气模块
│   ├── air_quality_module.py  # 空气质量模块
│   ├── forex_module.py        # 汇率模块
│   ├── timezone_module.py     # 时区模块
│   ├── holiday_module.py      # 节假日模块
│   └── travel_advisor.py      # 核心整合模块
└── ...
```

---

## Dependencies

```
requests>=2.28.0
yfinance>=0.2.0
```

---

*Created by Agent-Skill-Creator v3.2 - Flagship Edition*
