---
name: executive-calendar-cskill
description: Executive Calendar provides intelligent meeting scheduling across timezones, calendar management, meeting fatigue analysis, and smart reminders. Activates when user asks about scheduling, meetings, calendar, time zones, agenda, or availability.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Executive Calendar - 高管日程智囊

**Version:** 1.0.0
**Type:** Flagship Skill
**Domain:** Productivity / Time Management
**Target Users:** 高管、经常跨时区会议的商务人士

## Overview

为频繁跨国协作的高管提供智能日程管理，优化会议安排，减少时差困扰。

## Core Features

### 1. 时区管理 (Timezone Manager)
- 全球50+主要城市时区支持
- 实时时间转换
- 工作时间重叠计算
- 世界时钟显示

### 2. 会议安排 (Meeting Scheduler)
- 跨时区最佳会议时间推荐
- 便利度评分
- 妥协方案建议
- 会议疲劳度计算

### 3. 日历管理 (Calendar Manager)
- 事件创建/修改/删除
- 冲突检测
- 空闲时段查找
- 今日/本周日程

### 4. 提醒引擎 (Reminder Engine)
- 智能会议准备清单
- 出行提醒
- 时差提醒
- 每日简报

### 5. 报告生成 (Calendar Report)
- 每日日程表
- 本周概览
- 时间分配分析
- 高管简报

## Usage Examples

```
"现在纽约几点"
"北京9点是伦敦几点"
"帮我安排和东京、新加坡的会议"
"我今天的日程"
"本周最忙哪天"
"今天有多少空闲时间"
```

## Supported Cities

| 区域 | 城市 |
|------|------|
| 中国 | 北京、上海、深圳、香港、台北 |
| 日韩 | 东京、首尔、大阪 |
| 东南亚 | 新加坡、曼谷、吉隆坡 |
| 欧洲 | 伦敦、巴黎、柏林、法兰克福 |
| 北美 | 纽约、洛杉矶、旧金山、西雅图 |
| 大洋洲 | 悉尼、墨尔本 |
| 中东 | 迪拜、多哈 |

## Key Algorithms

### 最佳会议时间算法
1. 计算各城市工作时间(9-18)在UTC的范围
2. 找出所有城市的重叠时段
3. 在重叠时段内选择最佳时间点
4. 评估各参与者的便利度
5. 生成带评分的建议

### 疲劳度计算
- 会议时长因子
- 会议数量因子
- 背靠背会议惩罚
- 生成0-100评分

## Architecture

```
executive-calendar-cskill/
├── scripts/
│   ├── __init__.py           # 模块导出
│   ├── timezone_manager.py   # 时区管理
│   ├── meeting_scheduler.py  # 会议安排
│   ├── calendar_manager.py   # 日历管理
│   ├── reminder_engine.py    # 提醒引擎
│   └── calendar_report.py    # 报告生成
├── .claude-plugin/
│   └── marketplace.json
├── SKILL.md
├── README.md
└── LICENSE
```

## Dependencies

无外部依赖，纯Python实现

## Future Enhancements

- [ ] 对接Google Calendar / Outlook API
- [ ] 添加会议室预订功能
- [ ] 集成视频会议链接生成
- [ ] 支持重复会议规则
- [ ] 添加会议纪要自动生成

## License

MIT License
