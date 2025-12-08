import pandas as pd
import numpy as np

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
