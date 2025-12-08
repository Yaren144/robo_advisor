import streamlit as st

st.set_page_config(page_title="AI Robo Advisor", layout="centered")

st.title("AI Robo Advisor")

# --- USER INPUTS ---
name = st.text_input("Your name")
age = st.slider("Your age", 18, 70, 25)
goal = st.selectbox("Your main goal", ["Wealth Growth", "Retirement", "Short-term Savings"])
risk = st.selectbox("Risk Profile", ["Conservative", "Balanced", "Aggressive"])
years = st.slider("Investment Horizon (years)", 1, 20, 5)

# --- LOGIC ---
spy = 0
agg = 0

if risk == "Conservative":
    spy = 30
    agg = 70
elif risk == "Balanced":
    spy = 60
    agg = 40
else:
    spy = 85
    agg = 15

# Adjust by time horizon
if years >= 10:
    spy += 5
    agg -= 5
elif years <= 3:
    spy -= 5
    agg += 5

# --- FINAL OUTPUT ---
st.subheader(f"Personalized Portfolio for {name if name else 'you'}")

st.write(f"### 📊 Recommended Allocation")
st.write(f"**SPY (Stocks ETF):** {spy}%")
st.write(f"**AGG (Bonds ETF):** {agg}%")

# --- EXPLANATION ---
st.write("### 🧠 Why this portfolio?")
st.write(
    f"This recommendation is based on your risk preference ({risk}) "
    f"and your investment horizon ({years} years), adjusted for your goal ({goal})."
)

# --- SCENARIO SIMULATION ---
st.write("### 📈 Possible 1-Year Outcomes")

if risk == "Conservative":
    worst, expected, best = -3, 4, 7
elif risk == "Balanced":
    worst, expected, best = -6, 8, 12
else:
    worst, expected, best = -10, 12, 18

st.success(f"📉 Worst case: {worst}%")
st.info(f"📊 Expected case: {expected}%")
st.warning(f"📈 Best case: {best}%")
