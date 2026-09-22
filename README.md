# Multi-asset portfolio backtest

## Client proposal

Client: age 40, 15+ year horizon, moderate risk tolerance, no near-term withdrawals. Starting balance $10,000.

### Proposed diversified core

| Sleeve | ETF proxy | Target | Role |
|---|---|---:|---|
| US equities | VTI | 40% | Broad domestic growth |
| Developed international equities | VEA | 15% | Geographic diversification |
| US investment-grade bonds | BND | 25% | Income and rate exposure |
| Gold | GLD | 10% | Alternative asset and inflation sensitivity |
| US REITs | VNQ | 5% | Listed real estate exposure |
| Short-term US Treasuries | SHY | 5% | Cash-like reserve proxy |

### Alternative strategies for discussion

These illustrate different objectives and risk exposures; the historical comparison below does not establish that any alternative is suitable for this moderate-risk client.

| Strategy | Proposed allocation | What changes |
|---|---|---|
| Core + 5% Bitcoin | 35% VTI, 15% VEA, 25% BND, 10% GLD, 5% VNQ, 5% SHY, 5% BTC-USD | Funds Bitcoin by reducing the core's VTI weight from 40% to 35%; adds substantial crypto risk. |
| Technology heavy | 65% VGT, 20% VTI, 10% BND, 5% SHY | Concentrates in the US information technology sector and US stocks. |
| Dividend focus | 50% SCHD, 25% VYM, 20% BND, 5% SHY | Tilts toward dividend-oriented US stocks; backtest assumes distributions are reinvested. |
| 60/40 benchmark | 60% VTI, 40% BND | Simple stock/bond comparison, not a client recommendation. |

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

## Scenario results

The [scenario notebook](scenario_comparison.ipynb) compares five portfolios over the **same January 2015–December 2025 window** (132 monthly returns). This shorter period accommodates Bitcoin price history. Each starts at $10,000 and is rebalanced monthly. The original 2011–2025 analysis above remains unchanged; its ending values should not be compared directly with the 2015–2025 values below.

| Portfolio | CAGR | Volatility | Max month-end drawdown | Ending $10,000 |
|---|---:|---:|---:|---:|
| Diversified core | 8.65% | 9.84% | -20.36% | $24,915 |
| Core + 5% Bitcoin | 11.98% | 10.86% | -22.17% | $34,703 |
| Technology heavy | 16.50% | 15.76% | -27.94% | $53,627 |
| Dividend focus | 8.37% | 11.08% | -16.56% | $24,215 |
| 60/40 benchmark | 8.65% | 10.18% | -20.66% | $24,899 |

The technology portfolio had the highest historical return and the deepest drawdown. Adding 5% Bitcoin raised historical CAGR but also volatility and maximum drawdown. The dividend-focused portfolio had the smallest maximum month-end drawdown in this sample; its adjusted-price results measure **total return with dividends reinvested**, not cash dividend income or yield. These allocations are illustrative and were not optimized. Bitcoin trades continuously whereas ETFs trade on exchange days, so monthly observations are not perfectly synchronized.

To rerun the comparison, install `requirements.txt` in your Python environment and open `scenario_comparison.ipynb` from this project folder. The calculation module can also be run directly with `python scenario_comparison.py`. The notebook contains growth, drawdown, annual-return, and risk/return charts and does not overwrite the existing CSVs. Data sources and fund descriptions: [Yahoo Finance BTC-USD history](https://finance.yahoo.com/quote/BTC-USD/history/), [Schwab SCHD profile](https://www.schwabassetmanagement.com/products/schd), [Vanguard ETF list for VGT and VYM](https://investor.vanguard.com/investment-products/list/etfs).

## Annual returns

The original diversified core and 60/40 benchmark cover 2011–2025. New strategy columns begin in 2015, the shared comparison period required by the Bitcoin history. A dash means the strategy was not evaluated for that year in this comparison.

| Year | Diversified core | Core + 5% Bitcoin | Technology heavy | Dividend focus | 60/40 benchmark |
|---:|---:|---:|---:|---:|---:|
| 2011 | 2.40% | — | — | — | 4.06% |
| 2012 | 11.76% | — | — | — | 11.03% |
| 2013 | 11.83% | — | — | — | 18.09% |
| 2014 | 6.77% | — | — | — | 9.90% |
| 2015 | -0.35% | 1.94% | 3.59% | 0.23% | 0.67% |
| 2016 | 7.76% | 12.18% | 11.96% | 12.95% | 8.79% |
| 2017 | 14.73% | 33.78% | 28.25% | 15.16% | 14.06% |
| 2018 | -4.45% | -8.98% | 0.87% | -3.99% | -2.83% |
| 2019 | 21.27% | 25.10% | 38.24% | 21.56% | 21.80% |
| 2020 | 14.91% | 23.48% | 34.78% | 9.94% | 16.40% |
| 2021 | 12.57% | 15.48% | 24.34% | 20.56% | 14.04% |
| 2022 | -14.75% | -17.54% | -24.77% | -4.41% | -16.70% |
| 2023 | 16.56% | 21.41% | 39.33% | 5.36% | 17.61% |
| 2024 | 13.19% | 17.33% | 23.93% | 10.66% | 14.44% |
| 2025 | 19.95% | 18.95% | 18.76% | 7.74% | 13.17% |

## Interpretation

The diversified mix trades some equity upside for exposure to bonds, gold, real estate, and short Treasuries. Compare CAGR together with volatility and drawdown; a higher return alone does not establish a better fit for a moderate-risk client. The 2022 stock/bond selloff is a useful stress test, while 2020 and 2021 show different market conditions. Gold and REITs can also experience substantial losses, and correlations change over time.

## Data and reproducibility

Source: [Yahoo Finance historical data help](https://help.yahoo.com/kb/sln2311.html). Raw Yahoo chart API responses are retained in `data/`. Run `python backtest.py` to regenerate the CSVs and this report. The CSV contains every monthly adjusted close, asset return, portfolio return, and wealth path. Figures may change if the data provider revises adjusted history.
