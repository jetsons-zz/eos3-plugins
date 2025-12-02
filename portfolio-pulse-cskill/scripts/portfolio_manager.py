"""
Portfolio Manager - 投资组合管理
管理和跟踪投资组合
"""

from datetime import datetime
from typing import Dict, List, Optional
from .asset_tracker import get_multi_asset_prices


class Portfolio:
    """投资组合类"""

    def __init__(self, name: str = "我的投资组合", base_currency: str = "CNY"):
        self.name = name
        self.base_currency = base_currency
        self.holdings = []
        self.created_at = datetime.now()

    def add_holding(
        self,
        symbol: str,
        quantity: float,
        cost_basis: float,
        asset_type: str = "stock"
    ):
        """添加持仓"""
        self.holdings.append({
            "symbol": symbol,
            "quantity": quantity,
            "cost_basis": cost_basis,
            "type": asset_type,
            "added_at": datetime.now().isoformat()
        })

    def remove_holding(self, symbol: str):
        """移除持仓"""
        self.holdings = [h for h in self.holdings if h["symbol"] != symbol]

    def get_current_values(self) -> List[Dict]:
        """获取当前持仓价值"""
        return get_multi_asset_prices(self.holdings)

    def get_total_value(self) -> Dict:
        """获取投资组合总价值"""
        values = self.get_current_values()

        total_value = 0
        total_cost = 0
        by_type = {}

        for v in values:
            if "value" in v:
                total_value += v["value"]
                total_cost += v.get("cost_basis", 0)

                asset_type = v.get("type", "other")
                if asset_type not in by_type:
                    by_type[asset_type] = 0
                by_type[asset_type] += v["value"]

        profit_loss = total_value - total_cost
        profit_loss_pct = (profit_loss / total_cost * 100) if total_cost else 0

        return {
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "profit_loss": round(profit_loss, 2),
            "profit_loss_percent": round(profit_loss_pct, 2),
            "by_type": by_type,
            "holdings_count": len(self.holdings),
            "updated_at": datetime.now().isoformat()
        }

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "base_currency": self.base_currency,
            "holdings": self.holdings,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Portfolio':
        """从字典创建"""
        portfolio = cls(data.get("name", "Portfolio"), data.get("base_currency", "CNY"))
        portfolio.holdings = data.get("holdings", [])
        return portfolio


# 示例投资组合
SAMPLE_PORTFOLIO = {
    "name": "示例投资组合",
    "base_currency": "CNY",
    "holdings": [
        {"symbol": "AAPL", "quantity": 100, "cost_basis": 15000, "type": "stock"},
        {"symbol": "MSFT", "quantity": 50, "cost_basis": 18000, "type": "stock"},
        {"symbol": "BTC-USD", "quantity": 0.5, "cost_basis": 150000, "type": "crypto"},
        {"symbol": "GC=F", "quantity": 10, "cost_basis": 280000, "type": "commodity"},
    ]
}


def add_holding(portfolio: Portfolio, symbol: str, quantity: float, cost: float, asset_type: str = "stock"):
    """便捷函数：添加持仓"""
    portfolio.add_holding(symbol, quantity, cost, asset_type)


def get_portfolio_value(holdings: List[Dict]) -> Dict:
    """
    计算投资组合价值

    Args:
        holdings: 持仓列表

    Returns:
        组合价值信息
    """
    portfolio = Portfolio()
    for h in holdings:
        portfolio.add_holding(
            h["symbol"],
            h["quantity"],
            h.get("cost_basis", 0),
            h.get("type", "stock")
        )
    return portfolio.get_total_value()


def get_portfolio_performance(holdings: List[Dict], period: str = "1mo") -> Dict:
    """
    计算投资组合表现

    Args:
        holdings: 持仓列表
        period: 时间周期

    Returns:
        表现分析
    """
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance not installed"}

    total_start_value = 0
    total_current_value = 0

    period_map = {
        "1d": 1, "5d": 5, "1mo": 30, "3mo": 90, "6mo": 180, "1y": 365
    }
    days = period_map.get(period, 30)

    performances = []

    for h in holdings:
        symbol = h["symbol"]
        quantity = h["quantity"]

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                continue

            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]

            start_value = start_price * quantity
            end_value = end_price * quantity

            total_start_value += start_value
            total_current_value += end_value

            period_return = ((end_price - start_price) / start_price) * 100

            performances.append({
                "symbol": symbol,
                "quantity": quantity,
                "start_value": round(start_value, 2),
                "current_value": round(end_value, 2),
                "period_return": round(period_return, 2),
                "contribution": round(end_value - start_value, 2)
            })
        except:
            pass

    # 计算总表现
    total_return = 0
    if total_start_value > 0:
        total_return = ((total_current_value - total_start_value) / total_start_value) * 100

    # 按贡献排序
    performances.sort(key=lambda x: x.get("contribution", 0), reverse=True)

    return {
        "period": period,
        "start_value": round(total_start_value, 2),
        "current_value": round(total_current_value, 2),
        "total_return": round(total_return, 2),
        "total_gain_loss": round(total_current_value - total_start_value, 2),
        "top_performers": performances[:3] if performances else [],
        "worst_performers": performances[-3:][::-1] if len(performances) > 3 else [],
        "all_holdings": performances
    }
