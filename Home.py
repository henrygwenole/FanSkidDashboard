# Home.py
import streamlit as st
import pandas as pd
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

try:
    total_waste_kwh = 1450.0  # monthly energy waste
    total_cost = 1000.0       # monthly cost (£)
    high_waste_events = 25

    st.metric("High-Waste Events", high_waste_events)
    st.metric("Monthly Energy Waste (kWh)", f"{total_waste_kwh:,.0f} kWh")
    st.metric("Estimated Monthly Cost (£)", f"£{total_cost:,.0f}")

    st.subheader("📉 Energy Waste Trend (Simulated)")

    # Simulated energy loss data over a 30-day period
    days = np.arange(1, 31)
    energy_loss_percent = 2 + 0.4 * days + np.random.normal(0, 1, size=len(days))  # Simulate trend

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(days, energy_loss_percent, color='black', linewidth=2)
    ax.fill_between(days, 0, 5, color='green', alpha=0.2, label='Optimal')
    ax.fill_between(days, 5, 10, color='orange', alpha=0.2, label='Moderate')
    ax.fill_between(days, 10, max(energy_loss_percent) + 5, color='red', alpha=0.2, label='High')
    ax.axhline(10, color='red', linestyle='--', linewidth=1)
    ax.set_xlabel("Day")
    ax.set_ylabel("Energy Loss (%)")
    ax.set_title("Simulated Energy Loss Trend Over Time")
    ax.legend(loc="upper left")
    ax.grid(True)

    st.pyplot(fig)

except Exception as e:
    st.warning("⚠️ Could not calculate waste. Please check the data file.")

st.markdown("""
---

### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)