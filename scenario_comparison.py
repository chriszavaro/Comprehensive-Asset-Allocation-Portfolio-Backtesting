"""Compare five fixed-weight portfolios over a shared 2015–2025 history."""

import math

import pandas as pd
import yfinance as yf


START = "2014-12-01"  # Prior month-end price for the January 2015 return.
END = "2026-01-01"
FIRST_MONTH = "2014-12"
LAST_MONTH = "2025-12"
INITIAL_VALUE = 10_000

PORTFOLIOS = {
    "Diversified core": {"VTI": .40, "VEA": .15, "BND": .25, "GLD": .10, "VNQ": .05, "SHY": .05},
    "Core + 5% Bitcoin": {"VTI": .35, "VEA": .15, "BND": .25, "GLD": .10, "VNQ": .05, "SHY": .05, "BTC-USD": .05},
    "Technology heavy": {"VGT": .65, "VTI": .20, "BND": .10, "SHY": .05},
    "Dividend focus": {"SCHD": .50, "VYM": .25, "BND": .20, "SHY": .05},
    "60/40 benchmark": {"VTI": .60, "BND": .40},
}


def load_monthly_prices():
    """Get a common monthly adjusted-close history for all portfolio assets."""
    for name, weights in PORTFOLIOS.items():
        if not math.isclose(sum(weights.values()), 1.0, abs_tol=1e-12):
            raise ValueError(f"Weights do not total 100%: {name}")
    tickers = sorted({ticker for weights in PORTFOLIOS.values() for ticker in weights})
    raw = yf.download(
        tickers, start=START, end=END, interval="1mo",
        auto_adjust=True, group_by="ticker", multi_level_index=True,
        progress=False, threads=False,
    )
    prices = pd.DataFrame({ticker: raw[ticker]["Close"] for ticker in tickers})
    prices.index = pd.PeriodIndex(prices.index, freq="M")
    prices = prices.loc[FIRST_MONTH:LAST_MONTH, tickers]
    expected = pd.period_range(FIRST_MONTH, LAST_MONTH, freq="M")
    if not prices.index.equals(expected) or prices.isna().any().any():
        raise ValueError("Price data must contain every month from 2014-12 through 2025-12 for all assets")
    return prices


def run_comparison(prices):
    """Return ETF returns, monthly portfolio returns, and growth of $10,000."""
    asset_returns = prices.pct_change().iloc[1:]
    returns = pd.DataFrame({
        name: asset_returns.mul(pd.Series(weights)).sum(axis=1)
        for name, weights in PORTFOLIOS.items()
    })
    wealth = INITIAL_VALUE * (1 + returns).cumprod()
    return asset_returns, returns, wealth


def performance_summary(returns, wealth):
    """Calculate like-for-like return and risk statistics for each portfolio."""
    months = len(returns)
    peak = wealth.cummax().clip(lower=INITIAL_VALUE)
    return pd.DataFrame({
        "Ending value": wealth.iloc[-1],
        "CAGR": (wealth.iloc[-1] / INITIAL_VALUE) ** (12 / months) - 1,
        "Volatility": returns.std() * math.sqrt(12),
        "Sharpe (0% RF)": returns.mean() * 12 / (returns.std() * math.sqrt(12)),
        "Max drawdown": wealth.div(peak).sub(1).min(),
        "Positive months": returns.gt(0).mean(),
    })


if __name__ == "__main__":
    prices = load_monthly_prices()
    _, returns, wealth = run_comparison(prices)
    print(performance_summary(returns, wealth).round(4).to_string())
