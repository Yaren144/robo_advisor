import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import itertools
import warnings
warnings.filterwarnings('ignore')

def test_stationarity(series):
    """
    Test if time series is stationary using Augmented Dickey-Fuller test
    
    Returns:
    --------
    bool : True if stationary (p-value < 0.05)
    float : p-value from ADF test
    """
    result = adfuller(series.dropna())
    p_value = result[1]
    is_stationary = p_value < 0.05
    return is_stationary, p_value


def auto_select_arima(series, max_p=3, max_d=2, max_q=3, seasonal=False):
    """
    Automatically select best ARIMA parameters using AIC criterion
    
    Parameters:
    -----------
    series : pd.Series
        Time series data (returns)
    max_p : int
        Maximum AR order to test
    max_d : int
        Maximum differencing order to test
    max_q : int
        Maximum MA order to test
    seasonal : bool
        Whether to include seasonal component (set False for daily financial data)
    
    Returns:
    --------
    best_model : ARIMA model object (fitted)
    best_order : tuple (p, d, q)
    best_aic : float
    search_results : pd.DataFrame with all tested models
    """
    
    # Test stationarity to guide d parameter
    is_stationary, p_value = test_stationarity(series)
    
    # If already stationary, focus on d=0, otherwise try d=1,2
    if is_stationary:
        d_range = [0]
    else:
        d_range = range(1, max_d + 1)
    
    # Store results
    results = []
    best_aic = np.inf
    best_order = None
    best_model = None
    
    print(f"🔍 Searching for best ARIMA parameters...")
    print(f"   Series length: {len(series)}")
    print(f"   Stationary: {'Yes' if is_stationary else 'No'} (p-value: {p_value:.4f})")
    print(f"   Testing combinations: p∈[0,{max_p}], d∈{list(d_range)}, q∈[0,{max_q}]")
    print()
    
    # Grid search
    tested = 0
    for p in range(max_p + 1):
        for d in d_range:
            for q in range(max_q + 1):
                # Skip (0,0,0) - invalid model
                if p == 0 and q == 0:
                    continue
                
                try:
                    model = ARIMA(series, order=(p, d, q))
                    fitted = model.fit()
                    
                    aic = fitted.aic
                    bic = fitted.bic
                    
                    results.append({
                        'order': (p, d, q),
                        'aic': aic,
                        'bic': bic,
                        'converged': True
                    })
                    
                    if aic < best_aic:
                        best_aic = aic
                        best_order = (p, d, q)
                        best_model = fitted
                        print(f"   ✓ New best: ARIMA{(p,d,q)} - AIC: {aic:.2f}")
                    
                    tested += 1
                    
                except Exception as e:
                    results.append({
                        'order': (p, d, q),
                        'aic': np.nan,
                        'bic': np.nan,
                        'converged': False
                    })
                    continue
    
    print(f"\n✅ Tested {tested} models")
    print(f"🏆 Best model: ARIMA{best_order} with AIC={best_aic:.2f}")
    
    # Create results DataFrame
    search_results = pd.DataFrame(results)
    search_results = search_results.sort_values('aic').reset_index(drop=True)
    
    return best_model, best_order, best_aic, search_results


def get_forecasts_optimized():
    """
    Enhanced version of your get_forecasts() function with auto-ARIMA
    
    Returns:
    --------
    spy_forecast : float
    agg_forecast : float
    spy_model_info : dict (model diagnostics)
    agg_model_info : dict (model diagnostics)
    """
    import os
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
    
    if not os.path.exists(DATA_PATH):
        return 0.0, 0.0, {}, {}
    
    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    
    spy_series = df["SPY_return"].dropna()
    agg_series = df["AGG_return"].dropna()
    
    print("\n" + "="*70)
    print("📊 SPY MODEL OPTIMIZATION")
    print("="*70)
    spy_model, spy_order, spy_aic, spy_results = auto_select_arima(spy_series, max_p=3, max_d=2, max_q=3)
    
    print("\n" + "="*70)
    print("📊 AGG MODEL OPTIMIZATION")
    print("="*70)
    agg_model, agg_order, agg_aic, agg_results = auto_select_arima(agg_series, max_p=3, max_d=2, max_q=3)
    
    # Generate forecasts
    spy_forecast = float(spy_model.forecast(steps=1).iloc[0])
    agg_forecast = float(agg_model.forecast(steps=1).iloc[0])
    
    print("\n" + "="*70)
    print("🔮 FORECASTS")
    print("="*70)
    print(f"SPY Expected Return: {spy_forecast*100:>6.3f}% (Model: ARIMA{spy_order})")
    print(f"AGG Expected Return: {agg_forecast*100:>6.3f}% (Model: ARIMA{agg_order})")
    print("="*70 + "\n")
    
    # Package model info for dashboard
    spy_model_info = {
        'order': spy_order,
        'aic': spy_aic,
        'forecast': spy_forecast,
        'top_3_models': spy_results.head(3).to_dict('records')
    }
    
    agg_model_info = {
        'order': agg_order,
        'aic': agg_aic,
        'forecast': agg_forecast,
        'top_3_models': agg_results.head(3).to_dict('records')
    }
    
    # Save for dashboard
    import json
    model_info = {
        'spy': spy_model_info,
        'agg': agg_model_info
    }
    
    output_path = os.path.join(BASE_DIR, "data", "arima_model_info.json")
    with open(output_path, 'w') as f:
        # Convert any numpy types to native Python types
        def convert_types(obj):
            if isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(convert_types(item) for item in obj)
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif pd.isna(obj):
                return None
            else:
                return obj
        
        model_info_serializable = convert_types(model_info)
        json.dump(model_info_serializable, f, indent=2)
    
    return spy_forecast, agg_forecast, spy_model_info, agg_model_info


# Backward compatibility: simple function that returns just forecasts
def get_forecasts():
    """
    Drop-in replacement for your original get_forecasts() function
    """
    spy_forecast, agg_forecast, _, _ = get_forecasts_optimized()
    return spy_forecast, agg_forecast