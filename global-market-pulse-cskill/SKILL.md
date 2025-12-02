---
name: global-market-pulse-cskill
description: Global market pulse provides real-time stock indices, forex rates, commodities and cryptocurrency prices with executive-friendly analysis. Activates when user asks about stock market, market indices, S&P 500, Dow Jones, NASDAQ, market sentiment, forex rates, gold price, oil price, Bitcoin price, or investment market overview. Supports queries like 'how is the market today', 'global stock indices', 'USD CNY rate', 'gold price', 'market sentiment analysis'.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# Global Market Pulse - 全球股市快报

**Version:** 1.0.0
**Type:** Simple Skill
**Domain:** Financial Market Intelligence
**Target Users:** 高净值人群、企业高管
**API:** Yahoo Finance via yfinance (Free, No API Key Required)

---

## Overview

全球股市快报为高净值人群和企业高管提供一站式全球市场信息服务。通过简洁的自然语言查询，即可获取全球主要股指、汇率、大宗商品和加密货币的实时行情及专业分析。

### Core Features

1. **全球股指行情** - 美国、欧洲、亚太主要指数
2. **市场情绪分析** - 多空判断、VIX恐慌指数
3. **主要汇率** - 美元、欧元、人民币等
4. **大宗商品** - 黄金、原油价格
5. **加密货币** - 比特币、以太坊行情
6. **高管简报** - 一句话市场摘要

---

## Activation Keywords

### Primary Keywords (高优先级)
- 股市
- 股票
- 大盘
- 指数
- 行情
- market
- stock
- indices

### Secondary Keywords (中优先级)
- 标普500 / S&P 500
- 道琼斯 / Dow Jones
- 纳斯达克 / NASDAQ
- 恒生指数
- 上证综指
- 汇率
- forex
- 黄金 / gold
- 原油 / oil
- 比特币 / Bitcoin

### Query Patterns
- "今天股市怎么样"
- "全球市场行情"
- "美股表现如何"
- "市场情绪分析"
- "汇率查询"
- "黄金价格"
- "How is the market today"
- "Global market summary"

---

## Usage Examples

### 1. 全球市场快报
```
用户: 今天全球股市怎么样？
用户: 给我一个市场快报
用户: Global market summary
```

### 2. 特定区域市场
```
用户: 美股今天表现如何？
用户: 亚太市场行情
用户: 欧洲股市情况
```

### 3. 汇率查询
```
用户: 美元兑人民币汇率
用户: 主要货币汇率
用户: USD CNY rate
```

### 4. 大宗商品
```
用户: 黄金价格
用户: 今天油价多少
用户: Gold and oil prices
```

### 5. 加密货币
```
用户: 比特币价格
用户: BTC ETH 行情
```

### 6. 市场情绪
```
用户: 市场情绪如何
用户: VIX 恐慌指数
用户: 现在是牛市还是熊市
```

---

## API Integration

### Data Source: Yahoo Finance (yfinance)

**Advantages:**
- 免费使用，无需 API Key
- 2000 请求/小时限制
- 全球市场覆盖
- 实时数据（约15分钟延迟）

**Covered Markets:**
- 美国: NYSE, NASDAQ, AMEX
- 欧洲: London, Frankfurt, Paris
- 亚太: Tokyo, Hong Kong, Shanghai, Shenzhen, Seoul, Sydney

### Rate Limiting
- 内置缓存: 60秒
- 建议间隔: > 1秒/请求
- 批量请求自动节流

---

## Supported Indices

| Symbol | Name | Region | Currency |
|--------|------|--------|----------|
| ^GSPC | 标普500 | 美国 | USD |
| ^DJI | 道琼斯工业 | 美国 | USD |
| ^IXIC | 纳斯达克综合 | 美国 | USD |
| ^VIX | 恐慌指数VIX | 美国 | USD |
| ^FTSE | 富时100 | 英国 | GBP |
| ^GDAXI | 德国DAX | 德国 | EUR |
| ^FCHI | 法国CAC40 | 法国 | EUR |
| ^N225 | 日经225 | 日本 | JPY |
| ^HSI | 恒生指数 | 香港 | HKD |
| 000001.SS | 上证综指 | 中国 | CNY |
| 399001.SZ | 深证成指 | 中国 | CNY |
| ^KS11 | 韩国KOSPI | 韩国 | KRW |
| ^AXJO | 澳洲ASX200 | 澳大利亚 | AUD |
| ^BSESN | 印度孟买 | 印度 | INR |

---

## Output Format

### Executive Summary (一句话版本)
```
📈 全球市场看涨｜8涨4跌｜均幅+0.52%｜最强纳斯达克+1.2%｜最弱恒生指数-0.8%
```

### Market Brief (1分钟阅读)
```markdown
# 📊 全球市场快报
*2025年01月15日 14:30*

**市场状态**: 美国交易中

## 📈 市场情绪: 看涨
全球市场普遍上涨，投资者情绪乐观

- 上涨: 8 个指数
- 下跌: 4 个指数
- 平均涨跌: +0.52%

**恐慌指数VIX**: 15.2 (正常)

## 📈 涨幅榜
1. **纳斯达克综合** (美国) +1.20%
2. **标普500** (美国) +0.85%
...
```

---

## Architecture

```
global-market-pulse-cskill/
├── .claude-plugin/
│   └── marketplace.json
├── scripts/
│   ├── __init__.py
│   ├── market_client.py      # yfinance 客户端
│   ├── market_analyzer.py    # 市场分析
│   └── report_generator.py   # 报告生成
├── SKILL.md
├── README.md
└── LICENSE
```

---

## Dependencies

```
yfinance>=0.2.0
```

Install: `pip install yfinance`

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No data | Market closed | 显示最近收盘数据 |
| Timeout | Network issue | 重试或使用缓存 |
| Invalid symbol | Unknown ticker | 提供建议的符号 |

---

*Created by Agent-Skill-Creator v3.2*
