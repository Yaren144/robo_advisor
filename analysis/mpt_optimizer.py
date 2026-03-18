import pandas as pd
import numpy as np
from scipy.optimize import minimize
import sys
# arima_forecast dosyasını doğru yoldan import edebilmek için yol ekle
# Not: Bu import, app.py'den çalıştırıldığında sorunsuz çalışır.
sys.path.append('dashboard') 
from analysis.ensemble_forecast import get_robust_forecasts

import warnings
warnings.filterwarnings("ignore") 

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

returns = df[['SPY_return', 'AGG_return']].dropna()
asset_names = returns.columns 

# ============================================
# EXPECTED RETURNS 
# ============================================

# Ensemble tahminlerini yükle

spy_ensemble, agg_ensemble, spy_info, agg_info, spy_arima, agg_arima = get_robust_forecasts()
print(f"\nDEBUG - Ensemble forecasts:")
print(f"SPY ensemble: {spy_ensemble*100:.4f}% daily")
print(f"AGG ensemble: {agg_ensemble*100:.4f}% daily")
print(f"SPY ARIMA: {spy_arima*100:.4f}% daily")
print(f"AGG ARIMA: {agg_arima*100:.4f}% daily")

# Check if forecasts make sense
if spy_ensemble < agg_ensemble:
    print("⚠️  WARNING: SPY forecast lower than AGG - unusual!")


print(f"Using Historical Averages:")
print(f"SPY: {spy_ensemble*100:.4f}% daily ({spy_ensemble*252*100:.1f}% annual)")
print(f"AGG: {agg_ensemble*100:.4f}% daily ({agg_ensemble*252*100:.1f}% annual)")

# Debuging for ARIMA model


# MPT için beklenen getiri (mu), ARIMA tahminleridir.
# [SPY Daily Forecast, AGG Daily Forecast]

cov = returns.cov().values   


mu = np.array([spy_ensemble, agg_ensemble])

# ============================================
# PORTFOLIO FUNCTIONS
# ============================================

def portfolio_return(weights):
    return np.dot(weights, mu)

def portfolio_volatility(weights):
    return np.sqrt(np.dot(weights.T, np.dot(cov, weights)))

def minimize_volatility(weights):
    return portfolio_volatility(weights)


# Debug: Check if constraints are feasible
print("\nDEBUG - Asset characteristics:")
spy_vol = np.sqrt(cov[0,0]) * np.sqrt(252)
agg_vol = np.sqrt(cov[1,1]) * np.sqrt(252)
print(f"SPY volatility: {spy_vol*100:.2f}%")
print(f"AGG volatility: {agg_vol*100:.2f}%")
print(f"SPY return: {mu[0]*252*100:.2f}%")
print(f"AGG return: {mu[1]*252*100:.2f}%")
print()
# ============================================
# OPTIMIZATION FOR THREE RISK PROFILES
# ============================================
RISK_FREE_RATE = 0.0 # Günlük riskten arındırılmış oran
ANNUAL_FACTOR = 252 # Yıllık işlem günü sayısı

# Günlük Hedef Getiri Seviyeleri (MPT'yi sürmeye devam eder)
def get_risk_adjusted_volatility(base_vol, horizon):
    """Adjust max volatility based on horizon"""
    if horizon <= 5:
        return base_vol * 0.8  # Short-term: reduce risk
    elif horizon >= 15:
        return base_vol * 1.3  # Long-term: allow more risk
    else:
        return base_vol  # Medium-term: keep base

profiles = {
    "Conservative": 0.10,   
    "Balanced": 0.15,       
    "Aggressive": 0.21      
}

def negative_return(weights):
    """Negative return for maximization"""
    return -portfolio_return(weights)

results = []

for profile_name, max_vol in profiles.items():
    
    # Set initial guess based on risk level
    if profile_name == "Conservative":
        init_guess = [0.35, 0.65]
    elif profile_name == "Aggressive":
        init_guess = [0.80, 0.20]
    else:  # Balanced
        init_guess = [0.60, 0.40]

    constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'ineq', 'fun': lambda w, mv=max_vol: mv - portfolio_volatility(w) * np.sqrt(ANNUAL_FACTOR)}
        )
        
    bounds = ((0, 1), (0, 1))
        # MAXIMIZE return subject to volatility constraint
    opt = minimize(negative_return, init_guess, bounds=bounds, constraints=constraints)
        
    w = opt.x
        
    ret = portfolio_return(w)
    vol = portfolio_volatility(w)
    ann_ret = ret * ANNUAL_FACTOR
    ann_vol = vol * np.sqrt(ANNUAL_FACTOR)
    sharpe = (ann_ret - (RISK_FREE_RATE * ANNUAL_FACTOR)) / ann_vol if ann_vol > 0 else 0
    
    results.append([
        profile_name,
        w[0],
        w[1],
        ann_ret,
        ann_vol,
        sharpe
    ])

# ============================================
# SAVE RESULTS
# ============================================

result_df = pd.DataFrame(results, columns=[
    "Risk_Profile", 
    "Weight_SPY", 
    "Weight_AGG", 
    "Annual_Return", 
    "Annual_Volatility",
    "Sharpe_Ratio"
])

result_df.to_csv("portfolio_recommendations.csv", index=False)

print("\nPortfolio Optimization Results:")
print(result_df)

