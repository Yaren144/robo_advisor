import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import ast

# Ensure we can import from the same directory or analysis folder if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Ensemble forecast function
# Assuming arima_optimizer.py is in the same folder as app.py (dashboard/)
try:
    from analysis.ensemble_forecast import get_ensemble_forecast
except ImportError:
    # Fallback if running from root and files are in dashboard/
    sys.path.append(os.path.join(os.getcwd(), 'dashboard'))
    try:
        from analysis.ensemble_forecast import get_ensemble_forecast
    except ImportError:
        # Mock if absolutely cannot find it
        def get_forecasts():
            return 0.0005, 0.0001

# Cache the heavy ARIMA calculation so it doesn't rerun on every click
@st.cache_data
def get_cached_ensemble_forecasts():
    from analysis.ensemble_forecast import get_robust_forecasts
    return get_robust_forecasts()

spy_forecast, agg_forecast, spy_info, agg_info, spy_arima, agg_arima = get_cached_ensemble_forecasts()

st.set_page_config(page_title="AI Robo-Advisor", layout="wide", page_icon="💎")

# --- STYLING (EXACT COPY OF YOUR CSS) ---
st.markdown("""
<style>
    /* 🎨 Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 🌌 Darker, More Professional Purple Background */
    .stApp {
        /* Deep Indigo-Violet Gradient */
        background: linear-gradient(135deg, #1A0D3C 0%, #30195C 50%, #442278 100%);
        background-attachment: fixed;
    }
    
    /* --- General Text/Header Styling --- */
    
    h1 {
        color: #E0E0FF !important; /* Lighter text for contrast */
        font-weight: 700 !important; /* Slightly bolder for emphasis */
        font-size: 2.8rem !important; 
        letter-spacing: -0.04em;
    }
    
    h2, h3, h4 {
        color: #F0F0FF !important; 
        font-weight: 600 !important; 
        letter-spacing: -0.02em;
    }

    p, span, div:not(.element-container) {
        color: #D8D8E8; /* Soft white for readability */
        font-weight: 400;
    }
    
    /* --- Glassmorphism Containers (The "Clean" Card Base) --- */
    .glass, .metric-box, .result-box, .forecast-card {
        background: rgba(255, 255, 255, 0.05); /* Less opaque base glass */
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtler border */
        border-radius: 18px; /* Slightly smaller radius for professionalism */
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.25); /* Darker, more grounded shadow */
        transition: all 0.3s ease-in-out;
        margin-top: 3.5rem;
    }

    .glass:hover, .metric-box:hover, .result-box:hover, .forecast-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    
    /* --- Different but Matching Card Backgrounds --- */
    
    /* 1. Dark Purple Card */
    .card-purple {
        background: linear-gradient(145deg, rgba(50, 20, 90, 0.9), rgba(30, 10, 60, 0.9));
        border: 1px solid rgba(150, 100, 255, 0.3);
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    /* 2. Dark Indigo Card */
    .card-indigo {
        background: linear-gradient(145deg, rgba(30, 20, 80, 0.9), rgba(15, 10, 50, 0.9));
        border: 1px solid rgba(120, 100, 200, 0.3);
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    /* 3. Dark Violet Card */
    .card-violet {
        background: linear-gradient(145deg, rgba(65, 30, 100, 0.9), rgba(40, 15, 70, 0.9));
        border: 1px solid rgba(180, 120, 255, 0.3);
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    /* --- Input Field Refinements --- */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(255, 255, 255, 0.08) !important; 
        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
        color: #ffffff !important;
        border-radius: 12px !important; /* Smaller radius for inputs */
        padding: 0.75rem 1rem;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #A080FF !important; /* Light accent color on focus */
        box-shadow: 0 0 0 1px #A080FF;
    }
    
    /* Labels */
    label {
        color: #F0F0FF !important; 
        font-weight: 500 !important;
    }
    
    /* --- Button Refinements --- */
    .stButton button {
        background: linear-gradient(45deg, #7040A0, #A060C0) !important; /* Solid, darker professional gradient */
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #8550B5, #B570D5) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
    }
    
    /* --- Metric Box Refinements --- */
    .metric-box h3 {
        color: rgba(255, 255, 255, 0.8) !important; 
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .metric-box h2 {
        color: #A080FF !important; /* Use accent color for main value */
        font-size: 3.2rem;
        font-weight: 700;
    }
    
    .metric-box p {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.8rem;
    }
    
    /* --- Footer/Info Banner Refinements --- */
    .info-banner {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        color: #F0F0FF;
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        background: rgba(255, 255, 255, 0.15);
        margin: 2rem 0;
    }
    
</style>
""", unsafe_allow_html=True)

