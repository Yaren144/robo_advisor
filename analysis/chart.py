# Quick code to generate chart
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# Normalize to 100
spy_norm = (df['SPY_price'] / df['SPY_price'].iloc[0]) * 100
agg_norm = (df['AGG_price'] / df['AGG_price'].iloc[0]) * 100

plt.figure(figsize=(10, 6))
plt.plot(spy_norm, label='SPY (Stocks)', linewidth=2, color='#4A90E2')
plt.plot(agg_norm, label='AGG (Bonds)', linewidth=2, color='#50C878')
plt.axvline(pd.Timestamp('2020-03-01'), color='red', linestyle='--', alpha=0.5, label='COVID Crash')
plt.title('Cumulative Performance: SPY vs AGG (2019-2024)', fontsize=14, fontweight='bold')
plt.ylabel('Value ($100 Initial Investment)', fontsize=12)
plt.xlabel('Date', fontsize=12)
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('spy_agg_comparison.png', dpi=300)

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# Calculate cumulative returns
df['spy_cumulative'] = (1 + df['SPY_return']).cumprod()

plt.figure(figsize=(10, 5))
plt.plot(df.index, df['spy_cumulative'], label='SPY Buy & Hold', linewidth=2)
plt.title('SPY Performance (Benchmark)')
plt.ylabel('Growth of $1')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('benchmark.png', dpi=300)