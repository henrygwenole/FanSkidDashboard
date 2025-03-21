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
    fault_values = [10, 15, 20, 30, 45]  # Placeholder fault progression
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_series, y=fault_values, mode='lines+markers', name='Fault Trend'))
    
    fig.update_layout(title="Fault Progression Over Time", xaxis_title="Date", yaxis_title="Severity Index")
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

# Streamlit UI
st.set_page_config(page_title="Machine Monitoring Dashboard")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Faults", "Maintenance"])

if page == "Home":
    st.title("Machine Monitoring Dashboard")
    st.write("Overview of machine health and power waste.")
    
    # Display machine ID and live status
    machine_status = get_machine_status()
    st.write(f"**Machine ID:** {MACHINE_ID}")
    st.write(f"**Status:** {'🟢 Online' if machine_status == 'Online' else '🔴 Offline'}")
    
    # Display hexagonal health chart
    st.plotly_chart(create_health_chart())

elif page == "Faults":
    fault_page = st.sidebar.radio("Select Subpage", ["Issues", "Fault Details"])
    if fault_page == "Issues":
        st.header("Issues and Flags")
        st.write(f"List of flagged issues for {MONITORED_MACHINE}.")
        if st.button("View Fault Details"):
            st.session_state.page = "Fault Details"
    elif fault_page == "Fault Details":
        st.header("Fault Information")
        st.write(f"Detailed chart about faults for {MONITORED_MACHINE}.")
        st.plotly_chart(create_fault_trend_chart())
        st.button("Plan Maintenance")

elif page == "Maintenance":
    st.header("Maintenance")
    st.write(f"Scheduled maintenance actions for {MONITORED_MACHINE}.")
    
    # Display maintenance history as a table
    st.subheader("Maintenance History")
    st.table(maintenance_history)
    
    # Display planned maintenance activities as a table
    st.subheader("Upcoming Maintenance")
    st.table(planned_maintenance)
    
    st.write("[Frontline IO App](#)")  # Placeholder for link
