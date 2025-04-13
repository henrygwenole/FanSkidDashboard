# Home.py
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")
st.title("🛠️ Predictive Maintenance Dashboard")

st.markdown("""
Welcome to the Predictive Maintenance Dashboard. This interface provides insights into vibration patterns,
frequency characteristics, and potential maintenance needs based on recent sensor data.

Use the navigation menu to explore:
- 📈 **Sensor Signal Analysis**: Time-domain and frequency-domain inspection
- 🧠 **Fault Classification**: Pattern-based condition assessment
- 🔍 **Waste & Cost Insights**: Estimated inefficiencies based on vibration data
""")

# Status indicators
status_map = {
    "Motor Foundation": True,
    "Motor DE Bearing": False,
    "Motor NDE Bearing": True,
    "Motor Misalignment": True,
    "Driven 1 Foundation": True,
    "Driven 1 DE Bearing": True,
    "Driven 1 Transmission": False,
    "Driven 1 NDE Bearing": True,
    "Driven 1 Misalignment": True,
}

st.header("🩺 System Health Overview")
for label, status in status_map.items():
    color = "green" if status else "red"
    symbol = "✅" if status else "❌"
    st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:10px; color:white; margin-bottom:5px;'>"
                f"<strong>{symbol} {label}</strong></div>", unsafe_allow_html=True)

st.header("🧾 Estimated Operational Waste & Cost")
try:
    df = pd.read_csv("data/most_recent_readings.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    threshold = 0.15
    high_vibration = df[df["rms"] > threshold]

    waste_kwh = len(high_vibration) * 0.5
    cost = waste_kwh * 0.15

    st.metric("Detected High-Vibration Events", len(high_vibration))
    st.metric("Estimated Energy Waste (kWh)", f"{waste_kwh:.1f}")
    st.metric("Estimated Cost (£)", f"£{cost:.2f}")

except Exception as e:
    st.warning("⚠️ Could not calculate waste. Please check the data file.")

st.markdown("""
---

### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)