import streamlit as st
import pandas as pd

st.title("Robo-Advisor Dashboard")

df = pd.read_csv("analysis/portfolio_recommendations.csv")

risk = st.selectbox("Select Risk Profile", ["Conservative", "Balanced", "Aggressive"])

years = st.slider("Investment Horizon (years)", 1, 10, 5)

rec = df[df['Risk_Profile'] == risk].iloc[0]

if risk == "Aggressive":
    st.write("This portfolio favors stocks because you selected a high-risk profile and a longer time horizon.")

st.write("### Recommended Portfolio")
st.write("SPY:", round(rec["Weight_SPY"]*100,2), "%")
st.write("AGG:", round(rec["Weight_AGG"]*100,2), "%")
st.write("Expected Return:", round(rec["Expected_Return"]*100,2), "%")
