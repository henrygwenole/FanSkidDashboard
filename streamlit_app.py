import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

# Set page configuration
st.set_page_config(
    page_title="Fan Skid Predictive Maintenance",
    page_icon="🔧",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    # In production, you would load from a file or database
    # For now, using the sample data provided
    data = {
        "Timestamp": ["30:26.9", "26:53.4", "17:08.0", "07:03.9", "47:08.7"],
        "Motor Transmission Looseness": [2.963829, 2.950585, 3.90206, 4.883557, 3.117327],
        "Driven Unbalance/Misalignment": [-0.4654623, -0.4180369, -0.1298067, 1.061992, 0.5318896],
        "Electrical Rotor": [-0.2054151, -0.2052748, -0.1716933, -0.1548714, -0.1887314],
        "Driven Transmission Looseness": [3.048656, 2.928479, 3.915754, 4.953199, 2.956074],
        "Electrical Stator": [-0.5956343, -0.5949996, -0.5853148, -0.5881479, -0.5935417],
        "Electrical Odd Harmonics": [1.882828, 1.769092, 2.370785, 7.009338, 3.402307],
        "Electrical Even Harmonics": [-0.4175622, -0.4160648, -0.3518021, -0.356594, -0.372181],
        "Motor Unbalance/Misalignment": [-0.445515, -0.3809397, -0.1298067, 1.061992, 0.3155229],
        "Motor Bearing 1": [2.449097, 2.082776, 2.900844, 2.976794, 2.493944],
        "Motor Bearing 2": [1.937751, 1.508186, 2.361052, 2.961631, 2.444802],
        "Active Power": [25.69968704, 26.2600621, 25.71063137, 26.75807222, 25.97486275],
        "I1 RMS": [76.56158409, 76.06949171, 75.72623072, 76.59816045, 78.74206037],
        "I2 RMS": [79.83294691, 80.46531467, 80.99895297, 81.11500183, 82.0374348],
        "I3 RMS": [80.70576884, 79.01587691, 81.38101629, 81.1674286, 82.87993226],
        "I Balance": [3.127599402, 3.117039636, 4.589341994, 3.803619835, 3.050670514],
        "Nominal Current": [161, 161, 161, 161, 161],
        "Nominal Frequency": [50, 50, 50, 50, 50],
        "Power Factor": [0.514096976, 0.536330292, 0.522987478, 0.539021123, 0.514917311],
        "Reactive Power": [42.87799131, 41.32473536, 41.90197635, 41.81304925, 43.24322957],
        "V1 RMS": [220.8074938, 220.4609231, 220.5472217, 220.3193981, 220.6850383],
        "V2 RMS": [221.731615, 221.2495346, 221.8505979, 221.0554555, 222.0340967],
        "V3 RMS": [223.0397153, 222.6107596, 223.1291838, 222.539784, 223.0932874],
        "V Balance": [0.531916225, 0.528518647, 0.583798746, 0.558010648, 0.564319221],
        "WasteKW": [3.607286103, 3.568150315, 3.385136471, 3.956564931, 4.155666219],
        "WasteCost": [10111.94440352, 10002.23896332, 9489.21455667, 11091.04281435, 11649.16354573]
    }
    
    # Create a dataframe
    df = pd.DataFrame(data)
    
    # Convert timestamps to datetime
    # Since these aren't standard timestamps, we'll create some dummy dates for visualization
    base_date = datetime.now() - timedelta(days=5)
    dates = [base_date + timedelta(days=i) for i in range(len(df))]
    df['DateTimeStamp'] = dates
    
    return df

# Function to define health thresholds
def get_component_thresholds():
    return {
        "Motor Transmission Looseness": {"good": 2.0, "warning": 3.0, "critical": 4.0},
        "Driven Transmission Looseness": {"good": 2.0, "warning": 3.0, "critical": 4.0},
        "Motor Unbalance/Misalignment": {"good": 0.0, "warning": 0.5, "critical": 1.0},
        "Driven Unbalance/Misalignment": {"good": 0.0, "warning": 0.5, "critical": 1.0},
        "Motor Bearing 1": {"good": 1.5, "warning": 2.5, "critical": 3.5},
        "Motor Bearing 2": {"good": 1.5, "warning": 2.5, "critical": 3.5},
        "Electrical Rotor": {"good": 0.0, "warning": -0.3, "critical": -0.5},
        "Electrical Stator": {"good": -0.3, "warning": -0.5, "critical": -0.7},
        "Electrical Odd Harmonics": {"good": 1.5, "warning": 3.0, "critical": 5.0},
        "Electrical Even Harmonics": {"good": -0.2, "warning": -0.3, "critical": -0.4},
        "Power Factor": {"good": 0.85, "warning": 0.7, "critical": 0.5}
    }

# Calculate health status based on thresholds
def get_health_status(value, thresholds):
    if isinstance(thresholds["good"], (int, float)) and isinstance(thresholds["warning"], (int, float)) and isinstance(thresholds["critical"], (int, float)):
        if thresholds["good"] < thresholds["warning"]:  # Case: higher is worse
            if value <= thresholds["good"]:
                return "Good", "green"
            elif value <= thresholds["warning"]:
                return "Warning", "orange"
            else:
                return "Critical", "red"
        else:  # Case: lower is worse
            if value >= thresholds["good"]:
                return "Good", "green"
            elif value >= thresholds["warning"]:
                return "Warning", "orange"
            else:
                return "Critical", "red"
    return "Unknown", "gray"

# Calculate waste costs for different periods
def calculate_waste_costs(df):
    if df.empty:
        return 0, 0, 0, 0
    
    avg_waste_per_day = df['WasteKW'].mean() * 24  # kWh per day
    avg_cost_per_day = avg_waste_per_day * 0.34  # £0.34 per kWh (example rate)
    
    return {
        "day": avg_cost_per_day,
        "week": avg_cost_per_day * 7,
        "month": avg_cost_per_day * 30,
        "year": avg_cost_per_day * 365
    }

# Function to embed PDF maintenance procedure
def get_maintenance_pdf_display(pdf_url):
    pdf_display = f"""
        <div style="display: flex; justify-content: center;">
            <iframe src="{pdf_url}" width="800" height="600" type="application/pdf"></iframe>
        </div>
    """
    return pdf_display

# Start of the main app
def main():
    st.title("🔧 Fan Skid Predictive Maintenance Dashboard")
    
    # Load data
    df = load_data()
    thresholds = get_component_thresholds()
    
    # Get latest reading
    latest = df.iloc[-1]
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Detailed Analysis", "Maintenance Procedures"])
    
    if page == "Dashboard":
        # Summary metrics at the top
        col1, col2, col3 = st.columns(3)
        
        # Overall health status based on critical components
        motor_status, motor_color = get_health_status(latest["Motor Transmission Looseness"], thresholds["Motor Transmission Looseness"])
        driven_status, driven_color = get_health_status(latest["Driven Transmission Looseness"], thresholds["Driven Transmission Looseness"])
        motor_bal_status, motor_bal_color = get_health_status(latest["Motor Unbalance/Misalignment"], thresholds["Motor Unbalance/Misalignment"])
        
        with col1:
            st.subheader("System Status")
            overall_status = "Critical" if "Critical" in [motor_status, driven_status, motor_bal_status] else "Warning" if "Warning" in [motor_status, driven_status, motor_bal_status] else "Good"
            overall_color = "red" if overall_status == "Critical" else "orange" if overall_status == "Warning" else "green"
            st.markdown(f"<h1 style='text-align: center; color: {overall_color};'>{overall_status}</h1>", unsafe_allow_html=True)
        
        with col2:
            st.subheader("Latest Reading")
            st.markdown(f"<h3 style='text-align: center;'>{latest['DateTimeStamp'].strftime('%Y-%m-%d %H:%M')}</h3>", unsafe_allow_html=True)
        
        with col3:
            st.subheader("Daily Power Waste")
            waste_costs = calculate_waste_costs(df)
            st.markdown(f"<h3 style='text-align: center;'>£{waste_costs['day']:.2f}/day</h3>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main component health indicators
        st.subheader("Component Health")
        
        # Create three columns layout
        col1, col2, col3 = st.columns(3)
        
        # Format for health indicators
        def health_indicator(title, value, thresholds):
            status, color = get_health_status(value, thresholds)
            return f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px;">
                <h4>{title}</h4>
                <h2 style="color: {color};">{value:.2f}</h2>
                <p style="color: {color};">{status}</p>
            </div>
            """
        
        # Key health metrics
        with col1:
            st.markdown(health_indicator("Motor Transmission Looseness", latest["Motor Transmission Looseness"], thresholds["Motor Transmission Looseness"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Motor Unbalance/Misalignment", latest["Motor Unbalance/Misalignment"], thresholds["Motor Unbalance/Misalignment"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Motor Bearing 1", latest["Motor Bearing 1"], thresholds["Motor Bearing 1"]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(health_indicator("Driven Transmission Looseness", latest["Driven Transmission Looseness"], thresholds["Driven Transmission Looseness"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Driven Unbalance/Misalignment", latest["Driven Unbalance/Misalignment"], thresholds["Driven Unbalance/Misalignment"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Motor Bearing 2", latest["Motor Bearing 2"], thresholds["Motor Bearing 2"]), unsafe_allow_html=True)
        
        with col3:
            st.markdown(health_indicator("Electrical Rotor", latest["Electrical Rotor"], thresholds["Electrical Rotor"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Electrical Stator", latest["Electrical Stator"], thresholds["Electrical Stator"]), unsafe_allow_html=True)
            st.markdown(health_indicator("Power Factor", latest["Power Factor"], thresholds["Power Factor"]), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trend charts
        st.subheader("Trend Analysis")
        
        # Select time range
        time_range = st.selectbox("Time Range", ["Last 7 days", "Last 30 days", "All data"])
        
        # Two columns for key trend charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Unbalance trend chart
            fig_unbalance = px.line(df, x="DateTimeStamp", y=["Motor Unbalance/Misalignment", "Driven Unbalance/Misalignment"],
                                    title="Unbalance/Misalignment Trend", labels={"value": "Value", "variable": "Component"})
            
            # Add threshold lines
            fig_unbalance.add_hline(y=thresholds["Motor Unbalance/Misalignment"]["warning"], line_dash="dash", line_color="orange")
            fig_unbalance.add_hline(y=thresholds["Motor Unbalance/Misalignment"]["critical"], line_dash="dash", line_color="red")
            
            st.plotly_chart(fig_unbalance, use_container_width=True)
        
        with col2:
            # Transmission looseness trend chart
            fig_loose = px.line(df, x="DateTimeStamp", y=["Motor Transmission Looseness", "Driven Transmission Looseness"],
                                title="Transmission Looseness Trend", labels={"value": "Value", "variable": "Component"})
            
            # Add threshold lines
            fig_loose.add_hline(y=thresholds["Motor Transmission Looseness"]["warning"], line_dash="dash", line_color="orange")
            fig_loose.add_hline(y=thresholds["Motor Transmission Looseness"]["critical"], line_dash="dash", line_color="red")
            
            st.plotly_chart(fig_loose, use_container_width=True)
        
        # Power waste impact
        st.subheader("Power Waste Impact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            waste_costs = calculate_waste_costs(df)
            waste_periods = ['day', 'week', 'month', 'year']
            waste_values = [waste_costs[period] for period in waste_periods]
            
            fig_waste = px.bar(x=waste_periods, y=waste_values, 
                                labels={'x': 'Period', 'y': 'Cost (£)'},
                                title="Waste Cost by Period")
            
            st.plotly_chart(fig_waste, use_container_width=True)
        
        with col2:
            st.subheader("Power Waste Over Time")
            fig_waste_trend = px.line(df, x="DateTimeStamp", y="WasteKW", 
                                     title="Power Waste Trend (kW)",
                                     labels={"WasteKW": "Waste Power (kW)", "DateTimeStamp": "Date"})
            st.plotly_chart(fig_waste_trend, use_container_width=True)
        
        # Add alert box for critical issues
        if overall_status == "Critical":
            st.error("""
            ### Critical Issue Detected!
            
            The fan skid shows signs of severe belt unbalance/misalignment. Immediate maintenance is recommended to prevent further damage and reduce power waste.
            
            [Go to Maintenance Procedure →](#)
            """)
        
        elif overall_status == "Warning":
            st.warning("""
            ### Warning: Potential Issues Detected
            
            Early signs of unbalance/misalignment detected. Schedule maintenance in the next 1-2 weeks to prevent progression to critical status.
            
            [Go to Maintenance Procedure →](#)
            """)
    
    elif page == "Detailed Analysis":
        st.header("Detailed Component Analysis")
        
        # Component selector
        component = st.selectbox("Select Component to Analyze", 
                             [col for col in df.columns if col not in ["Timestamp", "DateTimeStamp", "WasteKW", "WasteCost", "Nominal Current", "Nominal Frequency"]])
        
        # Show historical trend with thresholds if available
        st.subheader(f"{component} Historical Trend")
        
        fig = px.line(df, x="DateTimeStamp", y=component, markers=True)
        
        # Add threshold lines if available for this component
        if component in thresholds:
            for level, value in thresholds[component].items():
                color = "green" if level == "good" else "orange" if level == "warning" else "red"
                fig.add_hline(y=value, line_dash="dash", line_color=color, annotation_text=level.capitalize())
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Component correlation analysis
        st.subheader("Component Correlation Analysis")
        
        # Select components to correlate
        corr_component = st.selectbox("Select component to correlate with", 
                                  [col for col in df.columns if col != component and col not in ["Timestamp", "DateTimeStamp"]])
        
        # Correlation scatter plot
        fig_corr = px.scatter(df, x=component, y=corr_component, trendline="ols", 
                           title=f"Correlation between {component} and {corr_component}")
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Correlation statistics
        corr_value = df[component].corr(df[corr_component])
        st.metric("Correlation Coefficient", f"{corr_value:.4f}")
        
        # Data table
        st.subheader("Raw Data")
        st.dataframe(df[["DateTimeStamp", component, corr_component]])
        
    elif page == "Maintenance Procedures":
        st.header("Maintenance Procedures")
        
        # Maintenance procedure selector
        procedure_type = st.selectbox("Select Maintenance Procedure", 
                                  ["Belt Alignment", "Bearing Replacement", "General Maintenance", "Electrical System Check"])
        
        # Display maintenance procedures
        if procedure_type == "Belt Alignment":
            st.subheader("Belt Alignment Procedure")
            
            # Display steps
            st.markdown("""
            ### Belt Alignment Procedure
            
            **Safety First:** Ensure machine is powered off and locked out before beginning any maintenance.
            
            #### Required Tools:
            - Laser alignment tool
            - Allen wrench set
            - Torque wrench
            - Straight edge
            
            #### Steps:
            1. **Preparation**
               - Shut down the fan skid and follow lockout/tagout procedures
               - Remove belt guards
            
            2. **Inspection**
               - Check belt condition for wear, cracks, or glazing
               - Inspect pulleys for damage or wear
            
            3. **Alignment Process**
               - Set up laser alignment tool according to manufacturer instructions
               - Measure and record initial misalignment values
               - Loosen motor mount bolts slightly to allow adjustment
               - Adjust motor position using alignment tool readings
               - Tighten bolts to specified torque (refer to equipment manual)
               - Verify alignment is within tolerance (typically <0.5° angular, <2mm parallel)
            
            4. **Final Check**
               - Rotate pulley manually to ensure smooth operation
               - Replace belt guards
               - Remove lockout/tagout
               - Test run at low speed and verify vibration readings have improved
            
            5. **Documentation**
               - Record maintenance performed
               - Document new alignment values
               - Schedule follow-up check after 1 week of operation
            """)
            
            # Download procedure button
            st.download_button(
                label="Download Procedure as PDF",
                data=b"Sample PDF content", # In production, this would be actual PDF content
                file_name="belt_alignment_procedure.pdf",
                mime="application/pdf"
            )
            
            # Link to video tutorial (placeholder)
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        elif procedure_type == "Bearing Replacement":
            st.subheader("Bearing Replacement Procedure")
            # Display bearing replacement procedure content
            st.markdown("Bearing replacement procedure content would go here...")
        
        elif procedure_type == "General Maintenance":
            st.subheader("General Maintenance Checklist")
            # Display general maintenance content
            st.markdown("General maintenance checklist content would go here...")
        
        elif procedure_type == "Electrical System Check":
            st.subheader("Electrical System Check")
            # Display electrical system check content
            st.markdown("Electrical system check procedure content would go here...")
        
        # Maintenance history log
        st.subheader("Maintenance History")
        
        # Sample maintenance log
        maintenance_log = pd.DataFrame({
            "Date": ["2025-02-15", "2025-01-10", "2024-12-05"],
            "Procedure": ["Belt Alignment", "General Maintenance", "Bearing Replacement"],
            "Technician": ["John Smith", "Emma Johnson", "Mike Wilson"],
            "Notes": ["Corrected 1.2° misalignment", "Scheduled maintenance", "Replaced DE bearing due to wear"]
        })
        
        st.dataframe(maintenance_log)
        
        # Form to add new maintenance record
        st.subheader("Log New Maintenance")
        with st.form("maintenance_log_form"):
            date = st.date_input("Date", datetime.now())
            procedure = st.selectbox("Procedure", ["Belt Alignment", "Bearing Replacement", "General Maintenance", "Electrical System Check"])
            technician = st.text_input("Technician Name")
            notes = st.text_area("Notes")
            
            submit_button = st.form_submit_button("Log Maintenance")
            if submit_button:
                st.success("Maintenance logged successfully")

if __name__ == "__main__":
    main()