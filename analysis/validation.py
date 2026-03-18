import pandas as pd
import numpy as np

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# Your strategy (from backtesting)
df['signal_spy'] = (df['SPY_price'] > df['SPY_ma20']).astype(int)
df['position_spy'] = df['signal_spy'].shift(1).fillna(0)
trade = df['position_spy'].diff().abs()
tc = 0.0005
df['strat_ret_spy'] = df['position_spy'] * df['SPY_return'] - trade * tc
df['strat_cum'] = (1 + df['strat_ret_spy']).cumprod()

# Buy & Hold benchmark
df['buy_hold_cum'] = (1 + df['SPY_return']).cumprod()

print("\n" + "="*70)
print("VALIDATION: STRATEGY vs BENCHMARK")
print("="*70)

# Strategy metrics
strat_total = (df['strat_cum'].iloc[-1] - 1) * 100
strat_annual = df['strat_ret_spy'].mean() * 252 * 100
strat_vol = df['strat_ret_spy'].std() * np.sqrt(252) * 100
strat_sharpe = (df['strat_ret_spy'].mean() * 252 - 0.02) / (df['strat_ret_spy'].std() * np.sqrt(252))

# Benchmark metrics
bench_total = (df['buy_hold_cum'].iloc[-1] - 1) * 100
bench_annual = df['SPY_return'].mean() * 252 * 100
bench_vol = df['SPY_return'].std() * np.sqrt(252) * 100
bench_sharpe = (df['SPY_return'].mean() * 252 - 0.02) / (df['SPY_return'].std() * np.sqrt(252))

print(f"\nSTRATEGY PERFORMANCE:")
print(f"  Total Return:    {strat_total:>6.1f}%")
print(f"  Annual Return:   {strat_annual:>6.2f}%")
print(f"  Annual Volatility: {strat_vol:>6.2f}%")
print(f"  Sharpe Ratio:    {strat_sharpe:>6.2f}")

print(f"\nBUY & HOLD SPY:")
print(f"  Total Return:    {bench_total:>6.1f}%")
print(f"  Annual Return:   {bench_annual:>6.2f}%")
print(f"  Annual Volatility: {bench_vol:>6.2f}%")
print(f"  Sharpe Ratio:    {bench_sharpe:>6.2f}")

print(f"\nCOMPARISON:")
print(f"  Return Difference:   {strat_annual - bench_annual:>6.2f}% (Strategy - Benchmark)")
print(f"  Volatility Reduction: {bench_vol - strat_vol:>6.2f}% (Lower is better)")
print(f"  Sharpe Improvement:  {strat_sharpe - bench_sharpe:>+6.2f}")

if strat_sharpe > bench_sharpe:
    print("\n✅ Strategy has BETTER risk-adjusted returns!")
else:
    print("\n⚠️ Strategy underperforms on risk-adjusted basis")

print("="*70)