# --- LOAD OPTIMIZED PORTFOLIOS ---
# We load the results generated by mpt_optimizer.py
# This ensures the app uses REAL MPT math, not mock rules.
@st.cache_data
def load_mpt_data():
    # Try multiple paths to find the CSV
    possible_paths = [
        "portfolio_recommendations.csv",
        "analysis/portfolio_recommendations.csv",
        "../portfolio_recommendations.csv"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

mpt_df = load_mpt_data()

# Use fallback MPT data if CSV is missing (prevents app crash)


# Convert to dictionary for easy lookup: { 'Conservative': { 'Weight_SPY': ... } }
PORTFOLIOS = mpt_df.set_index("Risk_Profile").T.to_dict()




# --- HEADER ---
st.markdown('<div class="info-banner">💎 Professional AI Investment Advisor</div>', unsafe_allow_html=True)
st.title("AI Robo-Advisor")

st.markdown("---")

# --- USER INPUTS ---
st.subheader("Investment Profile")
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Name", placeholder="Your name")
with col2:
    # Age is collected but not used in logic (as requested)
    age = st.number_input("Age", min_value=18, max_value=100, value=25)
with col3:
    monthly_saving = st.number_input("Monthly Investment ($)", value=500, step=100)

col4, col5, col6 = st.columns(3)
with col4:
    risk = st.selectbox("Risk Preference", ["Conservative", "Balanced", "Aggressive"])
with col5:
    horizon = st.slider("Investment Horizon (Years)", 1, 30, 10)
with col6:
    investment_goal = st.text_input("Investment Goal", placeholder="e.g., House, Retirement")

st.markdown("---")

# --- GENERATE PORTFOLIO LOGIC ---
if st.button("Generate Portfolio", use_container_width=True):
    
    if not name:
        st.warning("Please enter your name")
    elif not investment_goal:
        st.warning("Please specify your investment goal")
    else:
        # 1. Retrieve MPT Optimized Weights (Base Allocation)
        # ----------------------------------------------------
        # Get base allocation from MPT
        if risk in PORTFOLIOS:
            base_data = PORTFOLIOS[risk]
            base_spy = base_data['Weight_SPY'] * 100
            base_agg = base_data['Weight_AGG'] * 100
            base_sharpe = base_data['Sharpe_Ratio']
        else:
            st.error(f"Risk profile '{risk}' not found")
            st.stop()

        # Adjust for horizon
        if horizon >= 15:
            adjustment = 10  # +10% stocks for long horizon
        elif horizon <= 5:
            adjustment = -10  # -10% stocks for short horizon
        else:
            adjustment = 0  # No change for medium

        final_spy = max(20, min(90, base_spy + adjustment))
        final_agg = 100 - final_spy
        
        # 3. Calculate Financial Projections
        # ----------------------------------------------------
        # Daily expected return based on weighted average of ARIMA forecasts
        daily_exp_return = (final_spy/100 * spy_forecast) + (final_agg/100 * agg_forecast)
        # Annualized portfolio return
        ann_port_return = daily_exp_return * 252

        
        # Monthly return estimate (approx 21 trading days)
        # Formula: P * ((1 + r)^21 - 1)
        monthly_growth_rate = (1 + daily_exp_return)**21 - 1
        est_monthly_return_amt = monthly_saving * monthly_growth_rate

        # Risk Label
        risk_score = final_spy
        risk_label = "High" if risk_score >= 75 else "Medium" if risk_score >= 40 else "Low"

        # --- DISPLAY RESULTS ---
        st.markdown("---")
        st.subheader(f"Portfolio for {name}")
        
        # Row 1: Key Metrics
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h3>Stocks (SPY)</h3>
                <h2>{final_spy:.1f}%</h2>
                <p>Growth Assets</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h3>Bonds (AGG)</h3>
                <h2>{final_agg:.1f}%</h2>
                <p>Defensive Assets</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <h3>Risk Level</h3>
                <h2>{risk_label}</h2>
                <p>Sharpe: {base_sharpe:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2: Explanation & Monthly Projection
        st.markdown(f"""
    <div class="result-box">
    <b>Strategy Explanation</b><br><br>

    <b>MPT Base Allocation:</b> {base_spy:.0f}% SPY / {base_agg:.0f}% AGG<br>
    <b>Horizon Adjustment:</b> {adjustment:+.0f}% for {horizon}-year timeline<br>
    <b>Final Allocation:</b> {final_spy:.0f}% SPY / {final_agg:.0f}% AGG<br><br>

    Portfolio optimized using Modern Portfolio Theory with Sharpe ratio of {base_sharpe:.2f}.<br><br>

    <b>Est. Monthly Return:</b> <span style="color:#A080FF; font-weight:bold">${est_monthly_return_amt:.2f}</span>
    </div>
""", unsafe_allow_html=True)
        
                
        
    st.markdown(f"""
    <div class="forecast-card">
        <h4>🎯 Expected Performance</h4>
        <div class="forecast-value">{ann_port_return*100:.1f}%</div>
        <p>Annual Return</p>
        <hr>
        <p style="font-size:0.85em;">
        • Monthly contribution: ${monthly_saving:,.0f}<br>
        • Est. monthly gain: ${est_monthly_return_amt:.2f}<br>
        • Risk-adjusted: {base_sharpe:.2f} Sharpe
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Built with Modern Portfolio Theory | Backtested on Real Data | AI-Powered Forecasting</p>
</div>
""", unsafe_allow_html=True)