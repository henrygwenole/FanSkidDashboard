# Home.py
import streamlit as st

st.set_page_config(page_title="Predictive Maintenance Overview", layout="wide")
st.title("🛠️ Predictive Maintenance Dashboard")

st.markdown("""
Welcome to the G.U.N.T. Predictive Maintenance Dashboard.

This homepage summarizes the health of key machine components and links to sensor analysis views.
""")

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

st.write("\n")
st.page_link("pages/Sensor_Data.py", label="🔍 View Sensor Analysis", icon="📈")
