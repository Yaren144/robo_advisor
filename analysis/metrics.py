import pandas as pd
import numpy as np

def calculate_comprehensive_metrics(strategy_returns, benchmark_returns=None, risk_free_rate=0.02):
    """
    Calculate professional-grade performance metrics for backtesting
    
    Parameters:
    -----------
    strategy_returns : pd.Series
        Daily returns of your strategy (e.g., df['strat_ret_spy'])
    benchmark_returns : pd.Series, optional
        Daily returns of benchmark (e.g., df['SPY_return'])
    risk_free_rate : float
        Annual risk-free rate (default 2% = 0.02)
    
    Returns:
    --------
    dict : All performance metrics
    """
    
    # Convert annual risk-free rate to daily
    rf_daily = risk_free_rate / 252
    
    # 1. Annualized Return
    annual_return = strategy_returns.mean() * 252
    
    # 2. Annualized Volatility
    annual_vol = strategy_returns.std() * np.sqrt(252)
    
    # 3. Sharpe Ratio (you already have this)
    sharpe_ratio = (annual_return - risk_free_rate) / annual_vol if annual_vol != 0 else 0
    
    # 4. Sortino Ratio (only penalizes downside volatility)
    downside_returns = strategy_returns[strategy_returns < rf_daily]
    downside_std = downside_returns.std() * np.sqrt(252)
    sortino_ratio = (annual_return - risk_free_rate) / downside_std if downside_std != 0 else 0
    
    # 5. Maximum Drawdown
    cumulative = (1 + strategy_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # 6. Calmar Ratio (return / max drawdown)
    calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # 7. Win Rate
    win_rate = (strategy_returns > 0).sum() / len(strategy_returns)
    
    # 8. Average Win / Average Loss Ratio
    wins = strategy_returns[strategy_returns > 0]
    losses = strategy_returns[strategy_returns < 0]
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = abs(losses.mean()) if len(losses) > 0 else 0
    win_loss_ratio = avg_win / avg_loss if avg_loss != 0 else 0
    
    # 9. Total Cumulative Return
    total_return = (1 + strategy_returns).prod() - 1
    
    metrics = {
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'max_drawdown': max_drawdown,
        'calmar_ratio': calmar_ratio,
        'win_rate': win_rate,
        'win_loss_ratio': win_loss_ratio,
        'total_return': total_return
    }
    
    # 10. Alpha & Beta (if benchmark provided)
    if benchmark_returns is not None and len(benchmark_returns) == len(strategy_returns):
        # Align indices
        aligned = pd.DataFrame({
            'strategy': strategy_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned) > 0:
            # Beta (sensitivity to market)
            covariance = aligned.cov().loc['strategy', 'benchmark']
            benchmark_variance = aligned['benchmark'].var()
            beta = covariance / benchmark_variance if benchmark_variance != 0 else 0
            
            # Alpha (excess return over expected)
            benchmark_annual_return = aligned['benchmark'].mean() * 252
            expected_return = risk_free_rate + beta * (benchmark_annual_return - risk_free_rate)
            alpha = annual_return - expected_return
            
            metrics['alpha'] = alpha
            metrics['beta'] = beta
    
    return metrics


def print_metrics_report(metrics):
    """
    Print formatted metrics report for console output
    """
    print("\n" + "="*60)
    print("STRATEGY PERFORMANCE METRICS")
    print("="*60)
    
    print(f"\n📊 Returns & Risk:")
    print(f"  Annual Return:        {metrics['annual_return']*100:>8.2f}%")
    print(f"  Annual Volatility:    {metrics['annual_volatility']*100:>8.2f}%")
    print(f"  Total Return:         {metrics['total_return']*100:>8.2f}%")
    
    print(f"\n📈 Risk-Adjusted Performance:")
    print(f"  Sharpe Ratio:         {metrics['sharpe_ratio']:>8.3f}")
    print(f"  Sortino Ratio:        {metrics['sortino_ratio']:>8.3f}")
    print(f"  Calmar Ratio:         {metrics['calmar_ratio']:>8.3f}")
    
    print(f"\n📉 Drawdown Analysis:")
    print(f"  Maximum Drawdown:     {metrics['max_drawdown']*100:>8.2f}%")
    
    print(f"\n🎯 Win/Loss Statistics:")
    print(f"  Win Rate:             {metrics['win_rate']*100:>8.2f}%")
    print(f"  Win/Loss Ratio:       {metrics['win_loss_ratio']:>8.3f}")
    
    if 'alpha' in metrics and 'beta' in metrics:
        print(f"\n🔬 Market Comparison:")
        print(f"  Alpha:                {metrics['alpha']*100:>8.2f}%")
        print(f"  Beta:                 {metrics['beta']:>8.3f}")
    
    print("="*60 + "\n")


def compare_strategies(strategy1_returns, strategy2_returns, 
                       names=["Strategy 1", "Strategy 2"]):
    """
    Compare two strategies side-by-side
    
    Parameters:
    -----------
    strategy1_returns : pd.Series
        Returns for first strategy
    strategy2_returns : pd.Series
        Returns for second strategy
    names : list
        Names for the strategies
    """
    metrics1 = calculate_comprehensive_metrics(strategy1_returns)
    metrics2 = calculate_comprehensive_metrics(strategy2_returns)
    
    comparison = pd.DataFrame({
        names[0]: metrics1,
        names[1]: metrics2
    })
    
    # Calculate differences
    comparison['Difference'] = comparison[names[1]] - comparison[names[0]]
    
    return comparison