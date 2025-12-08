import pandas as pd
import numpy as np
from scipy.optimize import minimize

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv("data/processed_data.csv", index_col=0, parse_dates=True)

returns = df[['SPY_return', 'AGG_return']].dropna()

# ============================================
# EXPECTED RETURNS (from ARIMA or historical mean)
# --------------------------------------------
# For now: use simple mean as proxy
# Later you can manually insert ARIMA forecast values
# ============================================

mu = returns.mean().values   # [SPY_mean, AGG_mean]
cov = returns.cov().values   # covariance matrix

# ============================================
# PORTFOLIO FUNCTIONS
# ============================================

def portfolio_return(weights):
    return np.dot(weights, mu)

def portfolio_volatility(weights):
    return np.sqrt(np.dot(weights.T, np.dot(cov, weights)))

# Minimize volatility for a given target return
def minimize_volatility(weights):
    return portfolio_volatility(weights)

# ============================================
# OPTIMIZATION FOR THREE RISK PROFILES
# ============================================

profiles = {
    "Conservative": 0.0003,
    "Balanced":     0.0006,
    "Aggressive":   0.0010
}

results = []

for name, target in profiles.items():

    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},             # weights sum to 1
        {'type': 'eq', 'fun': lambda w: portfolio_return(w) - target}
    )

    bounds = ((0,1), (0,1))
    init_guess = [0.5, 0.5]

    opt = minimize(minimize_volatility, init_guess, bounds=bounds, constraints=constraints)

    w = opt.x
    ret = portfolio_return(w)
    vol = portfolio_volatility(w)

    results.append([name, w[0], w[1], ret, vol])

# ============================================
# SAVE RESULTS
# ============================================

result_df = pd.DataFrame(results, columns=[
    "Risk_Profile", "Weight_SPY", "Weight_AGG", "Expected_Return", "Volatility"
])

result_df.to_csv("portfolio_recommendations.csv", index=False)

print("\nPortfolio Optimization Results:")
print(result_df)
