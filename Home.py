# Home.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")
st.title("🛠️ Predictive Maintenance Dashboard")

st.markdown("""
Welcome to the G.U.N.T. Predictive Maintenance Dashboard.
This homepage provides an overview of machine health and operational impact.
""")

# --- System Health Overview Grid ---
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

cols = st.columns(3)
for i, (label, status) in enumerate(status_map.items()):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style='padding:1rem; background-color:{'#d4edda' if status else '#f8d7da'}; border:1px solid {'#155724' if status else '#721c24'}; border-radius:10px'>
                <h4 style='color:{'#155724' if status else '#721c24'}'>{'✅' if status else '❌'} {label}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Waste & Cost Summary ---
st.markdown("""
### 🧾 Estimated Operational Waste & Cost
""")

try:
    recent_df = pd.read_csv("data/most_recent_readings.csv")
    vibration = recent_df["Vibration RMS"].mean()
    speed = recent_df["Speed"].mean()
    hours = recent_df["Operation Hours"].mean()

    waste_kg = vibration * hours * 0.8  # illustrative formula
    cost_gbp = waste_kg * 18.5          # £18.5 per kg

    st.metric("Estimated Waste (kg)", f"{waste_kg:.2f}")
    st.metric("Estimated Cost (GBP)", f"£{cost_gbp:.2f}")
except Exception as e:
    st.warning("⚠️ Could not calculate waste. Please check the data file.")

# --- Link to Sensor Details ---
st.page_link("pages/Sensor_Data.py", label="📈 Go to Sensor Analysis", icon="📊")