"""Reproducible monthly total-return ETF portfolio backtest (2011–2025)."""
import csv
import datetime as dt
import json
import math
from pathlib import Path
import statistics
import urllib.request

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
ASSETS = {"VTI": .40, "VEA": .15, "BND": .25, "GLD": .10, "VNQ": .05, "SHY": .05}
BENCH = {"VTI": .60, "BND": .40}
TICKERS = list(ASSETS)
START = dt.datetime(2010, 12, 1, tzinfo=dt.timezone.utc)
END = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)


def prices(ticker):
    path = DATA / f"{ticker}_yahoo_chart.json"
    if not path.exists():
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
               f"?period1={int(START.timestamp())}&period2={int(END.timestamp())}"
               "&interval=1mo&events=history&includeAdjustedClose=true")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            path.write_bytes(response.read())
    result = json.loads(path.read_text(encoding="utf-8"))["chart"]["result"][0]
    timestamps = result["timestamp"]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    return {dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m"): p
            for t, p in zip(timestamps, adjusted) if p is not None}


def metrics(returns):
    n = len(returns)
    growth = math.prod(1 + x for x in returns)
    peak = value = 1.0
    worst_dd = 0.0
    for r in returns:
        value *= 1 + r
        peak = max(peak, value)
        worst_dd = min(worst_dd, value / peak - 1)
    annual = growth ** (12 / n) - 1
    vol = statistics.stdev(returns) * math.sqrt(12)
    return {"ending_10000": 10000 * growth, "cagr": annual, "volatility": vol,
            "sharpe_zero_rf": statistics.mean(returns) * 12 / vol,
            "max_drawdown": worst_dd, "positive_months": sum(r > 0 for r in returns) / n}


def main():
    price = {t: prices(t) for t in TICKERS}
    months = sorted(set.intersection(*(set(x) for x in price.values())))
    months = [m for m in months if "2010-12" <= m <= "2025-12"]
    assert months[0] == "2010-12" and months[-1] == "2025-12" and len(months) == 181, (months[0], months[-1], len(months))
    rows, p_rets, b_rets = [], [], []
    p_val = b_val = 10000.0
    for prev, month in zip(months, months[1:]):
        asset_ret = {t: price[t][month] / price[t][prev] - 1 for t in TICKERS}
        pr = sum(w * asset_ret[t] for t, w in ASSETS.items())
        br = sum(w * asset_ret[t] for t, w in BENCH.items())
        p_val *= 1 + pr
        b_val *= 1 + br
        p_rets.append(pr)
        b_rets.append(br)
        rows.append({"month": month, **{f"{t}_adjusted_close": price[t][month] for t in TICKERS},
                     **{f"{t}_return": asset_ret[t] for t in TICKERS},
                     "portfolio_return": pr, "benchmark_return": br,
                     "portfolio_value": p_val, "benchmark_value": b_val})
    with (OUT / "monthly_backtest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    yearly = []
    for year in range(2011, 2026):
        subset = [r for r in rows if r["month"].startswith(str(year))]
        yearly.append((year, math.prod(1 + r["portfolio_return"] for r in subset) - 1,
                       math.prod(1 + r["benchmark_return"] for r in subset) - 1))
    with (OUT / "annual_returns.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "portfolio", "benchmark_60_40"])
        writer.writerows(yearly)
    pm, bm = metrics(p_rets), metrics(b_rets)
    report = ["# Multi-asset portfolio backtest", "",
              "## Hypothetical client and allocation", "",
              "Client: age 40, 15+ year horizon, moderate risk tolerance, no near-term withdrawals. Starting balance $10,000.", "",
              "| Sleeve | ETF proxy | Target | Role |", "|---|---|---:|---|",
              "| US equities | VTI | 40% | Broad domestic growth |",
              "| Developed international equities | VEA | 15% | Geographic diversification |",
              "| US investment-grade bonds | BND | 25% | Income and rate exposure |",
              "| Gold | GLD | 10% | Alternative asset and inflation sensitivity |",
              "| US REITs | VNQ | 5% | Listed real estate exposure |",
              "| Short Treasury bills | SHY | 5% | Cash-like reserve proxy |", "",
              "## Method", "",
              "Adjusted monthly closes from Yahoo Finance, December 2010–December 2025. Returns include the provider's distribution and split adjustments. Invest at the December 2010 close, rebalance to fixed weights at each month end, and measure January 2011–December 2025. Benchmark: 60% VTI / 40% BND, same rebalance schedule. No fees, taxes, slippage, cash flows, or inflation adjustment. SHY is a short Treasury ETF, not a bank cash account. Sharpe uses a zero risk-free rate for transparent comparison; use an actual cash rate for an investment-grade Sharpe calculation. Results are hypothetical and depend on the selected proxies and period.", "",
              "## Results", "", "| Metric | Multi-asset | 60/40 benchmark |", "|---|---:|---:|"]
    for label, key, fmt in [("Ending value of $10,000", "ending_10000", "${:,.0f}"),
                            ("CAGR", "cagr", "{:.2%}"), ("Annualized volatility", "volatility", "{:.2%}"),
                            ("Sharpe (0% risk-free)", "sharpe_zero_rf", "{:.2f}"),
                            ("Maximum drawdown (month end)", "max_drawdown", "{:.2%}"),
                            ("Positive months", "positive_months", "{:.1%}")]:
        report.append(f"| {label} | {fmt.format(pm[key])} | {fmt.format(bm[key])} |")
    report += ["", "## Annual returns", "", "| Year | Multi-asset | 60/40 |", "|---:|---:|---:|"]
    report += [f"| {y} | {p:.2%} | {b:.2%} |" for y, p, b in yearly]
    report += ["", "## Interpretation", "",
               "The diversified mix trades some equity upside for exposure to bonds, gold, real estate, and short Treasuries. Compare CAGR together with volatility and drawdown; a higher return alone does not establish a better fit for a moderate-risk client. The 2022 stock/bond selloff is a useful stress test, while 2020 and 2021 show different market conditions. Gold and REITs can also experience substantial losses, and correlations change over time.", "",
               "## Data and reproducibility", "",
               "Source: [Yahoo Finance historical data help](https://help.yahoo.com/kb/sln2311.html). Raw Yahoo chart API responses are retained in `data/`. Run `python backtest.py` to regenerate the CSVs and this report. The CSV contains every monthly adjusted close, asset return, portfolio return, and wealth path. Figures may change if the data provider revises adjusted history."]
    (ROOT / "README.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"portfolio": pm, "benchmark": bm, "months": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
