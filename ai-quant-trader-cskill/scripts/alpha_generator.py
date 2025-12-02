"""
Alpha Generator - Alpha信号生成器
多因子模型、选股信号、量化策略
"""

import math
import random
from datetime import datetime
from typing import Dict, List, Optional

from .market_analyzer import MarketAnalyzer, analyze_stock, calculate_technical_indicators


class AlphaGenerator:
    """Alpha信号生成器"""

    def __init__(self):
        self.analyzer = MarketAnalyzer()

    def calculate_momentum_score(self, symbol: str) -> float:
        """计算动量因子分数"""
        data = self.analyzer.get_stock_data(symbol)
        if not data or "history" not in data:
            return 50

        prices = data["history"]["close"]
        if len(prices) < 20:
            return 50

        # 计算不同周期的动量
        mom_5d = (prices[-1] / prices[-5] - 1) * 100 if len(prices) >= 5 else 0
        mom_10d = (prices[-1] / prices[-10] - 1) * 100 if len(prices) >= 10 else 0
        mom_20d = (prices[-1] / prices[-20] - 1) * 100 if len(prices) >= 20 else 0

        # 综合动量分数
        raw_score = mom_5d * 0.5 + mom_10d * 0.3 + mom_20d * 0.2

        # 归一化到0-100
        score = 50 + raw_score * 2
        return max(0, min(100, score))

    def calculate_value_score(self, symbol: str) -> float:
        """计算价值因子分数"""
        data = self.analyzer.get_stock_data(symbol)
        if not data:
            return 50

        pe = data.get("pe_ratio", 0)
        eps = data.get("eps", 0)

        score = 50

        # PE估值评分
        if pe > 0:
            if pe < 10:
                score += 20
            elif pe < 15:
                score += 15
            elif pe < 20:
                score += 10
            elif pe < 30:
                score += 0
            elif pe < 50:
                score -= 10
            else:
                score -= 20

        # EPS评分
        if eps > 5:
            score += 10
        elif eps > 2:
            score += 5
        elif eps < 0:
            score -= 15

        return max(0, min(100, score))

    def calculate_quality_score(self, symbol: str) -> float:
        """计算质量因子分数"""
        data = self.analyzer.get_stock_data(symbol)
        if not data:
            return 50

        score = 50

        # Beta评分（越接近1越稳定）
        beta = data.get("beta", 1.0)
        if 0.8 <= beta <= 1.2:
            score += 15
        elif 0.5 <= beta <= 1.5:
            score += 5
        else:
            score -= 10

        # 市值评分（大市值偏稳定）
        market_cap = data.get("market_cap", 0)
        if market_cap > 100e9:  # >1000亿
            score += 15
        elif market_cap > 10e9:  # >100亿
            score += 10
        elif market_cap > 1e9:  # >10亿
            score += 5
        else:
            score -= 5

        return max(0, min(100, score))


def generate_alpha_signals(symbols: List[str], strategy: str = "momentum") -> Dict:
    """
    生成Alpha交易信号

    Args:
        symbols: 股票代码列表
        strategy: 策略类型 (momentum/value/quality/combined)

    Returns:
        交易信号
    """
    generator = AlphaGenerator()
    signals = []

    for symbol in symbols:
        try:
            analysis = analyze_stock(symbol)

            if "error" in analysis:
                continue

            # 根据策略计算分数
            if strategy == "momentum":
                score = generator.calculate_momentum_score(symbol)
            elif strategy == "value":
                score = generator.calculate_value_score(symbol)
            elif strategy == "quality":
                score = generator.calculate_quality_score(symbol)
            else:  # combined
                mom = generator.calculate_momentum_score(symbol)
                val = generator.calculate_value_score(symbol)
                qual = generator.calculate_quality_score(symbol)
                score = mom * 0.4 + val * 0.3 + qual * 0.3

            # 生成信号
            if score >= 70:
                action = "STRONG_BUY"
                confidence = min(0.95, score / 100)
            elif score >= 60:
                action = "BUY"
                confidence = min(0.8, score / 100)
            elif score >= 45:
                action = "HOLD"
                confidence = 0.5
            elif score >= 35:
                action = "SELL"
                confidence = min(0.7, (100 - score) / 100)
            else:
                action = "STRONG_SELL"
                confidence = min(0.9, (100 - score) / 100)

            signals.append({
                "symbol": symbol,
                "score": round(score, 1),
                "action": action,
                "confidence": round(confidence, 2),
                "price": analysis.get("price", 0),
                "strategy": strategy
            })

        except Exception as e:
            continue

    # 按分数排序
    signals.sort(key=lambda x: x["score"], reverse=True)

    return {
        "strategy": strategy,
        "signals": signals,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total": len(signals),
            "strong_buy": sum(1 for s in signals if s["action"] == "STRONG_BUY"),
            "buy": sum(1 for s in signals if s["action"] == "BUY"),
            "hold": sum(1 for s in signals if s["action"] == "HOLD"),
            "sell": sum(1 for s in signals if s["action"] == "SELL"),
            "strong_sell": sum(1 for s in signals if s["action"] == "STRONG_SELL")
        }
    }


