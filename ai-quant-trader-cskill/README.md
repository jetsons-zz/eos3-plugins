# AI Quant Trader Pro

大模型驱动的智能量化交易系统，对标顶级量化竞赛水准。

## Features

- **技术分析**: 30+ 技术指标、K线形态识别
- **情绪分析**: 新闻情绪、恐惧贪婪指数、分析师评级
- **多因子模型**: 价值、动量、质量、成长因子
- **风险管理**: VaR、凯利公式、智能止损
- **策略回测**: 历史回测、绩效分析、参数优化
- **AI 建议**: 综合评分、买卖信号、目标价位

## Installation

```bash
# As Claude Code Plugin
claude plugins add ai-quant-trader
```

## Quick Start

```python
from scripts import analyze_stock, get_ai_recommendation

# 分析股票
analysis = analyze_stock("AAPL")
print(f"综合评分: {analysis['overall_score']}/100")
print(f"信号: {analysis['signal']}")

# AI 建议
rec = get_ai_recommendation("NVDA")
print(f"建议: {rec['action']}")
print(f"目标价: ${rec['target_price']}")
```

## Supported Markets

- US (NYSE, NASDAQ)
- CN (上证, 深证)
- HK (港股)

## License

MIT License
