import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Placeholder function to get source names from a dataset
def get_source_names():
    return ["Machine A", "Machine B", "Machine C", "Machine D"]  # Placeholder values

# Function to create the hexagonal radar chart
def create_health_chart():
    categories = ['Vibration', 'Temperature', 'Power Usage', 'Wear & Tear', 'Efficiency', 'Load']
    values = [70, 85, 60, 40, 75, 90]  # Placeholder values representing health metrics
    
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

# Streamlit UI
st.set_page_config(page_title="Machine Monitoring Dashboard")

st.title("Machine Monitoring Dashboard")
st.write("Overview of machine health and power waste.")

# Dropdown to select source (machine)
source_names = get_source_names()
selected_source = st.selectbox("Select Machine:", source_names)

# Display hexagonal health chart
st.plotly_chart(create_health_chart())

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Issues", "Fault Information", "Planned Maintenance"])

if page == "Issues":
    st.header("Issues and Flags")
    st.write(f"List of flagged issues for {selected_source}.")
    if st.button("View Fault Details"):
        st.session_state.page = "Fault Information"

elif page == "Fault Information":
    st.header("Fault Information")
    st.write(f"Detailed chart about faults for {selected_source}.")
    st.button("Plan Maintenance")

elif page == "Planned Maintenance":
    st.header("Planned Maintenance")
    st.write(f"Scheduled maintenance actions for {selected_source}.")
    st.write("[Frontline IO App](#)")  # Placeholder for link

else:
    st.header("Welcome to the Machine Monitoring Dashboard")