def run_factor_model(symbols: List[str], factors: List[str] = None) -> Dict:
    """
    运行多因子模型评分

    Args:
        symbols: 股票代码列表
        factors: 因子列表

    Returns:
        因子模型评分结果
    """
    if factors is None:
        factors = ["value", "momentum", "quality"]

    generator = AlphaGenerator()
    results = []

    for symbol in symbols:
        try:
            scores = {}

            if "value" in factors:
                scores["value"] = generator.calculate_value_score(symbol)

            if "momentum" in factors:
                scores["momentum"] = generator.calculate_momentum_score(symbol)

            if "quality" in factors:
                scores["quality"] = generator.calculate_quality_score(symbol)

            if "growth" in factors:
                # 成长因子（简化版本）
                data = generator.analyzer.get_stock_data(symbol)
                eps = data.get("eps", 0) if data else 0
                scores["growth"] = 50 + min(30, eps * 5)

            if "volatility" in factors:
                # 波动率因子（低波动优先）
                data = generator.analyzer.get_stock_data(symbol)
                beta = data.get("beta", 1.0) if data else 1.0
                scores["volatility"] = 70 - abs(beta - 1) * 30

            # 计算综合分数
            if scores:
                composite = sum(scores.values()) / len(scores)
            else:
                composite = 50

            results.append({
                "symbol": symbol,
                "factor_scores": {k: round(v, 1) for k, v in scores.items()},
                "composite_score": round(composite, 1)
            })

        except Exception as e:
            continue

    # 按综合分数排序
    results.sort(key=lambda x: x["composite_score"], reverse=True)

    # 添加排名
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return {
        "factors": factors,
        "rankings": results,
        "top_picks": results[:5] if len(results) >= 5 else results,
        "generated_at": datetime.now().isoformat()
    }


def screen_stocks(criteria: Dict, market: str = "US", limit: int = 20) -> Dict:
    """
    智能选股筛选器

    Args:
        criteria: 筛选条件
        market: 市场
        limit: 返回数量

    Returns:
        筛选结果
    """
    # 模拟股票池
    if market == "US":
        stock_pool = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
            "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "PYPL",
            "NFLX", "INTC", "AMD", "CRM", "ADBE", "CSCO", "PEP", "KO"
        ]
    elif market == "CN":
        stock_pool = [
            "600519", "601318", "600036", "000858", "600276", "601166",
            "000333", "600900", "601398", "600000"
        ]
    else:
        stock_pool = ["0700.HK", "9988.HK", "0005.HK", "1299.HK", "2318.HK"]

    generator = AlphaGenerator()
    results = []

    for symbol in stock_pool:
        try:
            data = generator.analyzer.get_stock_data(symbol)
            if not data:
                continue

            # 应用筛选条件
            passed = True

            if "min_market_cap" in criteria:
                if data.get("market_cap", 0) < criteria["min_market_cap"]:
                    passed = False

            if "max_pe" in criteria:
                pe = data.get("pe_ratio", 0)
                if pe <= 0 or pe > criteria["max_pe"]:
                    passed = False

            if "min_pe" in criteria:
                pe = data.get("pe_ratio", 0)
                if pe < criteria["min_pe"]:
                    passed = False

            if passed:
                analysis = analyze_stock(symbol)
                results.append({
                    "symbol": symbol,
                    "name": data.get("name", symbol),
                    "price": data.get("price", 0),
                    "market_cap": data.get("market_cap", 0),
                    "pe_ratio": data.get("pe_ratio", 0),
                    "sector": data.get("sector", "Unknown"),
                    "score": analysis.get("overall_score", 50) if "error" not in analysis else 50,
                    "signal": analysis.get("signal", "HOLD") if "error" not in analysis else "HOLD"
                })

        except Exception:
            continue

    # 按评分排序
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:limit]

    return {
        "market": market,
        "criteria": criteria,
        "results": results,
        "total_found": len(results),
        "generated_at": datetime.now().isoformat()
    }


