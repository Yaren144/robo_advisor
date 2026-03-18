# AI-Powered Robo-Advisor for Personalized ETF Investing

A fintech application that solves the beginner investor's trust problem — strategies are backtested on real historical data, AI-powered but fully transparent, with professional-grade portfolio optimization.

> Built for FIN4XX · Zeynep Yaren Deveci

---

## Problem & Motivation

Beginner investors face three core challenges:
- Online strategies look attractive but rarely come with real proof
- Testing ideas requires risking real money
- The result: confusion, fear, and loss of motivation

This robo-advisor addresses all three by backtesting every strategy on historical data and explaining every recommendation in plain terms.

---

## Features

- **Personalized portfolio recommendations** based on risk profile, investment horizon, and initial capital
- **ARIMA forecasting** with Auto-ARIMA (AIC optimization) for next-day return prediction
- **Momentum backtesting** with transaction cost modeling (0.05%) and performance metrics
- **Modern Portfolio Theory (MPT)** optimization across three risk profiles: Conservative, Balanced, Aggressive
- **Walk-forward validation** for out-of-sample robustness testing
- **Interactive Dash dashboard** for visual exploration of results

---

## System Architecture

```
Data Collection & Preprocessing
        ↓
Feature Engineering (volatility, moving averages)
        ↓
AI Forecasting (ARIMA / Ensemble)
        ↓
Portfolio Optimization (MPT)
        ↓
Interactive Dashboard (Dash)
```

---

## Assets Covered

| ETF | Represents | Profile |
|-----|-----------|---------|
| **SPY** | S&P 500 — 500 largest U.S. companies | Growth · High return · High risk |
| **AGG** | U.S. Aggregate Bond Market | Stability · Low return · Low risk |

SPY and AGG are negatively correlated — together they form a simple, diversified portfolio ideal for beginner investors and widely used in real-world robo-advisors.

---

## Methodology

### ARIMA Forecasting
Auto-ARIMA selects optimal parameters via AIC score (best model for SPY: `ARIMA(3,0,2)`). Pipeline: stationarity test (ADF) → grid search (p=0–3, d=0–2, q=0–3) → forecast generation.

### Backtesting — Momentum Strategy
Buy when price is above 20-day moving average, shift to bonds when below. Validated against buy-and-hold SPY benchmark.

| Metric | Momentum Strategy | SPY Buy & Hold |
|--------|------------------|---------------|
| Annual Return | 11.67% | ~15% |
| Sharpe Ratio | 0.98 | 0.82 |
| Max Drawdown | -19% | -30% |

**Key takeaway:** Lower returns, significantly lower risk — better risk-adjusted performance for risk-averse investors.

### Portfolio Optimization (MPT)
Three profiles optimized via MPT with horizon adjustment (±10% equity allocation):

- **Conservative** — more bonds, short horizon (<5 years)
- **Balanced** — equal weighting, medium horizon
- **Aggressive** — more equities, long horizon (>15 years)

---

## Project Structure

```
robo_advisor/
├── analysis/
│   ├── backtest.py               # Momentum strategy backtesting
│   ├── mpt_optimizer.py          # Modern Portfolio Theory optimization
│   ├── arima_optimizer.py        # Auto-ARIMA parameter selection
│   ├── ensemble_forecast.py      # Ensemble forecasting model
│   ├── walk_forward_backtest.py  # Walk-forward validation
│   ├── metrics.py                # Performance metrics (Sharpe, drawdown)
│   └── validation.py             # Model validation utilities
├── dashboard/
│   └── app.py                    # Dash interactive dashboard
├── data/
│   ├── arima_model_info.json
│   ├── backtest_metrics.json
│   └── walk_forward_metrics.json
└── README.md
```

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Yaren144/robo_advisor.git
cd robo_advisor

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python dashboard/app.py
```

Then open `http://localhost:8050` in your browser.

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.12 |
| Data | yfinance, pandas, numpy |
| Forecasting | statsmodels (ARIMA), pmdarima |
| Optimization | scipy |
| Dashboard | Plotly Dash |
| Backtesting | Custom implementation |

---

## Branches

| Branch | Description |
|--------|-------------|
| `master` | Original implementation — "purple final design" |
| `analysis-rework` | Refactored analysis pipeline with ensemble forecasting, walk-forward backtesting, and improved metrics |

---

## Future Enhancements

- Multi-asset expansion (international ETFs, commodities)
- Advanced transaction cost and tax-loss harvesting modeling
- Live data integration for real-time recommendations

---

## Author

**Zeynep Yaren Deveci** · [GitHub](https://github.com/Yaren144)
