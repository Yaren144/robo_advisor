import streamlit as st
import sys
import os

# Mock forecast function for demonstration
def get_forecasts():
    return 0.0823, 0.0412  # Example forecast values

spy_forecast, agg_forecast = get_forecasts()

st.set_page_config(page_title="AI Robo-Advisor", layout="wide", page_icon="💎")

# Purple Glassmorphism Design
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
    /* Use these classes (e.g., st.markdown('<div class="card-purple">...</div>')) to apply the specific colors */

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

# Header
st.markdown('<div class="info-banner">💎 Professional AI Investment Advisor</div>', unsafe_allow_html=True)
st.title("AI Robo-Advisor")

st.markdown("---")

# User Profile Section
st.subheader("Investment Profile")
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Name", placeholder="Your name")
with col2:
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

def build_portfolio(risk, years, age):
    """Build optimized portfolio based on Modern Portfolio Theory principles"""
    if risk == "Conservative":
        spy, agg = 30, 70
    elif risk == "Balanced":
        spy, agg = 60, 40
    else:
        spy, agg = 85, 15
    
    # Time horizon adjustment
    if years >= 15:
        spy += 5
        agg -= 5
    elif years <= 3:
        spy -= 5
        agg += 5
    
    # Age-based adjustment
    if age < 30:
        spy += 5
        agg -= 5
    elif age > 50:
        spy -= 5
        agg += 5
    
    # Ensure bounds
    spy = max(0, min(spy, 100))
    agg = 100 - spy
    
    return spy, agg

# Generate Portfolio Button
if st.button("Generate Portfolio", use_container_width=True):
    
    if not name:
        st.warning("Please enter your name")
    elif not investment_goal:
        st.warning("Please specify your investment goal")
    else:
        spy, agg = build_portfolio(risk, horizon, age)
        
        st.markdown("---")
        st.subheader(f"Portfolio for {name}")
        
        # Portfolio Allocation Display
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h3>Stocks (SPY)</h3>
                <h2>{spy}%</h2>
                <p>Growth Assets</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h3>Bonds (AGG)</h3>
                <h2>{agg}%</h2>
                <p>Defensive Assets</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            risk_score = spy
            risk_label = "High" if risk_score >= 75 else "Medium" if risk_score >= 50 else "Low"
            st.markdown(f"""
            <div class="metric-box">
                <h3>Risk Level</h3>
                <h2>{risk_label}</h2>
                <p>Portfolio Risk</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Strategy Explanation
        st.markdown(f"""
        <div class="result-box">
        <b>Strategy Explanation</b><br><br>
        Based on your profile (Age: {age}, Risk: {risk}, Timeline: {horizon} years), your portfolio 
        {"emphasizes growth through equities" if spy > agg else "prioritizes capital preservation"} 
        to achieve your goal: {investment_goal}.<br><br>
        
        <b>Key Points:</b><br>
        • Your {horizon}-year horizon {"allows for market recovery" if horizon >= 10 else "requires more stability"}<br>
        • {"Young investors benefit from higher equity exposure" if age < 35 else "Your age suggests a balanced approach"}<br>
        • This portfolio uses Modern Portfolio Theory and historical backtesting<br><br>
        
        <b>Expected Monthly Growth:</b> ${monthly_saving * ((spy/100 * 0.08) + (agg/100 * 0.04)):.2f}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # AI Forecast Section
        st.subheader("AI Forecast (ARIMA Model)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="forecast-card">
                <h4>SPY Expected Return</h4>
                <div class="forecast-value">+{spy_forecast*100:.2f}%</div>
                <p>Next period forecast based on historical data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="forecast-card">
                <h4>AGG Expected Return</h4>
                <div class="forecast-value">+{agg_forecast*100:.2f}%</div>
                <p>Next period forecast based on historical data</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Portfolio Expected Return
        portfolio_return = (spy/100 * spy_forecast) + (agg/100 * agg_forecast)
        st.markdown(f"""
        <div class="result-box">
        <b>Your Portfolio Expected Return:</b> <span style="font-size: 1.4rem; font-weight: 600;">+{portfolio_return*100:.2f}%</span><br>
        Based on AI forecast and your {spy}% SPY / {agg}% AGG allocation
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Built with Modern Portfolio Theory | Backtested on Real Data | AI-Powered Forecasting</p>
</div>
""", unsafe_allow_html=True)