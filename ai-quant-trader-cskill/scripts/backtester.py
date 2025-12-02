"""
Backtester - 策略回测引擎
历史回测、绩效分析、参数优化
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable

from .market_analyzer import MarketAnalyzer, calculate_sma, calculate_ema


class Backtester:
    """回测引擎"""

    def __init__(self):
        self.analyzer = MarketAnalyzer()
        self.strategies = {
            "golden_cross": self._strategy_golden_cross,
            "rsi_reversal": self._strategy_rsi_reversal,
            "breakout": self._strategy_breakout,
            "mean_reversion": self._strategy_mean_reversion
        }

    def _strategy_golden_cross(self, prices: List[float], params: Dict) -> List[Dict]:
        """
        金叉死叉策略
        MA快线上穿慢线买入，下穿卖出
        """
        fast_period = params.get("fast", 10)
        slow_period = params.get("slow", 30)

        ma_fast = calculate_sma(prices, fast_period)
        ma_slow = calculate_sma(prices, slow_period)

        signals = []

        for i in range(slow_period, len(prices)):
            if ma_fast[i] > ma_slow[i] and ma_fast[i-1] <= ma_slow[i-1]:
                signals.append({"day": i, "action": "BUY", "price": prices[i]})
            elif ma_fast[i] < ma_slow[i] and ma_fast[i-1] >= ma_slow[i-1]:
                signals.append({"day": i, "action": "SELL", "price": prices[i]})

        return signals

    def _strategy_rsi_reversal(self, prices: List[float], params: Dict) -> List[Dict]:
        """
        RSI反转策略
        RSI超卖买入，超买卖出
        """
        period = params.get("period", 14)
        oversold = params.get("oversold", 30)
        overbought = params.get("overbought", 70)

        if len(prices) < period + 1:
            return []

        # 计算RSI
        signals = []
        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

            if i >= period:
                avg_gain = sum(gains[-period:]) / period
                avg_loss = sum(losses[-period:]) / period

                if avg_loss == 0:
                    rsi = 100
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))

                if rsi < oversold:
                    signals.append({"day": i, "action": "BUY", "price": prices[i], "rsi": rsi})
                elif rsi > overbought:
                    signals.append({"day": i, "action": "SELL", "price": prices[i], "rsi": rsi})

        return signals

    def _strategy_breakout(self, prices: List[float], params: Dict) -> List[Dict]:
        """
        突破策略
        突破N日高点买入，跌破N日低点卖出
        """
        period = params.get("period", 20)

        if len(prices) < period:
            return []

        signals = []

        for i in range(period, len(prices)):
            recent_high = max(prices[i-period:i])
            recent_low = min(prices[i-period:i])

            if prices[i] > recent_high:
                signals.append({"day": i, "action": "BUY", "price": prices[i]})
            elif prices[i] < recent_low:
                signals.append({"day": i, "action": "SELL", "price": prices[i]})

        return signals

    def _strategy_mean_reversion(self, prices: List[float], params: Dict) -> List[Dict]:
        """
        均值回归策略
        偏离均线过多时反向操作
        """
        period = params.get("period", 20)
        threshold = params.get("threshold", 0.05)  # 5%偏离

        ma = calculate_sma(prices, period)
        signals = []

        for i in range(period, len(prices)):
            deviation = (prices[i] - ma[i]) / ma[i]

            if deviation < -threshold:  # 超跌买入
                signals.append({"day": i, "action": "BUY", "price": prices[i], "deviation": deviation})
            elif deviation > threshold:  # 超涨卖出
                signals.append({"day": i, "action": "SELL", "price": prices[i], "deviation": deviation})

        return signals


def backtest_strategy(
    strategy: str,
    symbols: List[str],
    start_date: str,
    end_date: str,
    initial_capital: float = 100000,
    params: Dict = None
) -> Dict:
    """
    回测交易策略

    Args:
        strategy: 策略名称
        symbols: 标的列表
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        params: 策略参数

    Returns:
        回测结果
    """
    backtester = Backtester()

    if strategy not in backtester.strategies:
        return {"error": f"未知策略: {strategy}，支持: {list(backtester.strategies.keys())}"}

    if params is None:
        params = {}

    all_trades = []
    total_return = 0
    equity_curve = [initial_capital]

    for symbol in symbols:
        data = backtester.analyzer.get_stock_data(symbol, period="1y")
        if not data or "history" not in data:
            continue

        prices = data["history"]["close"]
        dates = data["history"]["dates"]

        # 运行策略
        signals = backtester.strategies[strategy](prices, params)

        # 模拟交易
        position = 0
        entry_price = 0
        cash = initial_capital / len(symbols)

        for sig in signals:
            day = sig["day"]
            action = sig["action"]
            price = sig["price"]

            if action == "BUY" and position == 0:
                shares = int(cash / price)
                if shares > 0:
                    position = shares
                    entry_price = price
                    cash -= shares * price

                    all_trades.append({
                        "symbol": symbol,
                        "date": dates[day] if day < len(dates) else f"Day {day}",
                        "action": "BUY",
                        "shares": shares,
                        "price": price
                    })

            elif action == "SELL" and position > 0:
                pnl = (price - entry_price) * position
                cash += position * price

                all_trades.append({
                    "symbol": symbol,
                    "date": dates[day] if day < len(dates) else f"Day {day}",
                    "action": "SELL",
                    "shares": position,
                    "price": price,
                    "pnl": round(pnl, 2)
                })

                position = 0

        # 计算最终价值
        if position > 0:
            final_value = cash + position * prices[-1]
        else:
            final_value = cash

        equity_curve.append(final_value)

    # 汇总统计
    final_capital = sum(equity_curve[1:]) if len(equity_curve) > 1 else initial_capital
    total_return = (final_capital - initial_capital) / initial_capital * 100

    # 分析交易
    winning_trades = [t for t in all_trades if t.get("pnl", 0) > 0]
    losing_trades = [t for t in all_trades if t.get("pnl", 0) < 0]

    performance = analyze_performance(all_trades)

    return {
        "strategy": strategy,
        "symbols": symbols,
        "period": f"{start_date} to {end_date}",
        "initial_capital": initial_capital,
        "final_capital": round(final_capital, 2),
        "total_return": round(total_return, 2),
        "total_trades": len([t for t in all_trades if t["action"] == "SELL"]),
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "win_rate": performance.get("win_rate", 0),
        "sharpe_ratio": performance.get("sharpe_ratio", 0),
        "max_drawdown": performance.get("max_drawdown", 0),
        "profit_factor": performance.get("profit_factor", 0),
        "recent_trades": all_trades[-10:],
        "generated_at": datetime.now().isoformat()
    }


def analyze_performance(trades: List[Dict]) -> Dict:
    """
    分析策略绩效

    Args:
        trades: 交易记录

    Returns:
        绩效分析
    """
    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "profit_factor": 0
        }

    # 筛选已平仓交易
    closed_trades = [t for t in trades if "pnl" in t]

    if not closed_trades:
        return {
            "total_trades": len(trades),
            "win_rate": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "profit_factor": 0
        }

    # 计算基本指标
    pnls = [t["pnl"] for t in closed_trades]
    total_trades = len(closed_trades)
    winning = [p for p in pnls if p > 0]
    losing = [p for p in pnls if p < 0]

    win_rate = len(winning) / total_trades * 100 if total_trades > 0 else 0

    # 盈亏比
    avg_win = sum(winning) / len(winning) if winning else 0
    avg_loss = abs(sum(losing) / len(losing)) if losing else 0
    risk_reward = avg_win / avg_loss if avg_loss > 0 else 0

    # 盈利因子
    total_profit = sum(winning)
    total_loss = abs(sum(losing))
    profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')

    # 夏普比率（简化计算）
    if len(pnls) > 1:
        returns = [p / 10000 for p in pnls]  # 假设每笔约1万本金
        avg_return = sum(returns) / len(returns)
        std_return = math.sqrt(sum((r - avg_return)**2 for r in returns) / len(returns))
        sharpe_ratio = (avg_return * 252 / std_return * math.sqrt(252)) if std_return > 0 else 0
    else:
        sharpe_ratio = 0

    # 最大回撤
    cumulative = [0]
    for pnl in pnls:
        cumulative.append(cumulative[-1] + pnl)

    peak = cumulative[0]
    max_drawdown = 0
    for val in cumulative:
        if val > peak:
            peak = val
        drawdown = (peak - val) / peak * 100 if peak > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)

    return {
        "total_trades": total_trades,
        "winning_trades": len(winning),
        "losing_trades": len(losing),
        "win_rate": round(win_rate, 1),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "risk_reward_ratio": round(risk_reward, 2),
        "profit_factor": round(profit_factor, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown": round(max_drawdown, 1),
        "total_pnl": round(sum(pnls), 2),
        "largest_win": round(max(pnls), 2) if pnls else 0,
        "largest_loss": round(min(pnls), 2) if pnls else 0
    }


def compare_strategies(strategies: List[str], benchmark: str = "SPY") -> Dict:
    """
    比较多个策略绩效

    Args:
        strategies: 策略列表
        benchmark: 基准

    Returns:
        比较结果
    """
    results = []

    for strategy in strategies:
        result = backtest_strategy(
            strategy=strategy,
            symbols=[benchmark],
            start_date="2023-01-01",
            end_date="2023-12-31"
        )

        if "error" not in result:
            results.append({
                "strategy": strategy,
                "total_return": result["total_return"],
                "sharpe_ratio": result["sharpe_ratio"],
                "max_drawdown": result["max_drawdown"],
                "win_rate": result["win_rate"],
                "total_trades": result["total_trades"]
            })

    # 获取基准收益
    backtester = Backtester()
    bench_data = backtester.analyzer.get_stock_data(benchmark, period="1y")
    if bench_data and "history" in bench_data:
        prices = bench_data["history"]["close"]
        benchmark_return = (prices[-1] / prices[0] - 1) * 100 if prices else 0
    else:
        benchmark_return = 0

    # 排序
    results.sort(key=lambda x: x["total_return"], reverse=True)

    return {
        "benchmark": {
            "symbol": benchmark,
            "return": round(benchmark_return, 2)
        },
        "strategies": results,
        "best_performer": results[0] if results else None,
        "generated_at": datetime.now().isoformat()
    }


def optimize_parameters(strategy: str, param_grid: Dict) -> Dict:
    """
    参数优化

    Args:
        strategy: 策略名称
        param_grid: 参数网格

    Returns:
        优化结果
    """
    backtester = Backtester()

    if strategy not in backtester.strategies:
        return {"error": f"未知策略: {strategy}"}

    # 生成参数组合
    from itertools import product

    param_names = list(param_grid.keys())
    param_values = [param_grid[name] for name in param_names]

    results = []

    for values in product(*param_values):
        params = dict(zip(param_names, values))

        result = backtest_strategy(
            strategy=strategy,
            symbols=["SPY"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            params=params
        )

        if "error" not in result:
            results.append({
                "params": params,
                "total_return": result["total_return"],
                "sharpe_ratio": result["sharpe_ratio"],
                "max_drawdown": result["max_drawdown"],
                "win_rate": result["win_rate"]
            })

    # 按夏普比率排序
    results.sort(key=lambda x: x["sharpe_ratio"], reverse=True)

    return {
        "strategy": strategy,
        "param_grid": param_grid,
        "total_combinations": len(results),
        "best_params": results[0] if results else None,
        "top_5": results[:5],
        "generated_at": datetime.now().isoformat()
    }
