import pandas as pd
import numpy as np
from analysis.arima_optimizer import get_forecasts_optimized

def get_ensemble_forecast(returns_series, arima_weight=0.3):
    """
    Ensemble forecast: Blend ARIMA + Historical Average
    
    Parameters:
    -----------
    returns_series : pd.Series
        Historical returns (e.g., df['SPY_return'])
    arima_weight : float
        Weight for ARIMA (0.3 = 30% ARIMA, 70% historical)
        Lower = more conservative, Higher = more tactical
    
    Returns:
    --------
    ensemble_forecast : float
        Blended daily return forecast
    arima_forecast : float
        Raw ARIMA forecast (for transparency)
    historical_avg : float
        Historical average (for transparency)
    """
    
    # Get ARIMA forecast
    arima_forecast = returns_series.iloc[-1]  # Placeholder, will use actual ARIMA
    
    # Get historical average
    historical_avg = returns_series.mean()
    
    # Blend with weights
    ensemble_forecast = (arima_weight * arima_forecast) + ((1 - arima_weight) * historical_avg)
    
    return ensemble_forecast, arima_forecast, historical_avg


def get_robust_forecasts():
    """
    Get ensemble forecasts for SPY and AGG
    Uses 30% ARIMA + 70% Historical (configurable)
    """
    import os
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
    
    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    
    spy_series = df["SPY_return"].dropna()
    agg_series = df["AGG_return"].dropna()
    
    # Get ARIMA forecasts
    spy_arima, agg_arima, spy_info, agg_info = get_forecasts_optimized()
    
    # Get historical averages
    # spy_historical = spy_series.mean()
    # agg_historical = agg_series.mean()

    spy_historical = 0.10 / 252  # 10% annual expected return
    agg_historical = 0.05 / 252  # 5% annual expected return

    print(f"Using long-term market expectations for MPT:")
    print(f"  SPY: 10% annual expected return")
    print(f"  AGG: 5% annual expected return")
    
    # Blend with 30% ARIMA, 70% Historical
    ARIMA_WEIGHT = 0.0  # Adjust this (0.0 = pure historical, 1.0 = pure ARIMA)
    
    spy_ensemble = (ARIMA_WEIGHT * spy_arima) + ((1 - ARIMA_WEIGHT) * spy_historical)
    agg_ensemble = (ARIMA_WEIGHT * agg_arima) + ((1 - ARIMA_WEIGHT) * agg_historical)
    
    # Cap extreme forecasts (safety bounds)
    spy_ensemble = max(min(spy_ensemble, 0.003), -0.001)  # Cap at ±0.3%/0.1% daily
    agg_ensemble = max(min(agg_ensemble, 0.002), -0.0005) # Cap at ±0.2%/0.05% daily
    
    print("\n" + "="*70)
    print("📊 ENSEMBLE FORECAST BREAKDOWN")
    print("="*70)
    print(f"\nSPY:")
    print(f"  ARIMA Forecast:      {spy_arima*100:>7.3f}% daily ({spy_arima*252*100:>6.1f}% annual)")
    print(f"  Historical Average:  {spy_historical*100:>7.3f}% daily ({spy_historical*252*100:>6.1f}% annual)")
    print(f"  Ensemble (30/70):    {spy_ensemble*100:>7.3f}% daily ({spy_ensemble*252*100:>6.1f}% annual)")
    
    print(f"\nAGG:")
    print(f"  ARIMA Forecast:      {agg_arima*100:>7.3f}% daily ({agg_arima*252*100:>6.1f}% annual)")
    print(f"  Historical Average:  {agg_historical*100:>7.3f}% daily ({agg_historical*252*100:>6.1f}% annual)")
    print(f"  Ensemble (30/70):    {agg_ensemble*100:>7.3f}% daily ({agg_ensemble*252*100:>6.1f}% annual)")
    print("="*70 + "\n")
    
    return spy_ensemble, agg_ensemble, spy_info, agg_info, spy_arima, agg_arima