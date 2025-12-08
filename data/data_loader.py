import yfinance as yf
import pandas as pd

def load_price_data(tickers):
    raw = yf.download(
        tickers,
        start="2019-01-01",
        end="2024-01-01",
        auto_adjust=True
    )

    prices = raw["Close"].dropna().copy()

    # Derived features
    returns = prices.pct_change()
    volatility = returns.rolling(window=20).std()
    momentum = prices.rolling(window=20).mean()

    df = pd.concat([
        prices.add_suffix("_price"),
        returns.add_suffix("_return"),
        volatility.add_suffix("_vol"),
        momentum.add_suffix("_ma20")
    ], axis=1).dropna()

    return df

if __name__ == "__main__":
    tickers = ["SPY", "AGG"]
    df = load_price_data(tickers)
    df.to_csv("processed_data.csv")
    print("Dataset saved as processed_data.csv")
