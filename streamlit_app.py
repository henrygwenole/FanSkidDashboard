import streamlit as st
import plotly.graph_objects as go

# Function to create the hexagonal radar chart
def create_health_chart():
    categories = ['Vibration', 'Temperature', 'Power Usage', 'Wear & Tear', 'Efficiency', 'Load']
    values = [70, 85, 60, 40, 75, 90]  # Sample values representing health metrics
    
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

# Display hexagonal health chart
st.plotly_chart(create_health_chart())

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Issues", "Fault Information", "Planned Maintenance"])

if page == "Issues":
    st.header("Issues and Flags")
    st.write("List of flagged issues.")
    if st.button("View Fault Details"):
        st.session_state.page = "Fault Information"

elif page == "Fault Information":
    st.header("Fault Information")
    st.write("Detailed chart about faults.")
    st.button("Plan Maintenance")

elif page == "Planned Maintenance":
    st.header("Planned Maintenance")
    st.write("Scheduled maintenance actions.")
    st.write("[Frontline IO App](#)")  # Placeholder for link

else:
    st.header("Welcome to the Machine Monitoring Dashboard")

