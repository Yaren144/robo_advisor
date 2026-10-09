# AI Robo-Advisor

A Python robo-advisor prototype that recommends a stock/bond allocation (SPY / AGG) based on an investor's risk preference, age and investment horizon. It combines exploratory data analysis, Modern Portfolio Theory (MPT) optimization and ARIMA time-series forecasting, with an interactive Streamlit dashboard on top.

## Features

- **Data pipeline:** downloads 5 years of daily SPY and AGG prices (2019–2024) with `yfinance` and derives daily returns, 20-day rolling volatility and 20-day moving averages.
- **Exploratory analysis:** descriptive statistics (including skewness and kurtosis), return distributions, outlier boxplots, correlation heatmap, rolling volatility and momentum charts.
- **MPT optimizer:** uses `scipy.optimize` to find the minimum-volatility SPY/AGG weights for three target-return profiles: Conservative, Balanced and Aggressive.
- **ARIMA forecasting:** fits ARIMA(1,1,1) models with `statsmodels` to forecast the next-period return of each asset.
- **Streamlit dashboard:** collects the investor profile, builds an allocation adjusted for horizon and age, and shows the risk level, the reasoning behind the strategy and the expected return.

## Tech Stack

Python · pandas · NumPy · SciPy · statsmodels · yfinance · Matplotlib · Seaborn · Streamlit

## Project Structure

```
robo_advisor/
├── data/
│   ├── data_loader.py              # Download prices, engineer features
│   ├── processed_data.csv          # Prepared dataset (1,238 trading days)
│   └── descriptive_stats.csv       # Output of the EDA step
├── analysis/
│   ├── explore_data.py             # EDA and visualizations
│   ├── mpt_optimizer.py            # Minimum-volatility portfolio optimization
│   ├── portfolio_recommendations.csv
│   ├── validation.py               # Buy-and-hold benchmark
│   └── backtest.py
└── dashboard/
    ├── app.py                      # Streamlit app
    └── arima_forecast.py           # ARIMA return forecasts
```

## Getting Started

```bash
git clone https://github.com/Yaren144/robo_advisor.git
cd robo_advisor
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py

# Run the analysis scripts (from the project root)
python analysis/explore_data.py
python analysis/mpt_optimizer.py
```

`data/processed_data.csv` is included, so the analysis runs without downloading data. To refresh it, run `python data/data_loader.py`.

## Sample Results (MPT optimizer)

| Risk profile | SPY weight | AGG weight | Daily volatility |
|---|---|---|---|
| Conservative | 44% | 56% | 0.67% |
| Balanced | 97% | 3% | 1.28% |
| Aggressive | 100% | 0% | 1.32% |

The Aggressive profile reaches the upper bound: its 0.10% daily return target is higher than the best return available from SPY alone (~0.062%/day), so the optimizer puts the entire portfolio in SPY.

## Limitations and Next Steps

This is a learning project, and the dashboard and analysis modules are not fully connected yet:

- The dashboard uses fixed example forecast values. `arima_forecast.get_forecasts()` is implemented, but the app does not call it yet.
- The dashboard's allocation is rule-based (risk profile, adjusted for horizon and age). It does not use the MPT optimizer's output yet.
- The planned next steps are to connect both modules to the dashboard, add a proper backtest against a buy-and-hold benchmark, and expand the asset universe.

> **Disclaimer:** This project is for educational purposes only and is not financial advice.
