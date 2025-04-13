# Home.py
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

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

# Updated example values (hardcoded for illustration)
try:
    total_waste_kwh = 1450.0  # monthly energy waste
    total_cost = 1000.0       # monthly cost (£)
    high_waste_events = 25

    st.metric("High-Waste Events", high_waste_events)
    st.metric("Monthly Energy Waste (kWh)", f"{total_waste_kwh:,.0f} kWh")
    st.metric("Estimated Monthly Cost (£)", f"£{total_cost:,.0f}")

    # Predicted future cost if maintenance is delayed
    st.subheader("📅 Projected Cost If Maintenance Is Delayed")
    daily_cost = total_cost / 30
    for days in range(1, 4):
        projected_cost = total_cost + (days * daily_cost)
        st.markdown(f"<div style='font-size:16px;'>If delayed by {days} day(s): <strong>£{projected_cost:,.2f}</strong></div>", unsafe_allow_html=True)

    # Trend plot
    st.subheader("📊 Trend: Trans1 Belt Drive")
    days = np.arange(1, 31)
    values = np.concatenate([
        np.linspace(0, 5, 10),
        np.linspace(5, 15, 10),
        np.linspace(15, 20, 10)
    ])
    plt.figure(figsize=(10, 4))
    plt.plot(days, values, color='green')
    plt.fill_between(days, 10, 20, color='sandybrown', alpha=0.3)
    plt.xlabel("Measurements for day")
    plt.ylabel("Trend Value")
    plt.title("Trend: Trans1 Belt Drive")
    plt.grid(True)
    st.pyplot(plt)

except Exception as e:
    st.warning("⚠️ Could not calculate waste. Please check the data file.")

st.markdown("""
---

### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)
