import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Define the Relative Path ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "Data")  # Uses relative path

# --- File Paths ---
file_readings = os.path.join(DATA_PATH, "most_recent_readings.csv")
file_twave = os.path.join(DATA_PATH, "Twave - results.csv")

# --- Check if files exist ---
if not os.path.exists(file_readings):
    st.error(f"❌ File not found: {file_readings}")
if not os.path.exists(file_twave):
    st.error(f"❌ File not found: {file_twave}")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df_readings = pd.read_csv(file_readings)
        df_twave = pd.read_csv(file_twave)

        # Debugging: Show first few rows
        st.write("✅ Data Loaded Successfully!")
        st.write("Data Preview (Readings):", df_readings.head())
        st.write("Data Preview (Twave):", df_twave.head())

        # Clean column names (remove spaces)
        df_readings.columns = df_readings.columns.str.strip()
        df_twave.columns = df_twave.columns.str.strip()

        # Ensure 'timestamp' column exists
        if 'timestamp' not in df_readings.columns:
            st.error("❌ 'timestamp' column missing in most_recent_readings.csv!")
        if 'timestamp' not in df_twave.columns:
            st.error("❌ 'timestamp' column missing in Twave - results.csv!")

        # Convert 'timestamp' to datetime if needed
        try:
            df_readings['timestamp'] = pd.to_datetime(df_readings['timestamp'])
        except:
            st.error("⚠️ 'timestamp' column is not in datetime format!")

        return df_readings, df_twave
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None, None

df_readings, df_twave = load_data()

# --- Proceed only if data is loaded ---
if df_readings is not None and df_twave is not None:

    # --- Define Misalignment & Looseness Thresholds ---
    MISALIGNMENT_THRESHOLD = 0.5  # Alert if > 0.5
    LOOSENESS_THRESHOLD = 4.0  # Alert if > 4.0

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filter Options")
    time_filter = st.sidebar.slider("Select Time Range (minutes)", 
                                    min_value=0, max_value=len(df_readings)-1, 
                                    value=(0, len(df_readings)-1))

    # Apply filter
    df_filtered = df_readings.iloc[time_filter[0]:time_filter[1]]

    # --- Debugging: Show Filtered Data ---
    st.write("Filtered Data Preview:", df_filtered.head())

    # --- Line Chart: Misalignment & Looseness ---
    try:
        fig_misalignment = px.line(df_filtered, x='timestamp', 
                                   y=['Driven Unbalance/Misalignment', 'Motor Unbalance/Misalignment'],
                                   labels={'value': "Misalignment Level", 'timestamp': "Time"},
                                   title="📈 Misalignment Over Time")
        fig_misalignment.add_hline(y=MISALIGNMENT_THRESHOLD, line_dash="dot", line_color="red")
        st.plotly_chart(fig_misalignment)
    except Exception as e:
        st.error(f"❌ Error plotting Misalignment Chart: {e}")

    try:
        fig_looseness = px.line(df_filtered, x='timestamp', 
                                y=['Transmission Looseness (Motor)', 'Transmission Looseness (Driven)'],
                                labels={'value': "Looseness Level", 'timestamp': "Time"},
                                title="📉 Transmission Looseness Over Time")
        fig_looseness.add_hline(y=LOOSENESS_THRESHOLD, line_dash="dot", line_color="red")
        st.plotly_chart(fig_looseness)
    except Exception as e:
        st.error(f"❌ Error plotting Looseness Chart: {e}")

    # --- Diagnostic Flags Section ---
    st.subheader("🚨 Diagnostic Flags & Anomalies")
    try:
        anomalies = df_filtered[(df_filtered['Driven Unbalance/Misalignment'] > MISALIGNMENT_THRESHOLD) |
                                (df_filtered['Transmission Looseness (Motor)'] > LOOSENESS_THRESHOLD)]
        if not anomalies.empty:
            st.error("⚠️ Belt Misalignment Detected! Check flagged timestamps below.")
            st.dataframe(anomalies)
        else:
            st.success("✅ No major misalignment issues detected.")
    except Exception as e:
        st.error(f"❌ Error detecting anomalies: {e}")

    # --- Maintenance Procedures ---
    st.subheader("🔧 Maintenance Procedures")
    st.markdown("Click the link below to access maintenance procedures:")
    st.markdown("[Open Maintenance Guide](https://your-app-link.com)")

    # --- Additional Vibration Analysis (Twave) ---
    st.subheader("📊 Vibration Data Analysis")
    try:
        fig_vibration = px.line(df_twave, x='timestamp', 
                                y=['ISO Vel RMS Motor', 'ISO Vel RMS Fan'],
                                labels={'value': "Vibration (mm/s RMS)", 'timestamp': "Time"},
                                title="🔍 Vibration Levels Over Time")
        st.plotly_chart(fig_vibration)
    except Exception as e:
        st.error(f"❌ Error plotting Vibration Chart: {e}")

    st.info("ℹ️ High vibration levels at specific speeds can indicate belt misalignment.")

else:
    st.warning("⚠️ No data loaded. Please check file paths and restart the app.")