def find_similar_stocks(symbol: str, limit: int = 10) -> Dict:
    """
    寻找相似股票

    Args:
        symbol: 参考股票
        limit: 返回数量

    Returns:
        相似股票列表
    """
    generator = AlphaGenerator()

    # 获取参考股票数据
    ref_data = generator.analyzer.get_stock_data(symbol)
    if not ref_data:
        return {"error": f"无法获取 {symbol} 数据"}

    ref_sector = ref_data.get("sector", "Unknown")
    ref_beta = ref_data.get("beta", 1.0)
    ref_pe = ref_data.get("pe_ratio", 15)

    # 计算参考股票的因子分数
    ref_mom = generator.calculate_momentum_score(symbol)
    ref_val = generator.calculate_value_score(symbol)
    ref_qual = generator.calculate_quality_score(symbol)

    # 模拟股票池
    candidates = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
        "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS",
        "NFLX", "INTC", "AMD", "CRM", "ADBE", "CSCO", "PEP", "KO"
    ]

    # 排除参考股票
    candidates = [c for c in candidates if c != symbol]

    similar = []

    for cand in candidates:
        try:
            cand_data = generator.analyzer.get_stock_data(cand)
            if not cand_data:
                continue

            # 计算相似度
            sector_match = 1.0 if cand_data.get("sector") == ref_sector else 0.5

            beta_diff = abs(cand_data.get("beta", 1.0) - ref_beta)
            beta_sim = max(0, 1 - beta_diff)

            pe_diff = abs(cand_data.get("pe_ratio", 15) - ref_pe) / max(ref_pe, 1)
            pe_sim = max(0, 1 - pe_diff)

            # 因子相似度
            cand_mom = generator.calculate_momentum_score(cand)
            cand_val = generator.calculate_value_score(cand)
            cand_qual = generator.calculate_quality_score(cand)

            factor_sim = 1 - (
                abs(cand_mom - ref_mom) +
                abs(cand_val - ref_val) +
                abs(cand_qual - ref_qual)
            ) / 300

            # 综合相似度
            similarity = (
                sector_match * 0.3 +
                beta_sim * 0.2 +
                pe_sim * 0.2 +
                factor_sim * 0.3
            )

            similar.append({
                "symbol": cand,
                "name": cand_data.get("name", cand),
                "similarity": round(similarity * 100, 1),
                "sector": cand_data.get("sector", "Unknown"),
                "price": cand_data.get("price", 0),
                "pe_ratio": cand_data.get("pe_ratio", 0),
                "beta": cand_data.get("beta", 1.0)
            })

        except Exception:
            continue

    # 按相似度排序
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    similar = similar[:limit]

    return {
        "reference": {
            "symbol": symbol,
            "name": ref_data.get("name", symbol),
            "sector": ref_sector,
            "pe_ratio": ref_pe,
            "beta": ref_beta
        },
        "similar_stocks": similar,
        "generated_at": datetime.now().isoformat()
    }
