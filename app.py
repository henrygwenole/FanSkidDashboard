# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")
st.title("🛠️ Predictive Maintenance Dashboard")

# --- Overview Block Grid ---
st.subheader("System Health Overview")
clicked_component = st.session_state.get("clicked_component", None)
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
        if st.button(f"{'✅' if status else '❌'} {label}"):
            st.session_state.clicked_component = label
        st.markdown(
            f"""
            <div style='padding:1rem; background-color:{'#d4edda' if status else '#f8d7da'}; border:1px solid {'#155724' if status else '#721c24'}; border-radius:10px'>
                <h4 style='color:{'#155724' if status else '#721c24'}'>{'✅' if status else '❌'} {label}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

if clicked_component:
    st.markdown(f"## 🔍 Detailed Analysis for {clicked_component}")

    # Display a section specific to the selected component
    st.write("Sensor location:", clicked_component)
    st.write("Status:", "⚠️ Fault Detected" if not status_map[clicked_component] else "✅ Healthy")

    st.write("---")
    st.subheader("Raw Signal and Frequency Analysis")
    for signal, label in zip([impeller_signal, motor_signal], ["Impeller Side (Bearing)", "Motor Side (Pulley)"]):
        freq, fft_magnitude = compute_fft(signal)
        fig, ax = plt.subplots()
        ax.plot(freq, fft_magnitude, label='FFT Magnitude')
        ax.set_xlim(0, 30)
        ax.set_ylim(0, np.max(fft_magnitude[:len(freq)//4]) * 1.2)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_title(f"FFT of {label} Signal")

        for f_label, f_val in char_freqs.items():
            color = "orange" if f_label == "n/2" else "purple"
            linestyle = "-." if f_label == "n/2" else "--"
            ax.axvline(f_val, color=color, linestyle=linestyle, alpha=0.6)
            ax.text(f_val, np.max(fft_magnitude[:len(freq)//4]) * 0.9, f"{f_label}", color=color, ha="center", fontsize=8, rotation=90)

        st.pyplot(fig)

st.markdown("""
This dashboard analyzes vibration data from a belt-driven system to detect misalignment or wear.

Analysing the vibration data in the frequency domain provides critical insights that are not as easily observed in the time domain. By converting the data to the frequency domain using Fast Fourier Transform (FFT), we can identify specific frequency components associated with various mechanical behaviours and potential faults within the system.

When FFT is applied directly to the raw signal, a large spike may appear at 0 Hz — this is a **DC offset**. Since it doesn’t provide useful mechanical information, we remove it by subtracting the **mean of the signal** before computing the FFT.

#### 🔍 Key Frequency Components to Monitor:
- **Belt Frequency (fr):** Main belt frequency with harmonics at 2fr, 4fr, etc.
- **Drive Speed (n):** Pulley or motor rotation frequency and its harmonics.
- **Half Drive Speed (n/2):** Often reveals misalignment or load imbalance issues.

🧠 **Note**: The dataset contains 10,000 samples collected over 100 seconds, giving a sampling rate of **100 Hz**. However, if you're seeing valid content up to 5,000 Hz, then the true sampling rate is **10,000 Hz**. This has now been correctly reflected in the frequency axis.
""")

# Load default data directly without file uploader
try:
    data = np.loadtxt("data/Data 110-F-0/51.txt", delimiter="	", usecols=(1, 2))
except Exception as e:
    st.error("Failed to load default example file.")
    st.stop()

impeller_signal = data[:, 0] - np.mean(data[:, 0])  # Impeller side (Bearing)
motor_signal = data[:, 1] - np.mean(data[:, 1])     # Motor side (Pulley)

# Plot time-domain signals
st.subheader("Time Domain Signals")
st.line_chart({"Impeller Side (Bearing)": impeller_signal, "Motor Side (Pulley)": motor_signal})

# Frequency analysis function
def compute_fft(signal, sample_rate=10000):
    windowed = signal * np.hanning(len(signal))
    fft_result = np.fft.fft(windowed)
    freq = np.fft.fftfreq(len(signal), d=1/sample_rate)
    return freq[:len(signal) // 2], np.abs(fft_result[:len(signal) // 2]) / len(signal)

def calculate_characteristic_frequencies(speed_rpm, driver_diameter=63, belt_length=912):
    drive_speed_hz = speed_rpm / 60
    fr = (drive_speed_hz * np.pi * driver_diameter) / belt_length
    return {
        "n/2": drive_speed_hz / 2,
        "fr": fr,
        "2fr": 2 * fr,
        "4fr": 4 * fr,
        "6fr": 6 * fr,
        "8fr": 8 * fr,
        "n": drive_speed_hz
    }

char_freqs = calculate_characteristic_frequencies(2000)

# Plot FFT for both measurements
for signal, label in zip([impeller_signal, motor_signal], ["Impeller Side (Bearing)", "Motor Side (Pulley)"]):
    freq, fft_magnitude = compute_fft(signal)
    fig, ax = plt.subplots()
    ax.plot(freq, fft_magnitude, label='FFT Magnitude')
    ax.set_xlim(0, 30)
    ax.set_ylim(0, np.max(fft_magnitude[:len(freq)//4]) * 1.2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title(f"FFT of {label} Signal (DC removed)")

    for f_label, f_val in char_freqs.items():
        color = "orange" if f_label == "n/2" else "purple"
        linestyle = "-." if f_label == "n/2" else "--"
        ax.axvline(f_val, color=color, linestyle=linestyle, alpha=0.6)
        ax.text(f_val, np.max(fft_magnitude[:len(freq)//4]) * 0.9, f"{f_label}", color=color, ha="center", fontsize=8, rotation=90)

    st.pyplot(fig)

# Illustrative classification logic (for demo purposes only)
def illustrate_classification(signal):
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal))
    if rms > 0.05 and peak > 0.1:
        return "⚠️ Fault Detected", "Maintenance Required! Possible misalignment or belt wear."
    else:
        return "✅ Healthy", "System appears to be running normally."

# Use impeller side signal for demonstration
classification_label, explanation = illustrate_classification(impeller_signal)

st.subheader("Illustrated Diagnostic Result")
st.write(classification_label)
if "Fault" in classification_label:
    st.error(explanation)
else:
    st.success(explanation)

st.markdown("""
### 👓 Launch AR Maintenance App
[Open on HoloLens](frn://s/6u615mm)
""", unsafe_allow_html=True)
