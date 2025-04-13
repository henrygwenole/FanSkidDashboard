# Sensor_Data.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import extract_features, load_model

st.set_page_config(page_title="Sensor Signal Analysis", layout="wide")
st.title("📈 Sensor Signal Analysis")

# Simulated signals for example
data_path_faulty = "data/Data 110-F-0/51.txt"
data_path_healthy = "data/Data 110-H-0/51.txt"

try:
    faulty_data = np.loadtxt(data_path_faulty, delimiter="\t", usecols=(1, 2))
    healthy_data = np.loadtxt(data_path_healthy, delimiter="\t", usecols=(1, 2))

    sample_rate = 10000  # Hz

    def compute_fft(signal):
        fft_vals = np.fft.rfft(signal - np.mean(signal))
        fft_freq = np.fft.rfftfreq(len(signal), d=1/sample_rate)
        magnitude = np.abs(fft_vals)
        return fft_freq, magnitude

    # Signals
    impeller_faulty = faulty_data[:, 0]
    motor_faulty = faulty_data[:, 1]
    impeller_healthy = healthy_data[:, 0]
    motor_healthy = healthy_data[:, 1]

    # FFT for comparison
    impeller_freq_f, impeller_mag_f = compute_fft(impeller_faulty)
    impeller_freq_h, impeller_mag_h = compute_fft(impeller_healthy)

    motor_freq_f, motor_mag_f = compute_fft(motor_faulty)
    motor_freq_h, motor_mag_h = compute_fft(motor_healthy)

    # Plot: Motor Side (Pulley)
    st.subheader("FFT Comparison for Pulley Sensor")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(motor_freq_f, motor_mag_f, label='Faulty', color='red')
    ax1.plot(motor_freq_h, motor_mag_h, label='Good', color='blue')
    ax1.set_xlim(0, 220)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Magnitude")
    ax1.set_title("FFT Comparison for Pulley Sensor")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Plot: Impeller Side (Bearing)
    st.subheader("FFT Comparison for Bearing Sensor")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(impeller_freq_f, impeller_mag_f, label='Faulty', color='red')
    ax2.plot(impeller_freq_h, impeller_mag_h, label='Good', color='blue')
    ax2.set_xlim(0, 220)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_title("FFT Comparison for Bearing Sensor")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    # AR Maintenance Link
    st.markdown("""
    ### 👓 Launch AR Maintenance App
    [Open on HoloLens](https://fanskiddashboard-gubxuivehlan4hbdadp6ph.streamlit.app)
    """, unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Failed to load or process signal data. Please check file paths or format.")
