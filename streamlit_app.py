import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    excel_file = "Data/Twave - results.xlsx"
    csv_file = "most_recent_readings.csv"
    df_excel = pd.read_excel(excel_file, sheet_name="Sheet1")
    df_csv = pd.read_csv(csv_file)
    return df_excel, df_csv

# Load the data
df_excel, df_csv = load_data()

# Sidebar
st.sidebar.title("Fan Skid Predictive Maintenance")
st.sidebar.markdown("### Focus on Belt Imbalance and Misalignment")

# Current Health Status
st.title("Current Machine Health Status")
st.metric(label="Driven Unbalance/Misalignment", value=f"{df_csv['Driven Unbalance/Misalignment'].iloc[-1]:.2f}")
st.metric(label="Motor Unbalance/Misalignment", value=f"{df_csv['Motor Unbalance/Misalignment'].iloc[-1]:.2f}")

# Projected Costs
st.title("Projected Cost Impact")
current_waste = df_csv['WasteCost'].iloc[-1]
st.write(f"**Current Daily Loss:** £{current_waste:.2f}")
st.write(f"**2 Days Loss:** £{current_waste * 2:.2f}")
st.write(f"**7 Days Loss:** £{current_waste * 7:.2f}")

# Insights
st.title("Insights and Recommendations")
if df_csv['Driven Unbalance/Misalignment'].iloc[-1] > 0.5:
    st.warning("⚠️ High driven unbalance/misalignment detected. Immediate maintenance recommended!")
if df_csv['Motor Unbalance/Misalignment'].iloc[-1] > 0.5:
    st.warning("⚠️ High motor unbalance/misalignment detected. Immediate maintenance recommended!")

# Link to Maintenance Procedure
st.markdown("### [🔧 Maintenance Procedure](https://example.com/maintenance-guide)")
