import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# Define monitored machine
MONITORED_MACHINE = "Fan Skid"
MACHINE_ID = "FSK-001"  # Example ID

# Function to simulate machine live status
def get_machine_status():
    return "Online" if random.choice([True, True, False]) else "Offline"

# Function to simulate belt drive misalignment severity
def get_alignment_severity():
    return random.choice(["Low", "Moderate", "High"])

# Function to create the hexagonal radar chart
def create_health_chart():
    categories = ['Vibration', 'Temperature', 'Power Usage', 'Wear & Tear', 'Efficiency', 'Load']
    values = [65, 80, 55, 45, 70, 85]  # Placeholder values aligned with real system
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Closing the loop
        theta=categories + [categories[0]],
        fill='toself',
        name='Machine Health'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True
    )
    return fig

# Function to create a sample fault trend chart
def create_fault_trend_chart():
    time_series = ["May 10", "May 15", "May 20", "May 25", "June 1"]
    fault_values = [10, 15, 30, 45, 60]  # Simulated fault progression
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_series, y=fault_values, mode='lines+markers', name='Fault Trend'))
    
    fig.update_layout(title="Belt Drive Alignment Fault Over Time", xaxis_title="Date", yaxis_title="Misalignment Severity Index")
    return fig

# Maintenance history and planned activities data (placeholder)
maintenance_history = pd.DataFrame([
    {"Date": "October", "Task": "Belt replaced and belt alignment corrected"},
    {"Date": "June", "Task": "Motor drive end bearing replaced"}
])

planned_maintenance = pd.DataFrame([
    {"Date": "December", "Task": "Lubrication check and fan blade inspection"},
    {"Date": "March", "Task": "Motor full inspection and electrical testing"}
])

# Shared status variables
machine_status = get_machine_status()
alignment_severity = get_alignment_severity()

# Streamlit UI
st.set_page_config(page_title="Machine Monitoring Dashboard")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Monitoring", "Maintenance"])

if page == "Home":
    st.title("Machine Monitoring Dashboard")
    st.write("Overview of machine health and power waste.")
    
    st.write(f"**Machine ID:** {MACHINE_ID}")
    st.write(f"**Status:** {'🟢 Online' if machine_status == 'Online' else '🔴 Offline'}")
    st.write(f"**Belt Drive Alignment Severity:** {alignment_severity}")
    
    st.plotly_chart(create_health_chart())

elif page == "Monitoring":
    st.header("Machine Condition Monitoring")
    st.write("Overview of machine status and detected issues.")
    
    # Simulated fault statuses (Green: Good, Orange: Needs Monitoring, Red: Critical Issue)
    fault_conditions = pd.DataFrame([
        {"Component": "Motor Foundation", "Status": "Good"},
        {"Component": "Motor Transmission", "Status": "Critical"},
        {"Component": "Drive 1 Unbalance", "Status": "Good"},
        {"Component": "Drive 1 DE Bearing", "Status": "Good"},
        {"Component": "Drive 1 Transmission", "Status": "Needs Monitoring"},
        {"Component": "Motor DE Bearing", "Status": "Critical"}
    ])
    
    def get_status_color(status):
        return {"Good": "#4CAF50", "Needs Monitoring": "#FFA500", "Critical": "#FF0000"}.get(status, "#CCCCCC")
    
    for _, row in fault_conditions.iterrows():
        st.markdown(f'<div style="background-color:{get_status_color(row["Status"])};padding:10px;border-radius:5px;margin:5px 0;color:white;text-align:center;">{row["Component"]} - {row["Status"]}</div>', unsafe_allow_html=True)
    
    if st.button("View Fault Details", key="view_fault_details_btn"): 
        st.session_state.page = "Fault Details"
    fault_page = st.sidebar.radio("Select Subpage", ["Issues", "Fault Details"])
    if fault_page == "Issues":
        st.header("Issues and Flags")
        st.write(f"List of flagged issues for {MONITORED_MACHINE}.")
        st.write(f"**Belt Alignment Issue Severity:** {alignment_severity}")
        if st.button("View Fault Details", key="view_fault_details_btn"): 
            st.session_state.page = "Fault Details"
    elif fault_page == "Fault Details":
        st.header("Belt Drive Fault Information")
        st.write(f"Detailed chart about belt drive misalignment for {MONITORED_MACHINE}.")
        st.plotly_chart(create_fault_trend_chart())
        st.button("Plan Maintenance")

elif page == "Maintenance":
    st.header("Maintenance")
    st.write(f"Scheduled maintenance actions for {MONITORED_MACHINE}.")
    
    st.subheader("Maintenance History")
    st.table(maintenance_history)
    
    st.subheader("Upcoming Maintenance")
    st.table(planned_maintenance)
    
    st.write("[Frontline IO App](#)")  # Placeholder for link
