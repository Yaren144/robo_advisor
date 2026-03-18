import pandas as pd
import numpy as np

from analysis.metrics import calculate_comprehensive_metrics, print_metrics_report

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# generate signal and position (lagged)
df['signal_spy'] = (df['SPY_price'] > df['SPY_ma20']).astype(int)
df['position_spy'] = df['signal_spy'].shift(1).fillna(0)

# strategy returns (with optional transaction cost)
trade = df['position_spy'].diff().abs()  # 1 when trade occurs
tc = 0.0005  # 0.05% per trade example
df['strat_ret_spy'] = df['position_spy'] * df['SPY_return'] - trade * tc

# cumulative return
df['strat_cum'] = (1 + df['strat_ret_spy']).cumprod()

# Sharpe ratio (annualized)
ann_return = df['strat_ret_spy'].mean() * 252
ann_vol = df['strat_ret_spy'].std() * np.sqrt(252)
sharpe = ann_return / ann_vol

# max drawdown
cum = (1 + df['strat_ret_spy']).cumprod()
rolling_max = cum.cummax()
drawdown = (cum - rolling_max) / rolling_max
max_dd = drawdown.min()


metrics = calculate_comprehensive_metrics(
    strategy_returns=df['strat_ret_spy'],
    benchmark_returns=df['SPY_return']  # Compare against buy-and-hold SPY
)

print_metrics_report(metrics)


# After your existing code, add:
print("\n" + "="*60)
print("BACKTEST RESULTS SUMMARY")
print("="*60)

# Annual return
ann_return = df['strat_ret_spy'].mean() * 252
print(f"Annual Return: {ann_return*100:.2f}%")

# Sharpe (you have this)
print(f"Sharpe Ratio: {sharpe:.2f}")

# Max Drawdown (you have this)
print(f"Max Drawdown: {max_dd*100:.2f}%")

# Win Rate
win_rate = (df['strat_ret_spy'] > 0).sum() / len(df['strat_ret_spy'])
print(f"Win Rate: {win_rate*100:.1f}%")

# Total Return
total_return = (df['strat_cum'].iloc[-1] - 1) * 100
print(f"Total Return: {total_return:.1f}%")

print("="*60)

# Save for later use in Streamlit
import json
with open('data/backtest_metrics.json', 'w') as f:
    # Convert numpy types to regular Python types for JSON
    metrics_serializable = {k: float(v) for k, v in metrics.items()}
    json.dump(metrics_serializable, f, indent=2)