# Air Quality Advisor - 空气质量顾问

为高净值人群和企业高管提供全球空气质量监测与健康建议。

## Features

- **实时 AQI** - 全球城市空气质量指数
- **健康建议** - 基于 AQI 的活动建议
- **敏感人群** - 特殊人群健康警告
- **出行对比** - 多城市空气质量对比
- **活动检查** - 跑步、高尔夫等活动适宜度

## Installation

```bash
pip install requests
```

## Usage

```
"北京空气质量"
"今天适合户外跑步吗？"
"上海和东京空气对比"
"需要戴口罩吗？"
```

## API

使用 AQICN API：
- **免费** - 需注册获取 Token
- **全球** - 9000+ 监测站
- **实时** - 每小时更新

获取 Token: https://aqicn.org/data-platform/token/

## AQI Levels

| AQI | Level | Action |
|-----|-------|--------|
| 0-50 | 🟢 优 | 适合户外活动 |
| 51-100 | 🟡 良 | 正常活动 |
| 101-150 | 🟠 轻度污染 | 减少户外 |
| 151-200 | 🔴 中度污染 | 避免户外 |
| 201+ | 🟣 重度污染 | 留在室内 |

## Supported Cities

北京、上海、广州、深圳、香港、东京、首尔、新加坡、纽约、伦敦等

## License

MIT License
