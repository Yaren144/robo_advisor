
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

# make sure index is datetime
df.index = pd.to_datetime(df.index)

# force business day frequency (stock market data)
df = df.asfreq('B')  # B = business day

# use SPY returns
series = df['SPY_return'].dropna()


model = ARIMA(series, order=(1,0,1))
model_fit = model.fit()


forecast = model_fit.forecast(steps=1)
predicted_return = forecast.iloc[0]

print("Next-day expected return (SPY):", predicted_return)


