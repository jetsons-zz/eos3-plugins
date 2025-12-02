---
name: ai-quant-trader
description: AI-powered quantitative trading system with technical analysis, sentiment analysis, factor models, risk management, and strategy backtesting. Provides professional-grade AI trading decision support for investors. Activates when user asks about stock analysis, trading signals, market sentiment, portfolio risk, or backtesting strategies.
version: 1.0.0
author: Agent-Skill-Creator
license: MIT
---

# AI Quant Trader Pro

**大模型驱动的智能量化交易系统**

## Overview

AI Quant Trader Pro 是一个对标顶级量化竞赛水准的智能交易决策系统，集成了：

- **技术分析引擎**: MA/EMA/MACD/RSI/KDJ/布林带等30+技术指标
- **形态识别**: 头肩顶底、双顶底、三角形、旗形等K线形态
- **情绪分析**: 新闻情绪、恐惧贪婪指数、分析师评级
- **多因子模型**: 价值、动量、质量、成长等因子评分
- **风险管理**: VaR计算、凯利公式仓位、智能止损
- **策略回测**: 历史回测、绩效分析、参数优化

## Core Features

### 1. 市场分析 (Market Analysis)

```python
from scripts import analyze_stock, calculate_technical_indicators, detect_patterns

# 综合分析
report = analyze_stock("AAPL")
print(report['overall_score'])  # 0-100 综合评分
print(report['signal'])  # BUY/SELL/HOLD

# 技术指标
indicators = calculate_technical_indicators("AAPL", ["MA", "RSI", "MACD", "BBANDS"])
print(indicators['RSI']['value'])  # 55.3
print(indicators['RSI']['signal'])  # "neutral"

# 形态识别
patterns = detect_patterns("AAPL")
print(patterns['detected'])  # ["ascending_triangle", "bullish_engulfing"]
```

### 2. 情绪分析 (Sentiment Analysis)

```python
from scripts import analyze_news_sentiment, get_market_sentiment

# 新闻情绪
sentiment = analyze_news_sentiment("TSLA", days=7)
print(sentiment['score'])  # -1.0 ~ 1.0
print(sentiment['trend'])  # "improving" / "deteriorating"

# 市场情绪
market = get_market_sentiment("US")
print(market['fear_greed_index'])  # 0-100
print(market['vix'])  # VIX指数
```

### 3. Alpha 信号生成 (Alpha Generation)

```python
from scripts import generate_alpha_signals, run_factor_model, screen_stocks

# 生成交易信号
signals = generate_alpha_signals(["AAPL", "GOOGL", "MSFT"], strategy="momentum")
for s in signals['signals']:
    print(f"{s['symbol']}: {s['action']} (confidence: {s['confidence']})")

# 多因子评分
scores = run_factor_model(["AAPL", "GOOGL"], factors=["value", "momentum", "quality"])
print(scores['rankings'])  # 因子综合排名

# 智能选股
picks = screen_stocks(
    criteria={"min_market_cap": 10e9, "min_roe": 15, "max_pe": 25},
    market="US",
    limit=10
)
```

### 4. 风险管理 (Risk Management)

```python
from scripts import calculate_position_size, calculate_var, set_stop_loss

# 仓位计算
position = calculate_position_size(
    capital=100000,
    risk_per_trade=0.02,
    entry_price=150,
    stop_loss=145
)
print(f"建议买入: {position['shares']} 股")

# VaR 计算
var = calculate_var(holdings, confidence=0.95)
print(f"95% VaR: ${var['value']:,.0f}")

# 智能止损
stop = set_stop_loss("AAPL", entry_price=175, method="atr")
print(f"建议止损: ${stop['stop_price']:.2f}")
```

### 5. 策略回测 (Backtesting)

```python
from scripts import backtest_strategy, analyze_performance

# 回测策略
result = backtest_strategy(
    strategy="golden_cross",
    symbols=["SPY"],
    start_date="2020-01-01",
    end_date="2023-12-31"
)
print(f"总收益: {result['total_return']:.1%}")
print(f"夏普比率: {result['sharpe_ratio']:.2f}")
print(f"最大回撤: {result['max_drawdown']:.1%}")
```

### 6. AI 综合建议 (AI Recommendation)

```python
from scripts import get_ai_recommendation, generate_trading_report

# AI 投资建议
rec = get_ai_recommendation("NVDA", investment_style="growth")
print(rec['action'])  # "STRONG BUY"
print(rec['target_price'])
print(rec['risk_level'])
print(rec['reasoning'])

# 综合报告
report = generate_trading_report("AAPL")
print(report)  # Markdown 格式完整报告
```

## Activation Triggers

This skill activates when you ask:

- "分析一下苹果股票" / "Analyze AAPL"
- "现在适合买入特斯拉吗"
- "帮我计算仓位"
- "回测一下均线策略"
- "市场情绪怎么样"
- "给我推荐几只股票"
- "NVDA 技术面分析"
- "设置止损点位"

## Supported Markets

- **US**: 美股 (NYSE, NASDAQ)
- **CN**: A股 (上证, 深证)
- **HK**: 港股

## Data Sources

- Yahoo Finance (实时行情)
- Alpha Vantage (技术指标)
- Financial Modeling Prep (基本面)
- Fear & Greed Index (市场情绪)

## Risk Disclaimer

本工具仅供参考，不构成投资建议。投资有风险，入市需谨慎。
