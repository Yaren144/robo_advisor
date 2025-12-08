import pandas as pd
import numpy as np

# Load backtest equity curve
df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# Calculate buy-and-hold benchmark
df['buy_hold_spy'] = (1 + df['SPY_return']).cumprod()

# Load strategy if exists
try:
    strat = pd.read_csv("analysis/backtest_results.csv")
except:
    strat = None

print("\nFinal Buy & Hold Return:")
print(df['buy_hold_spy'].iloc[-1])

if strat is not None:
    print("\nStrategy Results:")
    print(strat)
