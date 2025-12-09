import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def get_forecasts():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")

    if not os.path.exists(DATA_PATH):
        return 0.0, 0.0

    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)

    spy_series = df["SPY_return"].dropna()
    agg_series = df["AGG_return"].dropna()

    spy_model = ARIMA(spy_series, order=(1,1,1)).fit()
    agg_model = ARIMA(agg_series, order=(1,1,1)).fit()

    spy_forecast = float(spy_model.forecast(steps=1).iloc[0])
    agg_forecast = float(agg_model.forecast(steps=1).iloc[0])

    return spy_forecast, agg_forecast
