---
name: deal-intelligence-cskill
description: Deal Intelligence provides comprehensive business due diligence for executives including company profiles, financials, funding history, hiring activity analysis, news sentiment, and risk assessment. Activates when user asks about company research, due diligence, investment analysis, M&A targets, or business intelligence.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Deal Intelligence - 商业尽调助手

**Version:** 1.0.0
**Type:** Flagship Skill
**Domain:** Business Intelligence / M&A
**Target Users:** 高管、投资人、企业发展部门

## Overview

为高管和投资人提供一站式商业尽职调查能力，覆盖企业全景分析。

## Core Features

### 1. 企业信息 (Company Info)
- 上市公司实时数据（市值、股价、财务指标）
- 私有公司档案（估值、产品、创始人）
- 高管团队信息
- 行业与板块分类

### 2. 融资分析 (Funding Analyzer)
- 融资历史追踪
- 估值轨迹分析
- 投资人背景调查
- 融资节奏评估
- 发展阶段判断

### 3. 增长信号 (Hiring Tracker)
- 招聘规模追踪
- 部门增长分析
- 战略重点识别
- 关键人才变动
- 同比增长率

### 4. 舆情分析 (News Aggregator)
- 新闻聚合
- 情感分析（正面/中性/负面）
- 热点话题识别
- 官方发布追踪

### 5. 风险评估 (Risk Scanner)
- 法律风险扫描
- 财务风险评估
- 声誉风险监控
- 综合风险评分
- 风险对比分析

### 6. 报告生成 (Due Diligence Report)
- 快速概况（一句话版本）
- 投资备忘录
- 完整尽调报告
- 多公司对比分析

## Usage Examples

```
"帮我调研一下字节跳动"
"OpenAI的融资历史"
"腾讯最近有什么新闻"
"对比Anthropic和OpenAI"
"苹果公司风险评估"
"生成投资备忘录: 特斯拉"
```

## Supported Companies

### 上市公司 (via yfinance)
- 美股: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA...
- 港股: 腾讯(0700.HK), 阿里(9988.HK), 美团(3690.HK)...
- 支持中英文公司名称

### 私有公司 (内置数据库)
- 字节跳动
- SpaceX
- OpenAI
- Anthropic
- (可扩展)

## Output Formats

1. **快速概况**: 一句话摘要
2. **投资备忘录**: 2-3页精华
3. **完整报告**: 10页详细分析
4. **对比分析**: 多公司横向比较

## Data Sources

| 数据类型 | 来源 |
|---------|------|
| 上市公司财务 | yfinance (免费) |
| 融资历史 | 模拟数据 (可对接Crunchbase/天眼查) |
| 招聘活动 | 模拟数据 (可对接LinkedIn/Boss直聘) |
| 新闻舆情 | 模拟数据 (可对接新闻API) |
| 风险信息 | 模拟数据 (可对接天眼查/企查查) |

## Dependencies

```
yfinance>=0.2.0
```

## Architecture

```
deal-intelligence-cskill/
├── scripts/
│   ├── __init__.py          # 模块导出
│   ├── company_info.py      # 企业信息
│   ├── funding_analyzer.py  # 融资分析
│   ├── hiring_tracker.py    # 招聘追踪
│   ├── news_aggregator.py   # 新闻聚合
│   ├── risk_scanner.py      # 风险扫描
│   └── due_diligence_report.py  # 报告生成
├── .claude-plugin/
│   └── marketplace.json
├── SKILL.md
├── README.md
└── LICENSE
```

## Future Enhancements

- [ ] 对接天眼查API获取真实企业数据
- [ ] 对接Crunchbase获取全球融资数据
- [ ] 对接LinkedIn招聘数据
- [ ] 添加竞争对手分析
- [ ] 添加行业报告生成
- [ ] 支持PDF报告导出

## License

MIT License
