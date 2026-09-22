# Multi-asset portfolio backtest

## Hypothetical client and allocation

Client: age 40, 15+ year horizon, moderate risk tolerance, no near-term withdrawals. Starting balance $10,000.

| Sleeve | ETF proxy | Target | Role |
|---|---|---:|---|
| US equities | VTI | 40% | Broad domestic growth |
| Developed international equities | VEA | 15% | Geographic diversification |
| US investment-grade bonds | BND | 25% | Income and rate exposure |
| Gold | GLD | 10% | Alternative asset and inflation sensitivity |
| US REITs | VNQ | 5% | Listed real estate exposure |
| Short Treasury bills | SHY | 5% | Cash-like reserve proxy |

## Method

Adjusted monthly closes from Yahoo Finance, December 2010–December 2025. Returns include the provider's distribution and split adjustments. Invest at the December 2010 close, rebalance to fixed weights at each month end, and measure January 2011–December 2025. Benchmark: 60% VTI / 40% BND, same rebalance schedule. No fees, taxes, slippage, cash flows, or inflation adjustment. SHY is a short Treasury ETF, not a bank cash account. Sharpe uses a zero risk-free rate for transparent comparison; use an actual cash rate for an investment-grade Sharpe calculation. Results are hypothetical and depend on the selected proxies and period.

## Results

| Metric | Multi-asset | 60/40 benchmark |
|---|---:|---:|
| Ending value of $10,000 | $34,046 | $37,335 |
| CAGR | 8.51% | 9.18% |
| Annualized volatility | 9.41% | 9.43% |
| Sharpe (0% risk-free) | 0.92 | 0.98 |
| Maximum drawdown (month end) | -20.36% | -20.66% |
| Positive months | 66.7% | 68.3% |

## Annual returns

| Year | Multi-asset | 60/40 |
|---:|---:|---:|
| 2011 | 2.40% | 4.06% |
| 2012 | 11.76% | 11.03% |
| 2013 | 11.83% | 18.09% |
| 2014 | 6.77% | 9.90% |
| 2015 | -0.35% | 0.67% |
| 2016 | 7.76% | 8.79% |
| 2017 | 14.73% | 14.06% |
| 2018 | -4.45% | -2.83% |
| 2019 | 21.27% | 21.80% |
| 2020 | 14.91% | 16.40% |
| 2021 | 12.57% | 14.04% |
| 2022 | -14.75% | -16.70% |
| 2023 | 16.56% | 17.61% |
| 2024 | 13.19% | 14.44% |
| 2025 | 19.95% | 13.17% |

## Interpretation

The diversified mix trades some equity upside for exposure to bonds, gold, real estate, and short Treasuries. Compare CAGR together with volatility and drawdown; a higher return alone does not establish a better fit for a moderate-risk client. The 2022 stock/bond selloff is a useful stress test, while 2020 and 2021 show different market conditions. Gold and REITs can also experience substantial losses, and correlations change over time.

## Data and reproducibility

Source: [Yahoo Finance historical data help](https://help.yahoo.com/kb/sln2311.html). Raw Yahoo chart API responses are retained in `data/`. Run `python backtest.py` to regenerate the CSVs and this report. The CSV contains every monthly adjusted close, asset return, portfolio return, and wealth path. Figures may change if the data provider revises adjusted history.
