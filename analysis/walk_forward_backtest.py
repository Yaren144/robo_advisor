import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

def walk_forward_backtest(df, train_window=252, refit_frequency=20, 
                          transaction_cost=0.0005, verbose=True):
    """
    Walk-forward backtesting: train on rolling window, predict future, evaluate
    
    Parameters:
    -----------
    df : pd.DataFrame
        Your processed_data.csv loaded as DataFrame
    train_window : int
        Number of days to use for training (252 = 1 year)
    refit_frequency : int
        Retrain model every N days (20 = monthly for trading days)
    transaction_cost : float
        Cost per trade (0.0005 = 0.05%)
    verbose : bool
        Print progress updates
    
    Returns:
    --------
    results_df : pd.DataFrame with predictions, actuals, and trades
    metrics : dict with performance metrics
    """
    
    returns = df['SPY_return'].dropna()
    prices = df['SPY_price'].dropna()
    
    # Storage for results
    predictions = []
    actuals = []
    dates = []
    positions = []
    
    if verbose:
        print("\n" + "="*70)
        print("🔄 WALK-FORWARD BACKTESTING")
        print("="*70)
        print(f"Train window: {train_window} days (~{train_window/252:.1f} years)")
        print(f"Refit frequency: {refit_frequency} days")
        print(f"Test period: {len(returns) - train_window} days")
        print(f"Expected retrains: {(len(returns) - train_window) // refit_frequency}")
        print("="*70 + "\n")
    
    # Walk forward through time
    last_model = None
    last_order = None
    retrains = 0
    
    for i in range(train_window, len(returns), refit_frequency):
        # Only use data UP TO this point (no future information!)
        train_data = returns[i - train_window:i]
        
        # Retrain ARIMA model
        try:
            # Use simple (1,1,1) for speed, or implement auto-selection here
            model = ARIMA(train_data, order=(1, 1, 1))
            fitted_model = model.fit()
            last_model = fitted_model
            last_order = (1, 1, 1)
            retrains += 1
            
            if verbose and retrains % 5 == 0:
                print(f"   Retrain #{retrains}: {returns.index[i].date()} - Train: {returns.index[i-train_window].date()} to {returns.index[i-1].date()}")
        
        except Exception as e:
            if verbose:
                print(f"   ⚠️  Model fit failed at {returns.index[i].date()}, using last model")
            if last_model is None:
                continue
        
        # Make predictions for next refit_frequency days
        forecast_horizon = min(refit_frequency, len(returns) - i)
        
        try:
            forecast = last_model.forecast(steps=forecast_horizon)
            
            # For each forecasted day
            for j in range(forecast_horizon):
                if i + j >= len(returns):
                    break
                
                pred_return = float(forecast.iloc[j])
                actual_return = returns.iloc[i + j]
                pred_date = returns.index[i + j]
                
                # Trading signal: Long if predicted return > 0
                position = 1 if pred_return > 0 else 0
                
                predictions.append(pred_return)
                actuals.append(actual_return)
                dates.append(pred_date)
                positions.append(position)
        
        except Exception as e:
            if verbose:
                print(f"   ⚠️  Forecast failed at {returns.index[i].date()}")
            continue
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'date': dates,
        'predicted_return': predictions,
        'actual_return': actuals,
        'position': positions
    })
    results_df.set_index('date', inplace=True)
    
    # Calculate strategy returns
    results_df['strategy_return'] = results_df['position'] * results_df['actual_return']
    
    # Transaction costs
    results_df['trade'] = results_df['position'].diff().abs().fillna(0)
    results_df['strategy_return_net'] = results_df['strategy_return'] - results_df['trade'] * transaction_cost
    
    # Cumulative returns
    results_df['strategy_cumulative'] = (1 + results_df['strategy_return_net']).cumprod()
    results_df['buyhold_cumulative'] = (1 + results_df['actual_return']).cumprod()
    
    # Calculate metrics
    from metrics import calculate_comprehensive_metrics
    
    strategy_metrics = calculate_comprehensive_metrics(
        results_df['strategy_return_net'],
        results_df['actual_return']
    )
    
    # Add forecast-specific metrics
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    
    mae = mean_absolute_error(results_df['actual_return'], results_df['predicted_return'])
    rmse = np.sqrt(mean_squared_error(results_df['actual_return'], results_df['predicted_return']))
    
    # Direction accuracy
    direction_correct = ((results_df['predicted_return'] > 0) == (results_df['actual_return'] > 0)).sum()
    direction_accuracy = direction_correct / len(results_df)
    
    strategy_metrics['forecast_mae'] = mae
    strategy_metrics['forecast_rmse'] = rmse
    strategy_metrics['direction_accuracy'] = direction_accuracy
    strategy_metrics['number_of_retrains'] = retrains
    strategy_metrics['number_of_trades'] = results_df['trade'].sum()
    
    if verbose:
        print("\n" + "="*70)
        print("📊 WALK-FORWARD BACKTEST RESULTS")
        print("="*70)
        print(f"Total days tested: {len(results_df)}")
        print(f"Number of retrains: {retrains}")
        print(f"Number of trades: {int(results_df['trade'].sum())}")
        print(f"\n🎯 Forecast Accuracy:")
        print(f"  Direction Accuracy: {direction_accuracy*100:.2f}%")
        print(f"  MAE: {mae:.6f}")
        print(f"  RMSE: {rmse:.6f}")
        print(f"\n📈 Strategy Performance:")
        print(f"  Annual Return: {strategy_metrics['annual_return']*100:.2f}%")
        print(f"  Sharpe Ratio: {strategy_metrics['sharpe_ratio']:.3f}")
        print(f"  Max Drawdown: {strategy_metrics['max_drawdown']*100:.2f}%")
        print(f"  Win Rate: {strategy_metrics['win_rate']*100:.2f}%")
        print(f"\n📊 vs Buy & Hold:")
        buyhold_return = (results_df['buyhold_cumulative'].iloc[-1] - 1) * 100
        strategy_return = (results_df['strategy_cumulative'].iloc[-1] - 1) * 100
        print(f"  Strategy: {strategy_return:.2f}%")
        print(f"  Buy & Hold: {buyhold_return:.2f}%")
        print(f"  Outperformance: {strategy_return - buyhold_return:+.2f}%")
        print("="*70 + "\n")
    
    return results_df, strategy_metrics


def run_walk_forward_analysis():
    """
    Complete walk-forward analysis workflow
    Save results for dashboard
    """
    import os
    import json
    
    # Load data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
    
    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    
    # Run walk-forward backtest
    results_df, metrics = walk_forward_backtest(df, verbose=True)
    
    # Save results
    OUTPUT_DIR = os.path.join(BASE_DIR, "data")
    results_df.to_csv(os.path.join(OUTPUT_DIR, "walk_forward_results.csv"))
    
    # Save metrics (convert numpy types)
    metrics_serializable = {k: float(v) if not isinstance(v, (str, bool)) else v 
                           for k, v in metrics.items()}
    
    with open(os.path.join(OUTPUT_DIR, "walk_forward_metrics.json"), 'w') as f:
        json.dump(metrics_serializable, f, indent=2)
    
    print(f"✅ Results saved to {OUTPUT_DIR}/")
    print(f"   - walk_forward_results.csv")
    print(f"   - walk_forward_metrics.json")
    
    return results_df, metrics


if __name__ == "__main__":
    run_walk_forward_analysis()